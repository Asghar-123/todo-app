from fastapi.testclient import TestClient
from sqlmodel import Session, select
import pytest

# client fixture is provided by conftest.py

# Integration test for creating, reading, updating, and deleting tasks (T030)
def test_task_crud(client: TestClient):
    # Create Task
    create_response = client.post("/tasks/", json={"description": "Buy groceries"})
    assert create_response.status_code == 200
    created_task = create_response.json()
    assert created_task["description"] == "Buy groceries"
    assert created_task["is_completed"] is False
    assert "id" in created_task

    task_id = created_task["id"]

    # Read Tasks
    read_all_response = client.get("/tasks/")
    assert read_all_response.status_code == 200
    tasks = read_all_response.json()
    assert len(tasks) > 0
    assert any(task["id"] == task_id for task in tasks)

    # Read Single Task
    read_single_response = client.get(f"/tasks/{task_id}")
    assert read_single_response.status_code == 200
    read_task_data = read_single_response.json()
    assert read_task_data["id"] == task_id
    assert read_task_data["description"] == "Buy groceries"

    # Update Task
    update_response = client.put(f"/tasks/{task_id}", json={"description": "Buy organic groceries", "is_completed": True})
    assert update_response.status_code == 200
    updated_task = update_response.json()
    assert updated_task["id"] == task_id
    assert updated_task["description"] == "Buy organic groceries"
    assert updated_task["is_completed"] is True

    # Delete Task
    delete_response = client.delete(f"/tasks/{task_id}")
    assert delete_response.status_code == 200
    assert delete_response.json() == {"ok": True}

    # Verify task is deleted
    verify_delete_response = client.get(f"/tasks/{task_id}")
    assert verify_delete_response.status_code == 404
