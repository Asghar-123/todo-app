# Tasks: In-Memory Python Console Todo App

**Input**: Design documents from `/specs/001-in-memory-todo-app/`
**Prerequisites**: plan.md (required), spec.md (required for user stories)

**Tests**: The spec requests validation of CRUD operations, completion status, invalid inputs, edge cases, data resets on exit, and clear console outputs. Therefore, tests will be included.

**Organization**: Tasks are grouped by user story to enable independent implementation and testing of each story.

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Which user story this task belongs to (e.g., US1, US2, US3)
- Include exact file paths in descriptions

## Path Conventions

- **Single project**: `src/`, `tests/` at repository root

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Project initialization and basic structure

- [X] T001 Create `src/todo_app/` directory and `__init__.py` in `src/todo_app/`
- [X] T002 Create `tests/unit/` and `tests/integration/` directories in `tests/`

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Core infrastructure that MUST be complete before ANY user story can be implemented

**⚠️ CRITICAL**: No user story work can begin until this phase is complete

- [X] T003 Create `src/todo_app/models.py` for the `Todo` class
- [X] T004 Implement `Todo` class in `src/todo_app/models.py` with `id`, `description`, `is_completed` attributes, and a constructor.
- [X] T005 Create `src/todo_app/services.py` for business logic functions.
- [X] T006 Implement in-memory storage (e.g., a list for `Todo` objects) in `src/todo_app/services.py`.
- [X] T007 Implement `TodoNotFoundException` and `InvalidInputException` in `src/todo_app/services.py`.
- [X] T008 Create `src/todo_app/main.py` for the CLI entry point.
- [X] T009 Create `tests/unit/test_models.py` for unit tests of the `Todo` model.
- [X] T010 Implement unit tests for `Todo` class instantiation and attribute access in `tests/unit/test_models.py`.

**Checkpoint**: Foundation ready - user story implementation can now begin in parallel

---

## Phase 3: User Story 1 - Add Todo (Priority: P1) 🎯 MVP

**Goal**: Users can add new todo items to their list.

**Independent Test**: Can be fully tested by adding a todo and then viewing the list to confirm its presence.

### Tests for User Story 1 (OPTIONAL - only if tests requested) ⚠️

> **NOTE: Write these tests FIRST, ensure they FAIL before implementation**

- [X] T011 [P] [US1] Unit test `add_todo` with a valid description in `tests/unit/test_services.py`.
- [X] T012 [P] [US1] Unit test `add_todo` with an empty description (should raise `InvalidInputException`) in `tests/unit/test_services.py`.

### Implementation for User Story 1

- [X] T013 [US1] Implement `add_todo(description: str) -> Todo` function in `src/todo_app/services.py` that generates a unique ID, creates a `Todo` object, and adds it to the in-memory list.
- [X] T014 [US1] Integrate `add_todo` into `src/todo_app/main.py` CLI, including prompting for description and displaying success/error messages.

**Checkpoint**: At this point, User Story 1 should be fully functional and testable independently

---

## Phase 4: User Story 2 - View Todos (Priority: P1)

**Goal**: Users can view all their current todo items, including their status.

**Independent Test**: Can be fully tested by adding multiple todos and then displaying the list to verify all are shown with correct details.

### Tests for User Story 2 (OPTIONAL - only if tests requested) ⚠️

- [X] T015 [P] [US2] Unit test `get_all_todos()` with an empty list in `tests/unit/test_services.py`.
- [X] T016 [P] [US2] Unit test `get_all_todos()` with multiple todos (pending and completed) in `tests/unit/test_services.py`.

### Implementation for User Story 2

- [X] T017 [US2] Implement `get_all_todos() -> list[Todo]` function in `src/todo_app/services.py` that returns all current todo items.
- [X] T018 [US2] Integrate `get_all_todos` into `src/todo_app/main.py` CLI, including formatting and displaying the todo list (with IDs, descriptions, and status).

**Checkpoint**: At this point, User Stories 1 AND 2 should both work independently

---

## Phase 5: User Story 3 - Update Todo (Priority: P2)

**Goal**: Users can modify the description of an existing todo item.

**Independent Test**: Can be fully tested by adding a todo, updating its description, and then viewing the list to confirm the change.

### Tests for User Story 3 (OPTIONAL - only if tests requested) ⚠️

- [X] T019 [P] [US3] Unit test `update_todo` with a valid ID and new description in `tests/unit/test_services.py`.
- [X] T020 [P] [US3] Unit test `update_todo` with a non-existent ID (should raise `TodoNotFoundException`) in `tests/unit/test_services.py`.
- [X] T021 [P] [US3] Unit test `update_todo` with an empty new description (should raise `InvalidInputException`) in `tests/unit/test_services.py`.

### Implementation for User Story 3

- [X] T022 [US3] Implement `update_todo(todo_id: int, new_description: str) -> Todo` function in `src/todo_app/services.py` that finds and updates a todo item by ID.
- [X] T023 [US3] Integrate `update_todo` into `src/todo_app/main.py` CLI, including prompting for ID and new description, and handling success/error messages.

**Checkpoint**: All user stories should now be independently functional

---

## Phase 6: User Story 4 - Delete Todo (Priority: P2)

**Goal**: Users can remove todo items from their list.

**Independent Test**: Can be fully tested by adding a todo, deleting it, and then viewing the list to confirm its removal.

### Tests for User Story 4 (OPTIONAL - only if tests requested) ⚠️

- [X] T024 [P] [US4] Unit test `delete_todo` with a valid ID in `tests/unit/test_services.py`.
- [X] T025 [P] [US4] Unit test `delete_todo` with a non-existent ID (should raise `TodoNotFoundException`) in `tests/unit/test_services.py`.

### Implementation for User Story 4

- [X] T026 [US4] Implement `delete_todo(todo_id: int)` function in `src/todo_app/services.py` that finds and removes a todo item by ID.
- [X] T027 [US4] Integrate `delete_todo` into `src/todo_app/main.py` CLI, including prompting for ID and handling success/error messages.

---

## Phase 7: User Story 5 - Mark Todo as Completed (Priority: P2)

**Goal**: Users can mark a todo item as completed.

**Independent Test**: Can be fully tested by adding a todo, marking it as complete, and then viewing the list to confirm its status change.

### Tests for User Story 5 (OPTIONAL - only if tests requested) ⚠️

- [X] T028 [P] [US5] Unit test `mark_todo_completed` with a valid ID in `tests/unit/test_services.py`.
- [X] T029 [P] [US5] Unit test `mark_todo_completed` with a non-existent ID (should raise `TodoNotFoundException`) in `tests/unit/test_services.py`.

### Implementation for User Story 5

- [X] T030 [US5] Implement `mark_todo_completed(todo_id: int) -> Todo` function in `src/todo_app/services.py` that finds and updates the completion status of a todo item by ID.
- [X] T031 [US5] Integrate `mark_todo_completed` into `src/todo_app/main.py` CLI, including prompting for ID and handling success/error messages.

---

## Phase N: Polish & Cross-Cutting Concerns

**Purpose**: Improvements that affect multiple user stories

- [ ] T032 Add a main application loop to `src/todo_app/main.py` that presents a menu and handles user choices (Add, View, Update, Delete, Mark Completed, Exit).
- [ ] T033 Implement robust input parsing and validation for all CLI commands in `src/todo_app/main.py` (e.g., handling non-integer input for IDs, out-of-bounds IDs).
- [X] T034 Write integration tests for `src/todo_app/main.py` in `tests/integration/test_cli.py` to cover end-to-end user flows.

---

## Dependencies & Execution Order

### Phase Dependencies

- **Setup (Phase 1)**: No dependencies - can start immediately
- **Foundational (Phase 2)**: Depends on Setup completion - BLOCKS all user stories
- **User Stories (Phase 3+)**: All depend on Foundational phase completion
  - User stories can then proceed in parallel (if staffed)
  - Or sequentially in priority order (P1 → P2 → P3)
- **Polish (Final Phase)**: Depends on all desired user stories being complete

### User Story Dependencies

- **User Story 1 (P1)**: Can start after Foundational (Phase 2) - No dependencies on other stories
- **User Story 2 (P1)**: Can start after Foundational (Phase 2) - May integrate with US1 but should be independently testable
- **User Story 3 (P2)**: Can start after Foundational (Phase 2) - May integrate with US1/US2 but should be independently testable
- **User Story 4 (P2)**: Can start after Foundational (Phase 2) - May integrate with US1/US2/US3 but should be independently testable
- **User Story 5 (P2)**: Can start after Foundational (Phase 2) - May integrate with US1/US2/US3/US4 but should be independently testable

### Within Each User Story

- Tests (if included) MUST be written and FAIL before implementation
- Models before services
- Services before CLI integration
- Core implementation before integration
- Story complete before moving to next priority

### Parallel Opportunities

- Setup tasks marked [P] can run in parallel (T001, T002)
- Foundational tests (T009, T010) can run in parallel
- Once Foundational phase completes, all user stories can start in parallel (if team capacity allows)
- Within each User Story, test tasks marked [P] can run in parallel.
- Within each User Story, model and service tasks can run in parallel if they operate on different files.

---

## Parallel Example: User Story 1

```bash
# Launch all tests for User Story 1 together (if tests requested):
Task: "Unit test `add_todo` with a valid description in `tests/unit/test_services.py`"
Task: "Unit test `add_todo` with an empty description (should raise `InvalidInputException`) in `tests/unit/test_services.py`"

# Launch implementation tasks for User Story 1 (if independent):
Task: "Implement `add_todo(description: str) -> Todo` function in `src/todo_app/services.py`"
```

---

## Implementation Strategy

### MVP First (User Story 1 & 2 Only)

1. Complete Phase 1: Setup
2. Complete Phase 2: Foundational (CRITICAL - blocks all stories)
3. Complete Phase 3: User Story 1 (Add Todo)
4. Complete Phase 4: User Story 2 (View Todos)
5. **STOP and VALIDATE**: Test User Stories 1 and 2 independently.
6. Deploy/demo if ready

### Incremental Delivery

1. Complete Setup + Foundational → Foundation ready
2. Add User Story 1 (Add Todo) → Test independently → Deploy/Demo (MVP!)
3. Add User Story 2 (View Todos) → Test independently → Deploy/Demo
4. Add User Story 3 (Update Todo) → Test independently → Deploy/Demo
5. Add User Story 4 (Delete Todo) → Test independently → Deploy/Demo
6. Add User Story 5 (Mark Todo as Completed) → Test independently → Deploy/Demo
7. Each story adds value without breaking previous stories

### Parallel Team Strategy

With multiple developers:

1. Team completes Setup + Foundational together
2. Once Foundational is done:
   - Developer A: User Story 1 (Add Todo)
   - Developer B: User Story 2 (View Todos)
   - Developer C: User Story 3 (Update Todo)
   - Developer D: User Story 4 (Delete Todo)
   - Developer E: User Story 5 (Mark Todo as Completed)
3. Stories complete and integrate independently

---

## Notes

- [P] tasks = different files, no dependencies
- [Story] label maps task to specific user story for traceability
- Each user story should be independently completable and testable
- Verify tests fail before implementing
- Commit after each task or logical group
- Stop at any checkpoint to validate story independently
- Avoid: vague tasks, same file conflicts, cross-story dependencies that break independence
