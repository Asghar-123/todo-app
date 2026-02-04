import pytest
from src.todo_app import services # Import the services module
from src.todo_app.services import TodoNotFoundException, InvalidInputException # Import exceptions directly
from src.todo_app.models import Todo

# Helper to reset state for isolated tests
@pytest.fixture(autouse=True)
def run_around_tests():
    services._reset_state() # Call the reset function from the services module
    yield

def test_add_todo_valid_description():
    from src.todo_app.services import add_todo
    todo = add_todo("Test todo item")
    assert isinstance(todo, Todo)
    assert todo.id == 1
    assert todo.description == "Test todo item"
    assert todo.is_completed is False
    assert len(services._todos) == 1
    assert services._todos[0] == todo


def test_add_todo_empty_description_raises_exception():
    from src.todo_app.services import add_todo
    with pytest.raises(InvalidInputException, match="Description cannot be empty."):
        add_todo("")
    with pytest.raises(InvalidInputException, match="Description cannot be empty."):
        add_todo("   ")
    assert len(services._todos) == 0 # No todo should be added

def test_get_all_todos_empty_list():
    from src.todo_app.services import get_all_todos
    todos = get_all_todos()
    assert isinstance(todos, list)
    assert len(todos) == 0

def test_get_all_todos_multiple_todos():
    from src.todo_app.services import add_todo, get_all_todos, _todos
    todo1 = services.add_todo("Task 1")
    todo2 = services.add_todo("Task 2")
    todo3 = services.add_todo("Task 3")
    todo3.is_completed = True # Manually mark as completed for test purposes

    todos = services.get_all_todos()
    assert len(todos) == 3
    assert todos[0] == todo1
    assert todos[1] == todo2
    assert todos[2] == todo3

def test_update_todo_valid_description():
    from src.todo_app.services import add_todo, update_todo, get_all_todos
    todo = add_todo("Initial description")
    updated_todo = update_todo(todo.id, "Updated description")
    
    assert updated_todo.id == todo.id
    assert updated_todo.description == "Updated description"
    assert updated_todo.is_completed == todo.is_completed
    
    # Verify the change is reflected in the main list
    all_todos = get_all_todos()
    assert len(all_todos) == 1
    assert all_todos[0] == updated_todo

def test_update_todo_non_existent_id_raises_exception():
    from src.todo_app.services import update_todo
    with pytest.raises(TodoNotFoundException, match="Todo with ID 999 not found."):
        update_todo(999, "New description")

def test_update_todo_empty_description_raises_exception():
    from src.todo_app.services import add_todo, update_todo
    todo = add_todo("Original description")
    with pytest.raises(InvalidInputException, match="Description cannot be empty."):
        update_todo(todo.id, "")
    with pytest.raises(InvalidInputException, match="Description cannot be empty."):
        update_todo(todo.id, "   ")

def test_delete_todo_valid_id():
    from src.todo_app.services import add_todo, delete_todo, get_all_todos
    todo1 = add_todo("Task to delete")
    todo2 = add_todo("Another task")
    
    delete_todo(todo1.id)
    
    all_todos = get_all_todos()
    assert len(all_todos) == 1
    assert all_todos[0] == todo2

def test_delete_todo_non_existent_id_raises_exception():
    from src.todo_app.services import delete_todo
    with pytest.raises(TodoNotFoundException, match="Todo with ID 999 not found."):
        delete_todo(999)

def test_mark_todo_completed_valid_id():
    from src.todo_app.services import add_todo, mark_todo_completed, get_all_todos
    todo = add_todo("Task to complete")
    assert todo.is_completed is False

    completed_todo = mark_todo_completed(todo.id)
    assert completed_todo.is_completed is True
    assert completed_todo.id == todo.id
    assert completed_todo.description == todo.description

    # Verify the change is reflected in the main list
    all_todos = get_all_todos()
    assert all_todos[0].is_completed is True

def test_mark_todo_completed_non_existent_id_raises_exception():
    from src.todo_app.services import mark_todo_completed
    with pytest.raises(TodoNotFoundException, match="Todo with ID 999 not found."):
        mark_todo_completed(999)










    
