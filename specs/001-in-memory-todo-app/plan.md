# Implementation Plan: In-Memory Python Console Todo App

**Branch**: `001-in-memory-todo-app` | **Date**: 2026-02-04 | **Spec**: specs/001-in-memory-todo-app/spec.md
**Input**: Feature specification from `/specs/001-in-memory-todo-app/spec.md`

**Note**: This template is filled in by the `/sp.plan` command. See `.specify/templates/commands/plan.md` for the execution workflow.

## Summary

This plan outlines the architecture and implementation strategy for a command-line todo application in Python. The application will manage todo tasks entirely in memory, supporting add, view, update, delete, and mark as completed functionalities. It aims to demonstrate spec-driven, agentic development using Claude Code and Spec-Kit Plus.

## Technical Context

**Language/Version**: Python 3.11+
**Primary Dependencies**: Python standard library only
**Storage**: In-memory data structures (list/dict/class)
**Testing**: Validate each CRUD operation, completion status, invalid inputs, edge cases, data resets on exit, and clear console outputs.
**Target Platform**: Command-line interface (console-based interaction)
**Project Type**: Single project (console application)
**Performance Goals**: Responsive console interaction for a small number of in-memory tasks.
**Constraints**: Python 3.11+, UV for environment management, Python standard library only, in-memory data structures, no manual coding.
**Scale/Scope**: Single-user, in-memory todo list with basic CRUD operations. No persistence, no advanced features.

## Constitution Check

Refer to `.specify/memory/constitution.md` for general project principles. No specific violations or justifications are required for this project phase.

## Project Structure

### Documentation (this feature)

```text
specs/001-in-memory-todo-app/
├── plan.md              # This file (/sp.plan command output)
├── research.md          # Phase 0 output (/sp.plan command)
├── data-model.md        # Phase 1 output (/sp.plan command)
├── quickstart.md        # Phase 1 output (/sp.plan command)
├── contracts/           # Phase 1 output (/sp.plan command)
└── tasks.md             # Phase 2 output (/sp.tasks command - NOT created by /sp.plan)
```

### Source Code (repository root)

```text
src/
├── todo_app/
│   ├── __init__.py
│   ├── main.py          # CLI entry point, handles user input and output
│   ├── models.py        # Defines the Todo data model
│   └── services.py      # Contains business logic for Todo operations
└── tests/
    ├── unit/
    │   ├── test_models.py
    │   └── test_services.py
    └── integration/
        └── test_cli.py
```

**Structure Decision**: A single project structure is chosen, with a `src/todo_app` directory for the main application, separated into `main.py` (CLI), `models.py` (data model), and `services.py` (business logic). A `tests/` directory is included for unit and integration tests.

## Key Decisions and Rationale

### Todo Storage Structure (list vs dict vs class objects)
- **Options Considered**:
    - **List of dictionaries**: Simple to implement, but lacks type safety and easy attribute access.
    - **List of class objects**: Provides type safety, object-oriented encapsulation, and clearer attribute access. More scalable for future enhancements.
    - **Dictionary mapping IDs to class objects**: Offers efficient lookup by ID, combining benefits of dictionaries and class objects.
- **Rationale**: A **list of class objects** will be used for initial implementation simplicity, providing a good balance of structure and ease of use for an in-memory application. Each `Todo` object will encapsulate its `id`, `description`, and `is_completed` status. This choice also allows for easy iteration and maintains insertion order implicitly. For performance, if the number of todos becomes very large, a dictionary mapping IDs to objects could be considered for faster updates/deletions, but for a simple in-memory app, a list is sufficient.

### Unique Task Identification Method
- **Options Considered**:
    - **Sequential integer ID**: Simple, easy to understand and use in a console.
    - **UUID**: Globally unique, but longer and less user-friendly for console input.
- **Rationale**: **Sequential integer IDs** will be used. This is simpler for console interaction, as users can easily refer to tasks by their index in the displayed list. A counter will be maintained to generate unique IDs.

### Input Validation Strategy
- **Options Considered**:
    - **Basic type checks and boundary checks at point of input**: Simple and direct validation.
    - **Dedicated validation layer/functions**: More robust, reusable validation logic.
- **Rationale**: **Basic type checks and boundary checks will be performed at the point of input in the CLI layer.** For instance, checking if a provided ID is a valid integer and within the bounds of the current todo list. This keeps validation close to user interaction and is sufficient for a console application.

### Separation between UI and Logic Layers
- **Options Considered**:
    - **Tight coupling**: UI and logic mixed in `main.py`.
    - **Clear separation**: Dedicated `main.py` for CLI/UI and `services.py` for business logic.
- **Rationale**: A **clear separation** will be enforced. `main.py` will handle all user input, output formatting, and menu navigation. `services.py` will contain the core business logic for managing the todo list (add, view, update, delete, mark completed) without any direct interaction with `stdin`/`stdout`. This promotes modularity and testability.

### Error Handling Approach
- **Options Considered**:
    - **Return error codes/boolean flags**: Simple, but requires caller to constantly check.
    - **Raise exceptions**: Pythonic, allows for cleaner error propagation and handling at appropriate levels.
- **Rationale**: **Exceptions will be raised** for error conditions (e.g., `TodoNotFoundException`, `InvalidInputException`). The `main.py` (CLI layer) will catch these exceptions and display user-friendly error messages. This approach is more robust and cleaner for separating error detection from error reporting.

## User Interaction Flow

1.  **Main Menu**: Display options (Add, View, Update, Delete, Mark Completed, Exit).
2.  **Input**: Prompt user for choice (e.g., `1` for Add, `q` for Quit).
3.  **Command Handling**:
    -   **Add**: Prompt for todo description. Add to list. Display success/error.
    -   **View**: Display all todos with IDs, descriptions, and status. Handle empty list.
    -   **Update**: Prompt for todo ID and new description. Update todo. Display success/error.
    -   **Delete**: Prompt for todo ID. Delete todo. Display success/error.
    -   **Mark Completed**: Prompt for todo ID. Mark todo as completed. Display success/error.
    -   **Exit**: Terminate application.
4.  **Error Messages**: Display clear, user-friendly messages for invalid choices, non-existent IDs, empty descriptions, etc.

## Implementation Task Grouping

-   **Phase 1: Setup and Data Model**
    -   Initialize project structure.
    -   Define `Todo` class (ID, description, is_completed).
    -   Implement initial in-memory storage (e.g., a list to hold Todo objects).

-   **Phase 2: Core Logic (services.py)**
    -   Implement `add_todo` function.
    -   Implement `get_all_todos` function.
    -   Implement `update_todo` function.
    -   Implement `delete_todo` function.
    -   Implement `mark_todo_completed` function.

-   **Phase 3: Command-Line Interface (main.py)**
    -   Implement main application loop and menu display.
    -   Implement user input handling and command parsing.
    -   Integrate with `services.py` functions.
    -   Implement error message display.

-   **Phase 4: Testing**
    -   Write unit tests for `models.py`.
    -   Write unit tests for `services.py`.
    -   Write integration tests for `main.py` (CLI interaction).

## Evaluation and Validation

**Definition of Done (tests, scans)**:
-   All acceptance scenarios in `specs/001-in-memory-todo-app/spec.md` are covered by automated tests.
-   Unit and integration tests pass successfully.
-   Code adheres to readability and modularity standards (e.g., via static analysis, if external tools were permitted).

**Output Validation for format/requirements/safety**:
-   Console output is clear, consistent, and user-friendly.
-   Application correctly handles invalid inputs and displays appropriate error messages.
-   Data is confirmed to be in-memory and non-persistent across runs.
-   Python standard library only constraint is respected.
