# app/schemas.py

from pydantic import BaseModel,ConfigDict
from typing import Optional

class UserInfoBase(BaseModel):

    model_config = ConfigDict(
        populate_by_name=True,   # ✅ 使用原本欄位名稱
        extra="forbid",          # ✅ 拒絕多餘欄位（幫助排錯）
        from_attributes=True     # ✅ 支援 ORM 模式
    )

    chinese_name: str
    english_name: Optional[str]
    gender: Optional[str]
    degree: Optional[str]
    school_type: Optional[str]
    college_type: Optional[str]
    school_name: Optional[str]
    department: Optional[str]
    graduation_year: Optional[int]
    has_internship: Optional[bool]
    joined_bootcamp: Optional[bool]
    internship_count: Optional[int]
    linkedin_url: Optional[str]

class UserInfoCreate(UserInfoBase):
    pass

class UserInfo(UserInfoBase):
    pass

from typing import Optional


class JobTitle(BaseModel):
    id: int
    name: str
    standardized_name: str
    level: Optional[str]

    class Config:
        orm_mode = True


class JobTitleCreate(JobTitle):
    pass

class IndustryCategory(BaseModel):
    id: int
    name: str
    level1: str
    level2: Optional[str]
    note: Optional[str]

    class Config:
        orm_mode = True

class IndustryCreate(IndustryCategory):
    pass