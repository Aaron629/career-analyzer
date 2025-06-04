import pandas as pd

# 讀取原始檔案（Tab 分隔）
df = pd.read_csv("../data/all.csv", encoding="utf-8-sig")  # ✅ 使用預設逗號分隔

# 欄位對應表：總表 → user_info 所需格式
column_mapping = {
    "編號": "id",
    "姓名": "chinese_name",
    "英文名": "english_name",
    "性別": "gender",
    "學位": "degree",
    "公/私立": "school_type",
    "普通大學/科技大學": "college_type",
    "最高學歷校名": "school_name",
    "科系": "department",
    "畢業年份": "graduation_year",
    "是否有實習": "has_internship",
    "轉職班": "joined_bootcamp",
    "實習數量": "internship_count",
    "檔案連結": "linkedin_url"
}

# 篩選並重新命名欄位
user_info_df = df[list(column_mapping.keys())].rename(columns=column_mapping)

# 輸出為新的 CSV
user_info_df.to_csv("user_info.csv", index=False, encoding="utf-8-sig")
print("✅ 已匯出 user_info.csv！")
