import pytest
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from fastapi import FastAPI
from ..main import include_router
from ..database import Base
from typing import Generator,Any






SQLALCHEMY_DATABASE_URL = "sqlite:///./test_db.sqlite3"
engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)

SessionTesting = sessionmaker(autocommit=False, autoflush=False, bind=engine)

@pytest.fixture(scope='function')
def _get_test_db():
    db = SessionTesting()
    try:
        yield db
    except:
        db.rollback()
    finally:
        db.close()


def start_application():
    app = FastAPI()
    include_router(app)
    return app


@pytest.fixture(scope="function")
def app() -> Generator[FastAPI, Any, None]:
    """
    Create a fresh database on each test case.
    """
    Base.metadata.create_all(engine) 
    _app = start_application()
    yield _app
    Base.metadata.drop_all(engine)