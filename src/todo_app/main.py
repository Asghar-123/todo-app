from .services import add_todo, get_all_todos, update_todo, delete_todo, mark_todo_completed, InvalidInputException, TodoNotFoundException
from .models import Todo

def display_todos(todos: list[Todo]):
    if not todos:
        print("No todo items found.")
        return

    print("\n--- Your Todo List ---")
    for todo in todos:
        status = "[X]" if todo.is_completed else "[ ]"
        print(f"{status} {todo.id}: {todo.description}")
    print("----------------------")

def main():
    print("Welcome to the Todo App!")
    while True:
        print("\n--- Menu ---")
        print("1. Add Todo")
        print("2. View Todos")
        print("3. Update Todo")
        print("4. Delete Todo")
        print("5. Mark Todo as Completed")
        print("0. Exit")
        choice = input("Enter your choice: ").strip()

        if choice == '1':
            description = input("Enter todo description: ").strip()
            try:
                todo = add_todo(description)
                print(f"Todo added: ID {todo.id}, Description: {todo.description}")
            except InvalidInputException as e:
                print(f"Error: {e}")
        elif choice == '2':
            todos = get_all_todos()
            display_todos(todos)
        elif choice == '3':
            try:
                todo_id = int(input("Enter the ID of the todo to update: ").strip())
                new_description = input("Enter new description: ").strip()
                updated_todo = update_todo(todo_id, new_description)
                print(f"Todo ID {updated_todo.id} updated to: {updated_todo.description}")
            except ValueError:
                print("Error: Invalid ID. Please enter a number.")
            except (InvalidInputException, TodoNotFoundException) as e:
                print(f"Error: {e}")
        elif choice == '4':
            try:
                todo_id = int(input("Enter the ID of the todo to delete: ").strip())
                delete_todo(todo_id)
                print(f"Todo ID {todo_id} deleted successfully.")
            except ValueError:
                print("Error: Invalid ID. Please enter a number.")
            except TodoNotFoundException as e:
                print(f"Error: {e}")
        elif choice == '5':
            try:
                todo_id = int(input("Enter the ID of the todo to mark as completed: ").strip())
                completed_todo = mark_todo_completed(todo_id)
                print(f"Todo ID {completed_todo.id} marked as completed.")
            except ValueError:
                print("Error: Invalid ID. Please enter a number.")
            except TodoNotFoundException as e:
                print(f"Error: {e}")
        elif choice == '0':
            print("Exiting Todo App. Goodbye!")
            break
        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main()
