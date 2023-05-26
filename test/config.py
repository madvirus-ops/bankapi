from typing import Any
from typing import Generator

import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker



from database import Base
from database import get_db
from main import include_router
from utils import get_current_user




class User:
    def __init__(self, id, email, first_name, last_name, password):
        self.id = id
        self.email = email
        self.first_name = first_name
        self.last_name = last_name
        self.password = password





def start_application():
    app = FastAPI()
    include_router(app)
    return app


SQLALCHEMY_DATABASE_URL = "sqlite:///./test_db.db"
engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)
# Use connect_args parameter only with sqlite
SessionTesting = sessionmaker(autocommit=False, autoflush=False, bind=engine)


@pytest.fixture(scope="function")
def app() -> Generator[FastAPI, Any, None]:
    """
    Create a fresh database on each test case.
    """
    Base.metadata.create_all(engine)  # Create the tables.
    _app = start_application()
    yield _app
    Base.metadata.drop_all(engine)


@pytest.fixture(scope="function")
def db_session(app: FastAPI) -> Generator[SessionTesting, Any, None]:
    connection = engine.connect()
    transaction = connection.begin()
    session = SessionTesting(bind=connection)
    yield session  # use the session in tests.
    session.close()
    transaction.rollback()
    connection.close()



@pytest.fixture(scope="function")
def client(
    app: FastAPI, db_session: SessionTesting
) -> Generator[TestClient, Any, None]:
    """
    Create a new FastAPI TestClient that uses the `db_session` fixture to override
    the `get_db` dependency that is injected into routes, also override the get_current_user
    """

    def _get_test_db():
        try:
            yield db_session
        finally:
            pass

    def _get_current_user():
        user = User(
            id=1,
            email="john@ben.com",
            first_name="john",
            last_name="beans",
            password="password"
        )
        return user

    app.dependency_overrides[get_db] = _get_test_db
    app.dependency_overrides[get_current_user] = _get_current_user

    with TestClient(app) as client:
        yield client







# ...

