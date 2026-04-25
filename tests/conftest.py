from typing import Any, Generator
from uuid import uuid4

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import Engine, create_engine
from sqlalchemy.orm import Session
from testcontainers.postgres import PostgresContainer

from bill_splitter_api.auth.security import create_access_token, get_password_hash
from bill_splitter_api.dependencies import get_current_user, get_db
from bill_splitter_api.main import app
from bill_splitter_api.models import User
from bill_splitter_api.models.base import Base


@pytest.fixture
def pg_container() -> Generator[PostgresContainer, None, None]:
    with PostgresContainer("postgres:alpine") as postgres:
        yield postgres


@pytest.fixture
def engine(pg_container: PostgresContainer):
    connection_url = pg_container.get_connection_url().replace("psycopg2", "psycopg")
    print(f"Using database URL: {connection_url}")
    # connection_url = pg_container.get_connection_url()
    engine = create_engine(connection_url, echo=False)
    Base.metadata.create_all(engine)
    yield engine
    Base.metadata.drop_all(engine)
    engine.dispose()


@pytest.fixture
def session(engine: Engine) -> Generator[Session, None, None]:
    with Session(engine) as session:
        yield session
        session.rollback()


@pytest.fixture
def test_user(session: Session) -> User:
    user = User(
        id=uuid4(),
        username="testuser",
        email="testuser@example.com",
        password_hash=get_password_hash("testpassword"),
    )
    session.add(user)
    session.commit()
    session.refresh(user)
    return user


@pytest.fixture
def auth_token(test_user: User) -> str:
    return create_access_token(test_user)


@pytest.fixture
def unauthenticated_client(session: Session) -> Generator[TestClient, Any, None]:
    def override_get_db():
        yield session

    app.dependency_overrides[get_db] = override_get_db

    with TestClient(app) as test_client:
        yield test_client

    app.dependency_overrides.clear()


@pytest.fixture
def client(
    unauthenticated_client: TestClient,
    test_user: User,
    auth_token: str,
) -> Generator[TestClient, Any, None]:
    authenticated_client = unauthenticated_client

    def override_get_current_user():
        return test_user

    app.dependency_overrides[get_current_user] = override_get_current_user
    authenticated_client.headers.update({"Authorization": f"Bearer {auth_token}"})
    yield authenticated_client
