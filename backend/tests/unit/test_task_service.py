from unittest.mock import MagicMock, patch
from typing import List
import pytest
from sqlmodel import Session, select
from backend.app.services.task_service import TaskService
from backend.app.models.task import Task, TaskCreate, TaskUpdate
from fastapi import HTTPException # Import HTTPException for testing
from datetime import date # Import date for due_date filtering

# Fixture for a mock database session
@pytest.fixture
def mock_session():
    return MagicMock(spec=Session)

# Helper for creating a mock Query object that allows chaining
@pytest.fixture
def mock_exec_result():
    mock = MagicMock()
    mock.all.return_value = [] # Default empty list
    return mock

@pytest.fixture
def mock_select_query(mock_exec_result):
    mock = MagicMock()
    mock.offset.return_value = mock
    mock.limit.return_value = mock
    mock.where.return_value = mock
    mock.all.return_value = mock_exec_result.all.return_value
    return mock

# Test for create_task method
def test_create_task(mock_session):
    service = TaskService(mock_session)
    task_create = TaskCreate(description="Test Task", is_completed=False, due_date=None)
    
    mock_session.add.return_value = None
    mock_session.commit.return_value = None
    mock_session.refresh.side_effect = lambda x: None

    created_task = service.create_task(task_create)

    mock_session.add.assert_called_once()
    mock_session.commit.assert_called_once()
    mock_session.refresh.assert_called_once_with(created_task)

    assert created_task.description == "Test Task"
    assert created_task.is_completed is False
    assert created_task.id is None

# Test for get_tasks method (no filters)
def test_get_tasks(mock_session, mock_exec_result, mock_select_query):
    service = TaskService(mock_session)
    
    dummy_tasks = [
        Task(id=1, description="Task 1", is_completed=False),
        Task(id=2, description="Task 2", is_completed=True),
    ]
    
    mock_exec_result.all.return_value = dummy_tasks
    mock_session.exec.return_value = mock_exec_result # exec returns a result object
    
    # Mock the select(Task) to return our chainable mock_select_query
    with patch('backend.app.services.task_service.select', return_value=mock_select_query) as mock_select:
        tasks = service.get_tasks(skip=0, limit=10)

        mock_select.assert_called_once_with(Task)
        mock_select_query.offset.assert_called_once_with(0)
        mock_select_query.limit.assert_called_once_with(10)
        mock_exec_result.all.assert_called_once()
        
        assert len(tasks) == 2
        assert tasks[0].description == "Task 1"

# Test get_tasks with is_completed filter
def test_get_tasks_filter_completed(mock_session, mock_exec_result, mock_select_query):
    service = TaskService(mock_session)
    
    dummy_tasks = [
        Task(id=2, description="Task 2", is_completed=True),
    ]
    
    mock_exec_result.all.return_value = dummy_tasks
    mock_session.exec.return_value = mock_exec_result

    with patch('backend.app.services.task_service.select', return_value=mock_select_query) as mock_select:
        tasks = service.get_tasks(is_completed=True)
        
        mock_select.assert_called_once_with(Task)
        mock_select_query.where.assert_called_once()
        # You can inspect the call args of where if needed, e.g., mock_select_query.where.call_args[0][0]
        # For a simple check, we can assume where was called and then all() was called
        mock_exec_result.all.assert_called_once()
        
        assert len(tasks) == 1
        assert tasks[0].is_completed is True

# Test get_tasks with due_date filter
def test_get_tasks_filter_due_date(mock_session, mock_exec_result, mock_select_query):
    service = TaskService(mock_session)
    
    test_date = date(2026, 2, 9)
    dummy_tasks = [
        Task(id=3, description="Task 3", due_date=test_date, is_completed=False),
    ]
    
    mock_exec_result.all.return_value = dummy_tasks
    mock_session.exec.return_value = mock_exec_result

    with patch('backend.app.services.task_service.select', return_value=mock_select_query) as mock_select:
        tasks = service.get_tasks(due_date=test_date)
        
        mock_select.assert_called_once_with(Task)
        mock_select_query.where.assert_called_once()
        # Check that where was called with a condition related to due_date
        # We can be more specific here if needed, but for now, checking it's called is sufficient
        mock_exec_result.all.assert_called_once()
        
        assert len(tasks) == 1
        assert tasks[0].due_date == test_date

# Test get_tasks with no tasks
def test_get_tasks_no_tasks(mock_session, mock_exec_result, mock_select_query):
    service = TaskService(mock_session)
    
    mock_exec_result.all.return_value = []
    mock_session.exec.return_value = mock_exec_result

    with patch('backend.app.services.task_service.select', return_value=mock_select_query) as mock_select:
        tasks = service.get_tasks()
        mock_select.assert_called_once_with(Task)
        mock_exec_result.all.assert_called_once()
        assert len(tasks) == 0

# Test for mark_task_status method
def test_mark_task_status(mock_session):
    service = TaskService(mock_session)
    existing_task = Task(id=1, description="Existing Task", is_completed=False)
    
    # Mock session.get to return an existing task
    mock_session.get.return_value = existing_task
    
    mock_session.add.return_value = None
    mock_session.commit.return_value = None
    mock_session.refresh.side_effect = lambda x: None

    updated_task = service.mark_task_status(task_id=1, is_completed=True)

    mock_session.get.assert_called_once_with(Task, 1)
    mock_session.add.assert_called_once_with(existing_task)
    mock_session.commit.assert_called_once()
    mock_session.refresh.assert_called_once_with(existing_task)
    assert updated_task.is_completed is True

# Test mark_task_status with task not found
def test_mark_task_status_not_found(mock_session):
    service = TaskService(mock_session)
    mock_session.get.return_value = None # Simulate task not found
    
    with pytest.raises(HTTPException) as exc_info:
        service.mark_task_status(task_id=999, is_completed=True)
    
    assert exc_info.value.status_code == 404
    assert exc_info.value.detail == "Task not found"
    mock_session.get.assert_called_once_with(Task, 999)
    mock_session.add.assert_not_called()
    mock_session.commit.assert_not_called()

# Test for update_task method
def test_update_task(mock_session):
    service = TaskService(mock_session)
    existing_task = Task(id=1, description="Original Description", is_completed=False)
    task_update = TaskUpdate(description="Updated Description")

    mock_session.get.return_value = existing_task
    
    updated_task = service.update_task(task_id=1, task_update=task_update)
    
    mock_session.get.assert_called_once_with(Task, 1)
    mock_session.add.assert_called_once_with(existing_task)
    mock_session.commit.assert_called_once()
    mock_session.refresh.assert_called_once_with(existing_task)
    assert updated_task.description == "Updated Description"

# Test update_task with task not found
def test_update_task_not_found(mock_session):
    service = TaskService(mock_session)
    task_update = TaskUpdate(description="This should fail")
    mock_session.get.return_value = None

    with pytest.raises(HTTPException) as exc_info:
        service.update_task(task_id=999, task_update=task_update)
        
    assert exc_info.value.status_code == 404
    assert exc_info.value.detail == "Task not found"

# Test for delete_task method
def test_delete_task(mock_session):
    service = TaskService(mock_session)
    existing_task = Task(id=1, description="Task to be deleted", is_completed=False)
    
    mock_session.get.return_value = existing_task
    
    result = service.delete_task(task_id=1)
    
    mock_session.get.assert_called_once_with(Task, 1)
    mock_session.delete.assert_called_once_with(existing_task)
    mock_session.commit.assert_called_once()
    assert result == {"ok": True}

# Test delete_task with task not found
def test_delete_task_not_found(mock_session):
    service = TaskService(mock_session)
    mock_session.get.return_value = None

    with pytest.raises(HTTPException) as exc_info:
        service.delete_task(task_id=999)
        
    assert exc_info.value.status_code == 404
    assert exc_info.value.detail == "Task not found"
