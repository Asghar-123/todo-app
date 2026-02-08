import pytest
from mcp_tools.tools.create_task import CreateTaskTool
from mcp_tools.tools.list_tasks import ListTasksTool
from mcp_tools.tools.mark_status import MarkTaskStatusTool
from mcp_tools.tools.filter_tasks import FilterTasksTool
from mcp_tools.tools.update_task import UpdateTaskTool
from mcp_tools.tools.delete_task import DeleteTaskTool
from datetime import date, timedelta
from fastapi.testclient import TestClient
from sqlmodel import Session
import os
from unittest.mock import patch # For patching os.getenv in tools if needed

# Note: The backend_test_client, mcp_test_db_session, and create_test_task fixtures
# are provided by mcp_tools/tests/conftest.py

# Ensure that the test runs with a mocked backend URL
@pytest.fixture(autouse=True)
def mock_backend_url_env(monkeypatch, backend_test_client: TestClient):
    monkeypatch.setenv("BACKEND_URL", backend_test_client.base_url)
    # Ensure IS_TESTING is set for conditional imports in backend/app/api/chat.py
    # This might be redundant here, but good for consistency
    monkeypatch.setenv("IS_TESTING", "true")

# Test for CreateTaskTool
def test_create_task_tool_success(backend_test_client: TestClient):
    tool = CreateTaskTool(description="Buy groceries", due_date=date(2026, 3, 1))
    result = tool.run()
    assert "Task 'Buy groceries'" in result
    assert "created successfully" in result
    # Verify task creation in the mocked backend
    response = backend_test_client.get("/tasks/")
    assert response.status_code == 200
    assert len(response.json()) == 1
    assert response.json()[0]["description"] == "Buy groceries"

def test_create_task_tool_no_due_date_success(backend_test_client: TestClient):
    tool = CreateTaskTool(description="Read a book")
    result = tool.run()
    assert "Task 'Read a book'" in result
    assert "created successfully" in result
    response = backend_test_client.get("/tasks/")
    assert response.status_code == 200
    assert any(task["description"] == "Read a book" for task in response.json())

# Test for ListTasksTool
def test_list_tasks_tool_all_success(backend_test_client: TestClient, mcp_test_db_session: Session):
    create_test_task(mcp_test_db_session, "Task 1", False)
    create_test_task(mcp_test_db_session, "Task 2", True)
    tool = ListTasksTool()
    result = tool.run()
    assert "Your tasks:" in result
    assert "ID: 1, Task 1 (Completed: False)" in result
    assert "ID: 2, Task 2 (Completed: True)" in result

def test_list_tasks_tool_filter_completed_success(backend_test_client: TestClient, mcp_test_db_session: Session):
    create_test_task(mcp_test_db_session, "Incomplete Task", False)
    create_test_task(mcp_test_db_session, "Completed Task", True)
    tool = ListTasksTool(is_completed=True)
    result = tool.run()
    assert "Filtered tasks:" not in result # Changed to match current format
    assert "ID: 2, Completed Task (Completed: True)" in result
    assert "Incomplete Task" not in result

def test_list_tasks_tool_no_tasks(backend_test_client: TestClient):
    tool = ListTasksTool()
    result = tool.run()
    assert "No tasks found matching the criteria." in result

# Test for MarkTaskStatusTool
def test_mark_task_status_tool_success(backend_test_client: TestClient, mcp_test_db_session: Session):
    task_id = create_test_task(mcp_test_db_session, "Task to mark", False)
    tool = MarkTaskStatusTool(task_id=task_id, is_completed=True)
    result = tool.run()
    assert f"Task 'Task to mark' (ID: {task_id}) marked as complete." in result
    # Verify status in backend
    response = backend_test_client.get(f"/tasks/?is_completed=true")
    assert response.status_code == 200
    assert any(t["id"] == task_id and t["is_completed"] is True for t in response.json())

def test_mark_task_status_tool_not_found(backend_test_client: TestClient):
    tool = MarkTaskStatusTool(task_id=999, is_completed=True)
    result = tool.run()
    assert "Failed to mark task 999 status: 404 Client Error: Not Found for url" in result

# Test for FilterTasksTool
def test_filter_tasks_tool_due_date_success(backend_test_client: TestClient, mcp_test_db_session: Session):
    today = date.today()
    tomorrow = date.fromisoformat(str(today)) + timedelta(days=1)
    create_test_task(mcp_test_db_session, "Task for today", due_date=today)
    create_test_task(mcp_test_db_session, "Task for tomorrow", due_date=tomorrow)
    tool = FilterTasksTool(due_date=today)
    result = tool.run()
    assert "Your tasks:" in result
    assert f"ID: 1, Task for today (Completed: False) (Due: {today})" in result
    assert "Task for tomorrow" not in result

# Test for UpdateTaskTool
def test_update_task_tool_description_success(backend_test_client: TestClient, mcp_test_db_session: Session):
    task_id = create_test_task(mcp_test_db_session, "Old description")
    tool = UpdateTaskTool(task_id=task_id, description="New description")
    result = tool.run()
    assert f"Task 'New description' (ID: {task_id}) updated successfully." in result
    response = backend_test_client.get(f"/tasks/{task_id}")
    assert response.json()["description"] == "New description"

# Test for DeleteTaskTool
def test_delete_task_tool_success(backend_test_client: TestClient, mcp_test_db_session: Session):
    task_id = create_test_task(mcp_test_db_session, "Task to delete")
    tool = DeleteTaskTool(task_id=task_id)
    result = tool.run()
    assert f"Task ID {task_id} deleted successfully." in result
    response = backend_test_client.get(f"/tasks/{task_id}")
    assert response.status_code == 404