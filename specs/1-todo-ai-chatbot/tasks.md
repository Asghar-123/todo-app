# Tasks: AI-powered Todo Chatbot

**Input**: Design documents from `/specs/1-todo-ai-chatbot/`
**Prerequisites**: plan.md (required), spec.md (required for user stories), research.md, data-model.md, contracts/

**Tests**: The examples below include test tasks. Tests are OPTIONAL - only include them if explicitly requested in the feature specification.

**Organization**: Tasks are grouped by user story to enable independent implementation and testing of each story.

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Which user story this task belongs to (e.g., US1, US2, US3)
- Include exact file paths in descriptions

## Path Conventions

- **Web app**: `backend/src/`, `frontend/src/`, `mcp-tools/`, `ai-agent/` at repository root

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Project initialization and basic structure

- [ ] T001 Create `backend/` project structure
- [ ] T002 Create `frontend/` project structure
- [ ] T003 Create `mcp-tools/` project structure
- [ ] T004 Create `ai-agent/` project structure
- [ ] T005 Create `deployment/` project structure
- [ ] T006 Configure Python virtual environment and dependencies in `backend/`
- [ ] T007 Configure Python virtual environment and dependencies in `mcp-tools/`
- [ ] T008 Initialize Node.js project and dependencies in `frontend/`
- [ ] T009 Initialize Python virtual environment and dependencies in `ai-agent/`
- [ ] T010 Setup shared `.env` configuration

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Core infrastructure that MUST be complete before ANY user story can be implemented

**⚠️ CRITICAL**: No user story work can begin until this phase is complete

- [ ] T011 Implement database connection and session management in `backend/app/db/database.py`
- [ ] T012 Define `Task` SQLModel in `backend/app/models/task.py`
- [ ] T013 Define `ConversationHistory` SQLModel in `backend/app/models/conversation.py`
- [ ] T014 Implement Alembic migrations for database schema in `backend/migrations/`
- [ ] T015 Setup FastAPI application instance and basic routing in `backend/app/main.py`
- [ ] T016 Configure logging and error handling in `backend/app/core/`

**Checkpoint**: Foundation ready - user story implementation can now begin in parallel

---

## Phase 3: User Story 1 - Create and View Tasks (Priority: P1) 🎯 MVP

**Goal**: Users can create new tasks and view their existing tasks through natural language interaction with the chatbot.

**Independent Test**: Create a task via natural language and then query the chatbot to list all tasks, confirming the new task is present.

### Implementation for User Story 1

- [x] T017 [US1] Implement `TaskService` (create/list logic) in `backend/app/services/task_service.py`
- [x] T018 [US1] Implement `createTask` MCP tool in `mcp_tools/tools/create_task.py`
- [x] T019 [US1] Implement `listTasks` MCP tool in `mcp_tools/tools/list_tasks.py`
- [x] T020 [US1] Register MCP tools with OpenAI Agent in `ai_agent/config/tools.yaml`
- [x] T021 [US1] Implement Chat API endpoint `/chat/message` (create task) in `backend/app/api/chat.py`
- [x] T022 [US1] Implement Chat API endpoint `/chat/message` (view tasks) in `backend/app/api/chat.py`
- [x] T023 [US1] Implement `sendMessage` logic in `ai_agent/agent/main.py` to use `createTask` and `listTasks`
- [x] T024 [US1] Develop frontend components for sending messages in `frontend/src/components/ChatInput.tsx`
- [x] T025 [US1] Develop frontend components for displaying tasks in `frontend/src/components/TaskList.tsx`
- [x] T026 [US1] Integrate `ChatInput` and `TaskList` into main app in `frontend/src/App.tsx`

### Tests for User Story 1

- [x] T027 [US1] Write unit tests for `TaskService` in `backend/tests/unit/test_task_service.py`
- [x] T028 [US1] Write integration tests for `createTask` and `listTasks` MCP tools in `mcp_tools/tests/integration/`
- [x] T029 [US1] Write integration tests for Chat API create/view in `backend/tests/integration/test_chat_api.py`
- [x] T030 [US1] Write unit/component tests for `ChatInput` and `TaskList` in `frontend/tests/unit/`

**Checkpoint**: At this point, User Story 1 should be fully functional and testable independently

---

## Phase 4: User Story 2 - Mark Tasks Complete and Filter (Priority: P1)

**Goal**: Users can mark tasks as complete and filter their tasks by status or due date through natural language interaction.

**Independent Test**: Create a task, mark it complete, and then filter by status (completed/incomplete) to verify its state.

### Implementation for User Story 2

- [x] T031 [US2] Update `TaskService` (mark/filter logic) in `backend/app/services/task_service.py`
- [x] T032 [US2] Implement `markTaskStatus` MCP tool in `mcp_tools/tools/mark_status.py`
- [x] T033 [US2] Implement `filterTasks` MCP tool in `mcp_tools/tools/filter_tasks.py`
- [x] T034 [US2] Register new MCP tools with OpenAI Agent in `ai_agent/config/tools.yaml`
- [x] T035 [US2] Implement Chat API endpoint `/chat/message` (mark status) in `backend/app/api/chat.py`
- [x] T036 [US2] Implement Chat API endpoint `/chat/message` (filter tasks) in `backend/app/api/chat.py`
- [x] T037 [US2] Update `sendMessage` logic in `ai_agent/agent/main.py` to use `markTaskStatus` and `filterTasks`
- [x] T038 [US2] Develop frontend components for marking tasks complete/incomplete in `frontend/src/components/TaskItem.tsx`
- [x] T039 [US2] Develop frontend components for filtering tasks in `frontend/src/components/TaskFilter.tsx`

### Tests for User Story 2

- [x] T040 [US2] Write unit tests for updated `TaskService` in `backend/tests/unit/test_task_service.py`
- [x] T041 [US2] Write integration tests for `markTaskStatus` and `filterTasks` MCP tools in `mcp_tools/tests/integration/`
- [x] T042 [US2] Write integration tests for Chat API mark/filter in `backend/tests/integration/test_chat_api.py`
- [x] T043 [US2] Write unit/component tests for `TaskItem` and `TaskFilter` in `frontend/tests/unit/`

**Checkpoint**: At this point, User Stories 1 AND 2 should both work independently

---

## Phase 5: User Story 3 - Update and Delete Tasks (Priority: P2)

**Goal**: Users can modify existing tasks and delete tasks that are no longer relevant through natural language interaction.

**Independent Test**: Create a task, update its details, verify the update, and then delete it, verifying its removal.

### Implementation for User Story 3

- [x] T044 [US3] Update `TaskService` (update/delete logic) in `backend/app/services/task_service.py`
- [x] T045 [US3] Implement `updateTask` MCP tool in `mcp_tools/tools/update_task.py`
- [x] T046 [US3] Implement `deleteTask` MCP tool in `mcp_tools/tools/delete_task.py`
- [x] T047 [US3] Register new MCP tools with OpenAI Agent in `ai_agent/config/tools.yaml`
- [x] T048 [US3] Implement Chat API endpoint `/chat/message` (update task) in `backend/app/api/chat.py`
- [x] T049 [US3] Implement Chat API endpoint `/chat/message` (delete task) in `backend/app/api/chat.py`
- [x] T050 [US3] Update `sendMessage` logic in `ai_agent/agent/main.py` to use `updateTask` and `deleteTask`
- [x] T051 [US3] Develop frontend components for updating task details in `frontend/src/components/TaskDetail.tsx`
- [x] T052 [US3] Develop frontend components for confirming task deletion in `frontend/src/components/ConfirmDeleteDialog.tsx`

### Tests for User Story 3

- [x] T053 [US3] Write unit tests for updated `TaskService` in `backend/tests/unit/test_task_service.py`
- [x] T054 [US3] Write integration tests for `updateTask` and `deleteTask` MCP tools in `mcp_tools/tests/integration/`
- [x] T055 [US3] Write integration tests for Chat API update/delete in `backend/tests/integration/test_chat_api.py`
- [x] T056 [US3] Write unit/component tests for `TaskDetail` and `ConfirmDeleteDialog` in `frontend/tests/unit/`

**Checkpoint**: All user stories should now be independently functional

---

## Phase 6: Polish & Cross-Cutting Concerns

**Purpose**: Improvements that affect multiple user stories

- [ ] T057 Implement API for conversation history in `backend/app/api/chat.py`
- [ ] T058 Develop frontend for displaying conversation history in `frontend/src/components/ConversationHistory.tsx`
- [ ] T059 Implement comprehensive error handling and user feedback across frontend and backend
- [ ] T060 Configure structured logging for all services
- [ ] T061 Create Dockerfiles for backend, mcp-tools, and ai-agent in `deployment/docker/`
- [ ] T062 Write basic Kubernetes deployment manifests in `deployment/kubernetes/`
- [ ] T063 Develop deployment scripts for local development and cloud in `deployment/scripts/`
- [ ] T064 Review and refine API contracts for consistency and completeness
- [ ] T065 Conduct security review of the entire system
- [ ] T066 Performance testing and optimization

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

### Within Each User Story

- Tests (if included) MUST be written and FAIL before implementation
- Models before services
- Services before endpoints
- Core implementation before integration
- Story complete before moving to next priority

### Parallel Opportunities

- All Setup tasks marked [P] can run in parallel (though not explicitly marked in this list, assumed by separate file/config tasks)
- All Foundational tasks marked [P] can run in parallel (within Phase 2, if no explicit file dependencies)
- Once Foundational phase completes, all user stories can start in parallel (if team capacity allows)
- All tests for a user story can be written/run in parallel
- Models/components within a story that don't depend on each other can be developed in parallel
- Different user stories can be worked on in parallel by different team members

---

## Parallel Example: User Story 1

```bash
# Launching tasks for User Story 1 that can run in parallel
Task: "Write unit tests for TaskService in backend/tests/unit/test_task_service.py"
Task: "Write integration tests for createTask and listTasks MCP tools in mcp-tools/tests/integration/"
Task: "Write integration tests for Chat API create/view in backend/tests/integration/test_chat_api.py"
Task: "Write unit/component tests for ChatInput and TaskList in frontend/tests/unit/"
Task: "Implement createTask MCP tool in mcp-tools/tools/create_task.py"
Task: "Implement listTasks MCP tool in mcp-tools/tools/list_tasks.py"
Task: "Develop frontend components for sending messages in frontend/src/components/ChatInput.tsx"
Task: "Develop frontend components for displaying tasks in frontend/src/components/TaskList.tsx"
```

---

## Implementation Strategy

### MVP First (User Story 1 Only)

1. Complete Phase 1: Setup
2. Complete Phase 2: Foundational (CRITICAL - blocks all stories)
3. Complete Phase 3: User Story 1
4. **STOP and VALIDATE**: Test User Story 1 independently
5. Deploy/demo if ready

### Incremental Delivery

1. Complete Setup + Foundational → Foundation ready
2. Add User Story 1 → Test independently → Deploy/Demo (MVP!)
3. Add User Story 2 → Test independently → Deploy/Demo
4. Add User Story 3 → Test independently → Deploy/Demo
5. Each story adds value without breaking previous stories

### Parallel Team Strategy

With multiple developers:

1. Team completes Setup + Foundational together
2. Once Foundational is done:
   - Developer A: User Story 1
   - Developer B: User Story 2
   - Developer C: User Story 3
3. Stories complete and integrate independently

---

## Notes

- [P] tasks = different files, no dependencies (not explicitly marked in this comprehensive list, but implied by module separation)
- [Story] label maps task to specific user story for traceability
- Each user story should be independently completable and testable
- Verify tests fail before implementing
- Commit after each task or logical group
- Stop at any checkpoint to validate story independently
- Avoid: vague tasks, same file conflicts, cross-story dependencies that break independence
