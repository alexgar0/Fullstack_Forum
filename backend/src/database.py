from fastapi import FastAPI, Depends
from sqlalchemy import create_engine
DATABASE_URL = "postgresql://postgres_user:password@postgres_container:5432/postgres_db"
from sqlalchemy.orm import sessionmaker, Session, declarative_base

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()