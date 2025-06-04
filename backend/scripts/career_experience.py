import pandas as pd
import psycopg2
from dotenv import load_dotenv
import os
from datetime import datetime

# 載入環境變數
load_dotenv()
DATABASE_URL = os.getenv("DATABASE_URL")

# 讀取轉換後的 CSV 檔案
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
csv_path = os.path.join(BASE_DIR, "../data/career_experience.csv")
df = pd.read_csv(csv_path)

# 處理 present 日期
current_date = datetime.today().date()
df['end_date'] = df['end_date'].replace(to_replace=r'(?i)^present$', value=current_date, regex=True)
df['start_date'] = pd.to_datetime(df['start_date'], errors='coerce').dt.date
df['end_date'] = pd.to_datetime(df['end_date'], errors='coerce').dt.date

# 建立資料庫連線
conn = psycopg2.connect(DATABASE_URL)
cursor = conn.cursor()

# 儲存所有錯誤紀錄
errors = []

# 檢查資料是否合法，並建立暫存結果
valid_rows = []

for _, row in df.iterrows():
    # 查詢職稱
    cursor.execute("SELECT id FROM job_title WHERE name = %s", (row["job_title"],))
    job_result = cursor.fetchone()

    # 查詢產業分類（用 level2 對應）
    cursor.execute("SELECT id FROM industry_category WHERE name = %s", (row["industry_id"],))
    industry_result = cursor.fetchone()

    if not industry_result:
        errors.append(f"❌ 無對應產業類別：{row['industry_id']}（user_id={row['user_id']}）")
    if not job_result:
        errors.append(f"❌ 無對應職稱：{row['job_title']}（user_id={row['user_id']}）")

    if job_result and industry_result:
        valid_rows.append((
            row["user_id"],
            job_result[0],
            row["company_name"],
            industry_result[0],
            row["start_date"],
            row["end_date"],
            row["experience_order"]
        ))

# 如果有錯誤，列出並退出
if errors:
    print("⚠️ 以下資料驗證失敗，請修正後再執行匯入：")
    for e in errors:
        print(e)
    print("🚫 匯入中止，未寫入任何資料。")
else:
    for row in valid_rows:
        cursor.execute(
            """
            INSERT INTO career_experience (
                user_id, job_title_id, company_name, industry_id,
                start_date, end_date, experience_order
            )
            VALUES (%s, %s, %s, %s, %s, %s, %s)
            ON CONFLICT DO NOTHING;
            """,
            row
        )
    conn.commit()
    print("✅ 所有資料驗證通過，career_experience 成功匯入！")

cursor.close()
conn.close()

