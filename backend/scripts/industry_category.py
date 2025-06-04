import pandas as pd
import psycopg2
from dotenv import load_dotenv
import os

# 載入環境變數（含 DATABASE_URL）
load_dotenv()
DATABASE_URL = os.getenv("DATABASE_URL")

# 讀取 CSV
csv_path = "../data/industry_category.csv"
df = pd.read_csv(csv_path, encoding="utf-8-sig")

# 建立資料庫連線
conn = psycopg2.connect(DATABASE_URL)
cursor = conn.cursor()

# 插入每一筆分類資料
for _, row in df.iterrows():
    name = row["name"]
    sector = row["sector"]
    level1 = row["level1"]
    level2 = row["level2"] if pd.notna(row["level2"]) else None
    note = row["note"] if pd.notna(row["note"]) else None

    cursor.execute(
        """
        INSERT INTO industry_category (name, sector, level1, level2, note)
        VALUES (%s, %s, %s, %s, %s)
        ON CONFLICT (name) DO NOTHING;
        """,
        (name, sector, level1, level2, note)
    )

conn.commit()
cursor.close()
conn.close()

print("✅ industry_category 資料已成功匯入 PostgreSQL！")
