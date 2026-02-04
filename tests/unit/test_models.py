import pytest
from src.todo_app.models import Todo

def test_todo_creation_valid_data():
    todo = Todo(1, "Learn Python", False)
    assert todo.id == 1
    assert todo.description == "Learn Python"
    assert todo.is_completed is False

def test_todo_creation_strip_description():
    todo = Todo(2, "  Buy Groceries  ", True)
    assert todo.description == "Buy Groceries"

def test_todo_id_must_be_non_negative_integer():
    with pytest.raises(ValueError, match="Todo ID must be a non-negative integer."):
        Todo(-1, "Invalid ID Todo")
    with pytest.raises(ValueError, match="Todo ID must be a non-negative integer."):
        Todo("abc", "Invalid ID Type Todo")

def test_todo_description_cannot_be_empty():
    with pytest.raises(ValueError, match="Todo description cannot be empty."):
        Todo(3, "")
    with pytest.raises(ValueError, match="Todo description cannot be empty."):
        Todo(4, "   ")

def test_todo_is_completed_must_be_boolean():
    with pytest.raises(ValueError, match="Todo is_completed status must be a boolean."):
        Todo(5, "Invalid completion status", "True")
    with pytest.raises(ValueError, match="Todo is_completed status must be a boolean."):
        Todo(6, "Invalid completion status", 1)

def test_todo_equality():
    todo1 = Todo(1, "Task 1", False)
    todo2 = Todo(1, "Task 1", False)
    todo3 = Todo(2, "Task 2", True)
    todo4 = Todo(1, "Task 1", True)

    assert todo1 == todo2
    assert todo1 != todo3
    assert todo1 != todo4

def test_todo_representation():
    todo = Todo(1, "Sample Task", False)
    assert repr(todo) == "Todo(id=1, description='Sample Task', is_completed=False)"
