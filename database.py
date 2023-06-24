from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base,Session 
from collections.abc import Iterator
from dotenv import load_dotenv
import os
load_dotenv()


db_url = os.getenv('SQLALCHEMY_DATABASE_URL')

engine = create_engine(db_url,echo=True,pool_size=10)

Base = declarative_base()

SessionLocal = sessionmaker(bind=engine,autocommit=False,autoflush=False)


# def get_db() -> Iterator[Session]:
#     """
#         swapped out for this
#     """
#     with SessionLocal() as session:
#         yield session 
#Damn, i don write rubbish sha
def get_db():
    """ ensures the database connection is always closed 
        to use this we have to use fastapi.Depends() as an argument in the routes
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()