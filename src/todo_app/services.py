class TodoNotFoundException(Exception):
    """Exception raised when a Todo item is not found."""
    pass

class InvalidInputException(Exception):
    """Exception raised for invalid user input."""
    pass

from typing import List, Optional
from .models import Todo

_todos: List[Todo] = []
_next_id: int = 1

def _get_next_id() -> int:
    global _next_id
    current_id = _next_id
    _next_id += 1
    return current_id

def _reset_state():
    """Resets the internal state of the todo service for testing."""
    global _todos, _next_id
    _todos = []
    _next_id = 1

def add_todo(description: str) -> Todo:
    if not description or not description.strip():
        raise InvalidInputException("Description cannot be empty.")
    
    new_id = _get_next_id()
    todo = Todo(new_id, description)
    _todos.append(todo)
    return todo

def get_all_todos() -> list[Todo]:
    return list(_todos)

def update_todo(todo_id: int, new_description: str) -> Todo:
    if not isinstance(todo_id, int) or todo_id < 1:
        raise InvalidInputException("Todo ID must be a positive integer.")
    if not new_description or not new_description.strip():
        raise InvalidInputException("Description cannot be empty.")

    for todo in _todos:
        if todo.id == todo_id:
            todo.description = new_description.strip()
            return todo
    raise TodoNotFoundException(f"Todo with ID {todo_id} not found.")

def delete_todo(todo_id: int):
    global _todos
    if not isinstance(todo_id, int) or todo_id < 1:
        raise InvalidInputException("Todo ID must be a positive integer.")
    
    initial_len = len(_todos)
    _todos = [todo for todo in _todos if todo.id != todo_id]
    if len(_todos) == initial_len:
        raise TodoNotFoundException(f"Todo with ID {todo_id} not found.")

def mark_todo_completed(todo_id: int) -> Todo:
    if not isinstance(todo_id, int) or todo_id < 1:
        raise InvalidInputException("Todo ID must be a positive integer.")
    
    for todo in _todos:
        if todo.id == todo_id:
            todo.is_completed = True
            return todo
    raise TodoNotFoundException(f"Todo with ID {todo_id} not found.")