import pandas as pd
import psycopg2
from dotenv import load_dotenv
import os

# 載入環境變數
load_dotenv()
DATABASE_URL = os.getenv("DATABASE_URL")

# 讀入 career_experience.csv
csv_path = "../data/career_experience.csv"
df = pd.read_csv(csv_path, encoding="utf-8-sig")

# 建立資料庫連線
conn = psycopg2.connect(DATABASE_URL)
cursor = conn.cursor()

# 查出資料庫中已有的產業類別
cursor.execute("SELECT category_name FROM industry_category;")
existing_categories = set(row[0] for row in cursor.fetchall())

# 從 CSV 找出所有需要的分類
all_categories = set(df["industry_category"].dropna().unique())

# 找出缺漏的分類
missing_categories = all_categories - existing_categories

# 插入缺漏的分類
for category in missing_categories:
    print(f"✅ 新增產業類別：{category}")
    cursor.execute(
        "INSERT INTO industry_category (category_name) VALUES (%s) ON CONFLICT DO NOTHING;",
        (category,)
    )

# 提交變更並關閉
conn.commit()
cursor.close()
conn.close()

print("🎉 所有缺漏產業類別已補齊！")
