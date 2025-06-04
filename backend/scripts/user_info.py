import pandas as pd
import psycopg2
from dotenv import load_dotenv
import os

# 載入環境變數
load_dotenv()
DATABASE_URL = os.getenv("DATABASE_URL")

# 安全處理文字欄位
def safe_str(val):
    return str(val).strip() if pd.notna(val) else None

# 讀取 CSV
csv_path = "../data/user_info.csv"
df = pd.read_csv(csv_path, encoding="utf-8-sig")

# 連線資料庫
conn = psycopg2.connect(DATABASE_URL)
cursor = conn.cursor()

# 可選：清空資料
# cursor.execute("TRUNCATE TABLE user_info RESTART IDENTITY;")
# conn.commit()

# 插入資料
for _, row in df.iterrows():
    has_internship = bool(row["has_internship"]) if not pd.isna(row["has_internship"]) else False
    joined_bootcamp = bool(row["joined_bootcamp"]) if not pd.isna(row["joined_bootcamp"]) else False

    cursor.execute(
        """
        INSERT INTO user_info (
            id, chinese_name, english_name, gender, degree,
            school_type, college_type, school_name, department,
            graduation_year, has_internship, joined_bootcamp,
            internship_count, linkedin_url
        )
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        ON CONFLICT (id) DO NOTHING;
        """,
        (
            row["id"],
            safe_str(row["chinese_name"]),
            safe_str(row["english_name"]),
            safe_str(row["gender"]),
            safe_str(row["degree"]),
            safe_str(row["school_type"]),
            safe_str(row["college_type"]),
            safe_str(row["school_name"]),
            safe_str(row["department"]),
            int(row["graduation_year"]) if not pd.isna(row["graduation_year"]) else None,
            has_internship,
            joined_bootcamp,
            int(row["internship_count"]) if not pd.isna(row["internship_count"]) else 0,
            safe_str(row["linkedin_url"])
        )
    )

conn.commit()
cursor.close()
conn.close()
print("✅ user_info 資料已成功寫入 PostgreSQL！")
