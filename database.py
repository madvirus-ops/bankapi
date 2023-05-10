from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from dotenv import load_dotenv
import os
load_dotenv()


db_url = os.getenv('SQLALCHEMY_DATABASE_URL')

engine = create_engine(db_url,echo=True)

Base = declarative_base()

SessionLocal = sessionmaker(bind=engine,autocommit=False,autoflush=False)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()