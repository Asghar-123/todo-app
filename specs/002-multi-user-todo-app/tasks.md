# Tasks: Full-Stack Multi-User Todo Web Application

**Input**: Design documents from `specs/002-multi-user-todo-app/`
**Prerequisites**: plan.md (required), spec.md (required for user stories)

**Tests**: The spec and plan request validation of authentication flow, CRUD operations, user task isolation, invalid token/unauthorized access, database persistence, and responsive UI behavior. Therefore, tests will be included.

**Organization**: Tasks are grouped by user story to enable independent implementation and testing of each story.

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Which user story this task belongs to (e.g., US1, US2, US3)
- Include exact file paths in descriptions

## Path Conventions

- **Monorepo**: `apps/frontend/`, `apps/backend/`, `packages/types/`

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Project initialization and basic monorepo structure.

- [X] T001 Create `apps/` and `packages/` directories in the repository root.
- [X] T002 Create `apps/frontend/` directory and initialize a Next.js project inside it.
- [X] T003 Create `apps/backend/` directory and initialize a FastAPI project inside it.
- [X] T004 Create `packages/types/` directory for shared TypeScript/Python types.
- [X] T005 Set up basic monorepo configuration (e.g., `package.json` workspaces or `pnpm-workspace.yaml`).

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Core infrastructure that MUST be complete before ANY user story can be implemented.

**⚠️ CRITICAL**: No user story work can begin until this phase is complete.

- [X] T006 [P] Create `apps/backend/src/models/user.py` for the `User` SQLModel, including `id`, `username`, `hashed_password` attributes.
- [X] T007 [P] Create `apps/backend/src/models/task.py` for the `Task` SQLModel, including `id`, `description`, `is_completed`, `owner_id` (foreign key to User) attributes.
- [X] T008 [P] Implement password hashing utility in `apps/backend/src/auth/utils.py` (e.g., using `passlib`).
- [X] T009 [P] Implement JWT token creation and validation utilities in `apps/backend/src/auth/jwt.py` (using `python-jose`).
- [X] T010 Setup database connection in `apps/backend/src/database.py` using `SQLModel` and `Neon PostgreSQL` connection string from environment variables.
- [X] T011 Implement `main.py` in `apps/backend/src/main.py` to include database connection and basic FastAPI app setup.
- [X] T012 Configure `alembic` for database migrations in `apps/backend/`.

**Checkpoint**: Foundation ready - user story implementation can now begin in parallel.

---

## Phase 3: User Story 1 - User Authentication (Priority: P1) 🎯 MVP

**Goal**: Users can securely sign up for an account and log in.

**Independent Test**: Can be fully tested by creating a new user and successfully logging in.

### Tests for User Story 1 ⚠️

> **NOTE: Write these tests FIRST, ensure they FAIL before implementation.**

- [X] T013 [P] [US1] Unit test `password_hashing` utility in `apps/backend/tests/unit/test_auth_utils.py`.
- [X] T014 [P] [US1] Unit test `create_access_token` and `verify_token` in `apps/backend/tests/unit/test_auth_jwt.py`.
- [X] T015 [P] [US1] Integration test user signup (valid/invalid credentials) via API in `apps/backend/tests/integration/test_auth.py`.
- [X] T016 [P] [US1] Integration test user login (valid/invalid credentials) via API in `apps/backend/tests/integration/test_auth.py`.

### Implementation for User Story 1

- [X] T017 [US1] Implement user registration API endpoint (`POST /auth/signup`) in `apps/backend/src/api/auth.py`, including password hashing and user creation.
- [X] T018 [US1] Implement user login API endpoint (`POST /auth/login`) in `apps/backend/src/api/auth.py`, including password verification and JWT issuance.
- [X] T019 [US1] Implement `get_current_user` FastAPI dependency in `apps/backend/src/auth/dependencies.py` for JWT validation.
- [X] T020 [US1] Integrate `auth.py` endpoints into `apps/backend/src/main.py`.
- [ ] T023 [US1] Implement frontend API client for authentication in `apps/frontend/src/lib/auth.ts` (handle JWT storage in HTTP-only cookies). (SKIPPED for now)
- [ ] T024 [US1] Implement UI logic for user registration in `apps/frontend/src/app/(auth)/signup/page.tsx`. (SKIPPED for now)
- [ ] T025 [US1] Implement UI logic for user login in `apps/frontend/src/app/(auth)/login/page.tsx`. (SKIPPED for now)

**Checkpoint**: At this point, User Story 1 should be fully functional and testable independently.

---

## Phase 4: User Story 2 - Task Management (CRUD) (Priority: P1)

**Goal**: Authenticated users can create, view, update, and delete their own todo tasks.

**Independent Test**: Can be fully tested by an authenticated user performing all CRUD operations on their tasks, verifying changes persist and are correctly displayed.

### Tests for User Story 2 ⚠️

- [X] T026 [P] [US2] Unit test task creation for an authenticated user in `apps/backend/tests/unit/test_crud.py`.
- [X] T027 [P] [US2] Unit test retrieving tasks for an authenticated user in `apps/backend/tests/unit/test_crud.py`.
- [X] T028 [P] [US2] Unit test updating a task for an authenticated user in `apps/backend/tests/unit/test_crud.py`.
- [X] T029 [P] [US2] Unit test deleting a task for an authenticated user in `apps/backend/tests/unit/test_crud.py`.
- [X] T030 [P] [US2] Integration test end-to-end task CRUD via API in `apps/backend/tests/integration/test_tasks.py`.

### Implementation for User Story 2

- [X] T031 [US2] Implement create task API endpoint (`POST /tasks`) in `apps/backend/src/api/tasks.py`, ensuring `owner_id` is set to the authenticated user's ID.
- [X] T032 [US2] Implement get all tasks API endpoint (`GET /tasks`) in `apps/backend/src/api/tasks.py`, filtering by authenticated user's `owner_id`.
- [X] T033 [US2] Implement get single task API endpoint (`GET /tasks/{task_id}`) in `apps/backend/src/api/tasks.py`, ensuring task belongs to authenticated user.
- [X] T034 [US2] Implement update task API endpoint (`PUT /tasks/{task_id}`) in `apps/backend/src/api/tasks.py`, ensuring task belongs to authenticated user.
- [X] T035 [US2] Implement delete task API endpoint (`DELETE /tasks/{task_id}`) in `apps/backend/src/api/tasks.py`, ensuring task belongs to authenticated user.
- [X] T036 [US2] Integrate `tasks.py` endpoints into `apps/backend/src/main.py`.
- [X] T037 [US2] Create `apps/frontend/src/app/(app)/tasks/page.tsx` for displaying user's tasks.
- [X] T038 [US2] Implement frontend API client for task management in `apps/frontend/src/lib/tasks.ts`.
- [X] T039 [US2] Implement UI logic for displaying and managing tasks in `apps/frontend/src/app/(app)/tasks/page.tsx`.

**Checkpoint**: All user stories 1 AND 2 should now be independently functional.

---

## Phase 5: User Story 3 - Mark Task as Completed (Priority: P2)

**Goal**: Authenticated users can mark their tasks as completed.

**Independent Test**: Can be fully tested by an authenticated user marking a task as complete and verifying its status changes.

### Tests for User Story 3 ⚠️

- [ ] T040 [P] [US3] Unit test marking a task as completed for an authenticated user in `apps/backend/tests/unit/test_crud.py`.

### Implementation for User Story 3

- [X] T041 [US3] Extend update task API endpoint (`PUT /tasks/{task_id}`) in `apps/backend/src/api/tasks.py` to handle `is_completed` status updates.
- [X] T042 [US3] Implement frontend UI to mark a task as completed in `apps/frontend/src/app/(app)/tasks/page.tsx`.

---

## Phase 6: User Story 4 - Multi-User Task Isolation (Priority: P2)

**Goal**: Each authenticated user can only access and manage their own tasks.

**Independent Test**: Can be fully tested by creating two users, each adding tasks, and verifying that each user only sees and modifies their own tasks.

### Tests for User Story 4 ⚠️

- [ ] T043 [P] [US4] Integration test: User A attempts to access/modify/delete User B's task via API (should return 403 Forbidden) in `apps/backend/tests/integration/test_tasks.py`.

### Implementation for User Story 4

- [ ] T044 [US4] Review and ensure all task API endpoints in `apps/backend/src/api/tasks.py` robustly filter by `owner_id` and raise `HTTPException` for unauthorized access.

---

## Phase 7: User Story 5 - Responsive Frontend UI (Priority: P3)

**Goal**: The web application provides a responsive and intuitive user interface across different devices.

**Independent Test**: Can be tested by interacting with the web application on various screen sizes and devices, verifying layout and functionality remain consistent.

### Tests for User Story 5 ⚠️

- [ ] T045 [P] [US5] Automated (e.g., Playwright) or manual tests for UI responsiveness of key pages (login, signup, tasks list) in `apps/frontend/tests/integration/test_ui_responsiveness.spec.ts`.

### Implementation for User Story 5

- [ ] T046 [US5] Apply responsive design principles and styles to key frontend components and pages (`apps/frontend/src/app/(auth)/signup/page.tsx`, `apps/frontend/src/app/(auth)/login/page.tsx`, `apps/frontend/src/app/(app)/tasks/page.tsx`, etc.).

---

## Phase N: Polish & Cross-Cutting Concerns

**Purpose**: Improvements that affect multiple user stories, integration tests, and operational readiness.

- [ ] T047 Implement centralized error handling middleware in `apps/backend/src/main.py` to return standardized JSON responses.
- [ ] T048 Setup structured logging for FastAPI backend in `apps/backend/src/main.py` and frontend in `apps/frontend/src/lib/logger.ts`.
- [ ] T049 Implement a basic CI/CD pipeline configuration (e.g., `.github/workflows/main.yml`) for automated testing and deployment.
- [ ] T050 Write comprehensive integration tests for end-to-end user flows across frontend and backend in `apps/integration_tests/` (a new root-level directory for E2E tests).

---

## Dependencies & Execution Order

### Phase Dependencies

- **Setup (Phase 1)**: No dependencies - can start immediately.
- **Foundational (Phase 2)**: Depends on Setup completion - BLOCKS all user stories.
- **User Stories (Phase 3+)**: All depend on Foundational phase completion.
  - User Story 1 (Authentication) is a prerequisite for all other user stories.
  - User Stories 2-5 can then proceed largely in parallel once US1 is functional.
- **Polish (Final Phase)**: Depends on all desired user stories being complete.

### User Story Dependencies

- **User Story 1 (P1 - Auth)**: Can start after Foundational (Phase 2) - BLOCKS all other user stories.
- **User Story 2 (P1 - CRUD)**: Can start after User Story 1.
- **User Story 3 (P2 - Complete Task)**: Can start after User Story 2.
- **User Story 4 (P2 - Isolation)**: Can start after User Story 1, but its full verification depends on US2/US3.
- **User Story 5 (P3 - Responsive UI)**: Can start after User Story 1, but depends on basic UI from US1 and US2.

### Within Each User Story

- Tests MUST be written and FAIL before implementation.
- Models before services/API endpoints.
- Backend API before Frontend UI integration.
- Core implementation before integration.
- Story complete before moving to next priority or deploying independently.

### Parallel Opportunities

- Setup tasks marked [P] can run in parallel (T001-T005 are mostly sequential for monorepo setup, but can be split).
- Foundational tasks marked [P] can run in parallel (T006-T009).
- Once Foundational phase completes, User Story 1 can begin.
- Once User Story 1 completes, User Stories 2, 3, 4, 5 and Polish tasks can proceed with careful coordination, or sequentially if a single team.
- Within each User Story, test tasks marked [P] can run in parallel.

---

## Implementation Strategy

### MVP First (User Story 1 & 2 Only)

1. Complete Phase 1: Setup.
2. Complete Phase 2: Foundational (CRITICAL - blocks all stories).
3. Complete Phase 3: User Story 1 (User Authentication).
4. Complete Phase 4: User Story 2 (Task Management - CRUD).
5. **STOP and VALIDATE**: Test User Stories 1 and 2 independently.
6. Deploy/demo if ready.

### Incremental Delivery

1. Complete Setup + Foundational → Foundation ready.
2. Add User Story 1 (Auth) → Test independently → Deploy/Demo.
3. Add User Story 2 (CRUD) → Test independently → Deploy/Demo.
4. Add User Story 3 (Mark Complete) → Test independently → Deploy/Demo.
5. Add User Story 4 (Isolation) → Test independently → Deploy/Demo.
6. Add User Story 5 (Responsive UI) → Test independently → Deploy/Demo.
7. Each story adds value without breaking previous stories.

### Parallel Team Strategy

With multiple developers (after Foundational phase and US1 is done):

- Developer A: User Story 2 (Task Management - CRUD)
- Developer B: User Story 3 (Mark Task as Completed)
- Developer C: User Story 4 (Multi-User Task Isolation)
- Developer D: User Story 5 (Responsive Frontend UI)
- Developer E: Polish & Cross-Cutting Concerns (e.g., logging, CI/CD)

---