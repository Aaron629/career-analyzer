# app/crud.py

from sqlalchemy.orm import Session
from . import models, schemas

def create_user(db: Session, user: schemas.UserInfoCreate):
    db_user = models.UserInfo(**user.model_dump())
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def create_jobtitle(db: Session, title: schemas.JobTitleCreate):
    db_title = models.JobTitle(**title.model_dump())
    db.add(db_title)
    db.commit()
    db.refresh(db_title)
    return db_title

def create_industry(db: Session, industry: schemas.IndustryCreate):
    db_industry = models.IndustryCategory(**industry.model_dump())
    db.add(db_industry)
    db.commit()
    db.refresh(db_industry)
    return db_industry

def get_users(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.UserInfo).offset(skip).limit(limit).all()

def get_jobtitles(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.JobTitle).offset(skip).limit(limit).all()

def get_industries(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.IndustryCategory).offset(skip).limit(limit).all()
