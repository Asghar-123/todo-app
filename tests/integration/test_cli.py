import pytest
from unittest.mock import patch
import io
import sys

from src.todo_app.main import main
from src.todo_app.services import _reset_state # Import for fixture


@pytest.fixture(autouse=True)
def run_around_tests():
    _reset_state() # Reset service state before each test
    yield


def test_cli_add_and_view_todo():
    # Simulate user input: 1 (Add), "My new todo", 2 (View), 0 (Exit)
    user_inputs = ["1", "My new todo", "2", "0"]
    
    with patch("builtins.input", side_effect=user_inputs):
        captured_output = io.StringIO()
        sys.stdout = captured_output
        
        main() # Run the main CLI application
        
        sys.stdout = sys.__stdout__ # Restore stdout
        
        output = captured_output.getvalue()
        
        assert "Welcome to the Todo App!" in output
        assert "Todo added: ID 1, Description: My new todo" in output
        assert "[ ] 1: My new todo" in output
        assert "Exiting Todo App. Goodbye!" in output


def test_cli_full_crud_workflow():
    # Simulate user input for a full CRUD workflow
    user_inputs = [
        "1", "Task one",  # Add Task 1
        "1", "Task two",  # Add Task 2
        "2",             # View Todos
        "3", "1", "Updated task one", # Update Task 1
        "2",             # View Todos
        "5", "2",        # Mark Task 2 as completed
        "2",             # View Todos
        "4", "1",        # Delete Task 1
        "2",             # View Todos
        "0"              # Exit
    ]

    with patch("builtins.input", side_effect=user_inputs):
        captured_output = io.StringIO()
        sys.stdout = captured_output
        
        main()
        
        sys.stdout = sys.__stdout__
        
        output = captured_output.getvalue()

        # Assertions for Add
        assert "Todo added: ID 1, Description: Task one" in output
        assert "Todo added: ID 2, Description: Task two" in output
        
        # Assertions for initial View
        assert "[ ] 1: Task one" in output
        assert "[ ] 2: Task two" in output

        # Assertions for Update
        assert "Todo ID 1 updated to: Updated task one" in output
        
        # Assertions for View after Update
        assert "[ ] 1: Updated task one" in output
        assert "[ ] 2: Task two" in output

        # Assertions for Mark Completed
        assert "Todo ID 2 marked as completed." in output

        # Assertions for View after Mark Completed
        assert "[ ] 1: Updated task one" in output
        assert "[X] 2: Task two" in output

        # Assertions for Delete
        assert "Todo ID 1 deleted successfully." in output

        # Assertions for View after Delete
        assert "No todo items found." not in output # Should still show Task 2
        assert "[X] 2: Task two" in output

        # Assertions for Exit
        assert "Exiting Todo App. Goodbye!" in output

