from dotenv import load_dotenv
import os
from typing import Generator
from sqlmodel import Session, SQLModel, create_engine

# Load environment variables from .env file
load_dotenv()

# Get the database URL from environment variables
DATABASE_URL = os.getenv("DATABASE_URL")

# Ensure DATABASE_URL is set
if not DATABASE_URL:
    raise ValueError("DATABASE_URL environment variable is not set. Please set it in the .env file.")

# Create the SQLAlchemy engine
engine = create_engine(DATABASE_URL, echo=True)

def create_db_and_tables():
    """Creates all database tables defined by SQLModel metadata."""
    SQLModel.metadata.create_all(engine)

def get_session() -> Generator[Session, None, None]:
    """Provides a database session for dependency injection."""
    with Session(engine) as session:
        yield session
