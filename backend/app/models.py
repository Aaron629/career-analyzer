# app/models.py

from sqlalchemy import Column, Integer, String, Boolean
from .database import Base

class UserInfo(Base):
    __tablename__ = "user_info"

    id = Column(Integer, primary_key=True, index=True)
    chinese_name = Column(String, nullable=False)
    english_name = Column(String)
    gender = Column(String)  # male/female/other
    degree = Column(String)  # e.g. Bachelor, Master
    school_type = Column(String)  # 公立 / 私立
    college_type = Column(String)  # 普通大學 / 科技大學
    school_name = Column(String)
    department = Column(String)
    graduation_year = Column(Integer)
    has_internship = Column(Boolean)
    joined_bootcamp = Column(Boolean)
    internship_count = Column(Integer)
    linkedin_url = Column(String)


class JobTitle(Base):
    __tablename__ = "job_title"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    standardized_name = Column(String, nullable=False)
    level = Column(String, nullable=True)

class IndustryCategory(Base):
    __tablename__ = "industry_category"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    level1 = Column(String, nullable=False)
    level2 = Column(String, nullable=True)
    note = Column(String, nullable=True)