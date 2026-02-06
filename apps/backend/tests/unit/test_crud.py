from sqlmodel import Session
from apps.backend.src.models.task import Task, TaskCreate, TaskUpdate
from apps.backend.src.api.tasks import (
    create_task,
    read_tasks,
    read_task,
    update_task,
    delete_task,
)
from fastapi import HTTPException
import pytest

# Test for creating a task (T026)
def test_create_task(session: Session):
    task_create = TaskCreate(description="Test Task")
    task = create_task(task_create, session)
    assert task.description == "Test Task"
    assert task.is_completed is False
    assert task.id is not None

# Test for reading tasks (T027)
def test_read_tasks(session: Session):
    task_create1 = TaskCreate(description="Task 1")
    task_create2 = TaskCreate(description="Task 2")
    create_task(task_create1, session)
    create_task(task_create2, session)

    tasks = read_tasks(session)
    assert len(tasks) == 2
    assert tasks[0].description == "Task 1"
    assert tasks[1].description == "Task 2"

# Test for reading a single task (T027)
def test_read_single_task(session: Session):
    task_create = TaskCreate(description="Single Task")
    created_task = create_task(task_create, session)

    found_task = read_task(created_task.id, session)
    assert found_task.description == "Single Task"

# Test for updating a task (T028)
def test_update_task(session: Session):
    task_create = TaskCreate(description="Task to Update")
    created_task = create_task(task_create, session)

    task_update_data = TaskUpdate(description="Updated Task", is_completed=True)
    updated_task = update_task(created_task.id, task_update_data, session)
    assert updated_task.description == "Updated Task"
    assert updated_task.is_completed is True

# Test for deleting a task (T029)
def test_delete_task(session: Session):
    task_create = TaskCreate(description="Task to Delete")
    created_task = create_task(task_create, session)

    response = delete_task(created_task.id, session)
    assert response == {"ok": True}

    # Verify task is deleted
    with pytest.raises(HTTPException) as excinfo:
        read_task(created_task.id, session)
    assert excinfo.value.status_code == 404
