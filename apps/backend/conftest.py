from typing import Generator
import pytest
from fastapi.testclient import TestClient
from sqlmodel import Session, SQLModel, create_engine
from apps.backend.src.database import get_session
from apps.backend.src.main import app

# Setup a test database engine
sqlite_file_name = "test.db"
sqlite_url = f"sqlite:///{sqlite_file_name}"
engine = create_engine(sqlite_url, echo=True)

def create_db_and_tables():
    SQLModel.metadata.create_all(engine)

@pytest.fixture(name="client", scope="function") # Changed scope to function
def client_fixture(session: Session) -> Generator[TestClient, None, None]: # Depends on session
    def get_session_override():
        return session

    app.dependency_overrides[get_session] = get_session_override
    with TestClient(app) as client:
        yield client
    app.dependency_overrides.clear()
    # No need for create_db_and_tables() and drop_all here, session_fixture handles it

@pytest.fixture(name="session")
def session_fixture() -> Generator[Session, None, None]:
    create_db_and_tables()
    with Session(engine) as session:
        yield session
    SQLModel.metadata.drop_all(engine) # Clean up after tests
