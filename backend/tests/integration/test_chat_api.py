from fastapi.testclient import TestClient
import pytest
from backend.app.main import app
from backend.app.db.database import get_session
from sqlmodel import Session, SQLModel, create_engine
import os

# Define a test database URL
TEST_DATABASE_URL = "sqlite:///./test_chat.db"

# Create a test engine
test_engine = create_engine(TEST_DATABASE_URL)

# Override the get_session dependency to use the test database
@pytest.fixture(name="session")
def session_fixture():
    SQLModel.metadata.create_all(test_engine)
    with Session(test_engine) as session:
        yield session
    SQLModel.metadata.drop_all(test_engine)
    test_engine.dispose() # Explicitly dispose of the engine to close connections
    # Clean up the test database file
    if os.path.exists("./test_chat.db"):
        os.remove("./test_chat.db")

@pytest.fixture(name="client")
def client_fixture(session: Session):
    def get_session_override():
        return session
    
    app.dependency_overrides[get_session] = get_session_override
    with TestClient(app) as client:
        yield client
    app.dependency_overrides.clear()

def test_chat_message_generic(client: TestClient):
    """
    Test that the chat /message endpoint uses the mocked process_message.
    """
    message_content = "Hello, bot!"
    response = client.post("/chat/message", json={"message": message_content})
    
    assert response.status_code == 200
    data = response.json()
    assert "response" in data
    assert "actions" in data
    assert data["response"] == f"AI Agent response (mocked for testing) to: '{message_content}'"
    assert data["actions"] == []
    assert data["tasks"] == []

def test_chat_message_listing_tasks(client: TestClient):
    """
    Test that the chat /message endpoint can parse and return tasks from AI response.
    Relies on the hardcoded mock in backend/app/api/chat.py.
    """
    message_content = "show me my list of tasks"
    response = client.post("/chat/message", json={"message": message_content})
    
    assert response.status_code == 200
    data = response.json()
    assert data["response"] == "AI has listed your tasks:\n- Task 1 (Completed: False)\n- Task 2 (Completed: True)"
    assert data["actions"] == []
    assert len(data["tasks"]) == 2
    assert data["tasks"][0]["description"] == "Task 1"
    assert data["tasks"][0]["is_completed"] == False
    assert data["tasks"][1]["description"] == "Task 2"
    assert data["tasks"][1]["is_completed"] == True

def test_chat_message_marking_task(client: TestClient):
    """
    Test that the chat /message endpoint handles AI response for marking a task.
    Relies on the hardcoded mock in backend/app/api/chat.py.
    """
    message_content = "mark task 1 as complete"
    response = client.post("/chat/message", json={"message": message_content})
    
    assert response.status_code == 200
    data = response.json()
    assert data["response"] == "AI has marked task 1 as complete."
    assert data["actions"] == []
    assert len(data["tasks"]) == 0 # No tasks to extract from this response type

def test_chat_message_updating_task(client: TestClient):
    """
    Test that the chat /message endpoint handles AI response for updating a task.
    Relies on the hardcoded mock in backend/app/api/chat.py.
    """
    message_content = "update task 2"
    response = client.post("/chat/message", json={"message": message_content})
    
    assert response.status_code == 200
    data = response.json()
    assert data["response"] == "AI has updated task 2."
    assert data["actions"] == []
    assert len(data["tasks"]) == 0

def test_chat_message_deleting_task(client: TestClient):
    """
    Test that the chat /message endpoint handles AI response for deleting a task.
    Relies on the hardcoded mock in backend/app/api/chat.py.
    """
    message_content = "delete task 3"
    response = client.post("/chat/message", json={"message": message_content})
    
    assert response.status_code == 200
    data = response.json()
    assert data["response"] == "AI has deleted task 3."
    assert data["actions"] == []
    assert len(data["tasks"]) == 0
