import pandas as pd
import psycopg2
from dotenv import load_dotenv
import os

# 載入 .env 環境變數
load_dotenv()
DATABASE_URL = os.getenv("DATABASE_URL")

# 取得目前腳本的目錄，再組出 csv 檔案路徑
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
csv_path = os.path.join(BASE_DIR, "../data/job_title.csv")

# ✅ 讀取 CSV 檔案為 DataFrame
df = pd.read_csv(csv_path)

# 建立 PostgreSQL 連線
conn = psycopg2.connect(DATABASE_URL)
cursor = conn.cursor()

# 逐筆寫入 job_title 資料表
for _, row in df.iterrows():
    cursor.execute(
        """
        INSERT INTO job_title (name, standardized_name, level)
        VALUES (%s, %s, %s)
        ON CONFLICT DO NOTHING;  -- 若 name 重複則略過
        """,
        (row["name"], row["standardized_name"], row["level"])
    )

# 提交並關閉
conn.commit()
cursor.close()
conn.close()

print("✅ job_title 資料已成功寫入 PostgreSQL！")

