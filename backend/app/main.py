from fastapi import FastAPI, Depends
from pydantic import BaseModel
from sqlalchemy.orm import Session
from app import models, schemas, crud, database
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

models.Base.metadata.create_all(bind=database.engine)

# 開放前端跨域請求
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 生產環境請改為特定前端網址
    allow_methods=["*"],
    allow_headers=["*"],
)

class FormData(BaseModel):
    chineseName: str
    englishName: str
    gender: str
    degree: str
    school: str
    major: str
    graduationYear: str
    linkedin: str
    hasInternship: bool
    joined: bool
    jobTitle: str
    jobCompany: str
    jobIndustry: str


@app.get("/")
def read_root():
    return {"message": "Welcome to the Career Analyzer API"}

# Dependency
def get_db():
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.post("/users/", response_model=schemas.UserInfo)
def create_user(user: schemas.UserInfoCreate, db: Session = Depends(get_db)):
    return crud.create_user(db=db, user=user)

@app.post("/jobtitle/", response_model=schemas.JobTitle)
def create_jobtitle(title: schemas.JobTitleCreate, db: Session = Depends(get_db)):
    return crud.create_jobtitle(db=db, title=title)

@app.post("/industry/", response_model=schemas.IndustryCategory)
def create_industry(industry: schemas.IndustryCreate, db: Session = Depends(get_db)):
    return crud.create_industry(db=db, industry=industry)

@app.get("/users/", response_model=list[schemas.UserInfo])
def read_users(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    users = crud.get_users(db, skip=skip, limit=limit)
    return users

@app.get("/jobtitle/", response_model=list[schemas.JobTitle])
def read_jobtitle(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    return crud.get_jobtitles(db, skip=skip, limit=limit)

@app.get("/industry/", response_model=list[schemas.IndustryCategory])
def read_industry(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    return crud.get_industries(db, skip=skip, limit=limit)
