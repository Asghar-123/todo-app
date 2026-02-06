# Implementation Plan: Full-Stack Multi-User Todo Web Application

**Branch**: `002-multi-user-todo-app` | **Date**: 2026-02-05 | **Spec**: specs/002-multi-user-todo-app/spec.md
**Input**: Feature specification from `/specs/002-multi-user-todo-app/spec.md`

**Note**: This template is filled in by the `/sp.plan` command. See `.specify/templates/commands/plan.md` for the execution workflow.

## Summary

This plan outlines the architecture and implementation strategy for a Full-Stack Multi-User Todo Web Application, transforming the Phase I console todo app. It details the use of Next.js for the frontend, FastAPI for the backend, SQLModel for ORM, Neon PostgreSQL for persistent storage, and JWT-based authentication using Better Auth, all integrated within a monorepo structure.

## Technical Context

**Language/Version**: Python 3.11+ (for backend), TypeScript/JavaScript (for frontend with Next.js)
**Primary Dependencies**: Next.js 16+ (App Router), FastAPI, SQLModel, Better Auth, Neon PostgreSQL
**Storage**: Neon PostgreSQL
**Testing**: Pytest (backend), Jest/React Testing Library (frontend)
**Target Platform**: Web application (browsers)
**Project Type**: Monorepo with web (frontend) and API (backend)
**Performance Goals**: Responsive UI, API response times under 200ms for common operations, support for up to 100 concurrent users.
**Constraints**: Next.js 16+ App Router, FastAPI, SQLModel, Neon PostgreSQL, Better Auth JWT tokens with shared secret, Monorepo structure with Spec-Kit.
**Scale/Scope**: Multi-user todo application with basic CRUD operations, user authentication, and task isolation.

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

Refer to `.specify/memory/constitution.md` for general project principles. A detailed check will be performed against the specific project needs during implementation. No specific violations are currently identified based on the high-level plan.

## Project Structure

### Documentation (this feature)

```text
specs/002-multi-user-todo-app/
├── plan.md              # This file (/sp.plan command output)
├── research.md          # Phase 0 output (/sp.plan command)
├── data-model.md        # Phase 1 output (/sp.plan command)
├── quickstart.md        # Phase 1 output (/sp.plan command)
├── contracts/           # Phase 1 output (/sp.plan command)
└── tasks.md             # Phase 2 output (/sp.tasks command - NOT created by /sp.plan)
```

### Source Code (repository root)

```text
.
├── apps/
│   ├── frontend/             # Next.js App Router frontend
│   │   ├── src/
│   │   │   ├── app/          # App Router pages
│   │   │   ├── components/
│   │   │   └── lib/          # Frontend-specific utilities/hooks
│   │   └── tests/
│   │       ├── unit/
│   │       └── integration/
│   └── backend/              # FastAPI REST backend
│       ├── src/
│       │   ├── api/          # API endpoints
│       │   ├── auth/         # Authentication logic
│       │   ├── crud/         # Database operations
│       │   ├── models/       # SQLModel definitions
│       │   └── main.py       # FastAPI application entry
│       └── tests/
│           ├── unit/
│           └── integration/
├── packages/
│   └── types/                # Shared TypeScript/Python types (if needed)
├── specs/
│   └── 002-multi-user-todo-app/
│       ├── plan.md           # This file
│       ├── spec.md
│       ├── checklists/
│       └── ...
├── history/
│   └── prompts/
│       └── 002-multi-user-todo-app/
│           └── ...
└── .specify/
    └── ...
```

**Structure Decision**: A monorepo structure is chosen to accommodate separate frontend (Next.js) and backend (FastAPI) applications while maintaining a single repository. This allows for clear separation of concerns, independent deployment units, and potential for shared packages (e.g., types).

## Key Decisions and Rationale

### Task ownership enforcement strategy
- **Options Considered**:
    - Backend-only enforcement (database-level foreign keys, API query filters).
    - Frontend-level filtering only (less secure).
    - Combination of both.
- **Rationale**: **Backend-only enforcement** will be implemented using database-level relationships (foreign key from Task to User) and API-level authorization middleware. This is the most secure and reliable method, as frontend filtering alone is insufficient for security.

### JWT verification middleware design
- **Options Considered**:
    - Manual parsing and validation in each endpoint.
    - Custom FastAPI dependency (reusable middleware).
    - Using `Better Auth`'s built-in JWT handling.
- **Rationale**: FastAPI dependencies will be used to encapsulate JWT extraction and validation. `Better Auth`'s utilities will be integrated into these dependencies to handle token decoding, signature verification, and expiration checks. This provides a clean, reusable, and secure approach.

### Frontend API client authentication handling
- **Options Considered**:
    - Store JWT in local storage (vulnerable to XSS).
    - Store JWT in HTTP-only cookies (more secure against XSS).
    - Session-based authentication.
- **Rationale**: JWTs will be stored in **HTTP-only, secure cookies** on the frontend after successful login. This provides a balance between security (against XSS attacks) and usability. Frontend code will automatically send these cookies with API requests.

### Database schema structure for users and tasks
- **Options Considered**:
    - Separate `User` and `Task` tables with a one-to-many relationship.
    - Denormalized structure (e.g., tasks embedded in user document, not suitable for relational DB).
- **Rationale**: A **normalized relational schema** will be used with separate `User` and `Task` tables. The `Task` table will have a foreign key (`owner_id`) referencing the `User` table, establishing a one-to-many relationship. This ensures data integrity and supports efficient querying for user-specific tasks. `SQLModel` will be used to define these models.

### Error handling and validation approach
- **Options Considered**:
    - Ad-hoc error messages at each layer.
    - Centralized error handling middleware with standardized error responses.
    - Frontend-only validation.
- **Rationale**: **Centralized error handling middleware** will be implemented in the FastAPI backend to catch exceptions (e.g., validation errors, authentication failures, not found errors) and return standardized JSON error responses (e.g., HTTP status codes 400, 401, 403, 404, 500). Frontend will display user-friendly messages based on these standardized responses. Pydantic validation will be used at the API input level.

## Interfaces and API Contracts

### Public APIs
RESTful API endpoints will be defined for user authentication and todo task management.
- **Auth Endpoints**:
    - `POST /auth/signup`: Create new user. Input: username, password. Output: success/error message.
    - `POST /auth/login`: Authenticate user. Input: username, password. Output: JWT token (in HTTP-only cookie).
    - `POST /auth/logout`: Invalidate session/cookie.
- **Task Endpoints (Authenticated)**:
    - `POST /tasks`: Create a new task. Input: description. Output: new Task object.
    - `GET /tasks`: Retrieve all tasks for the authenticated user. Output: list of Task objects.
    - `GET /tasks/{task_id}`: Retrieve a specific task by ID for the authenticated user. Output: Task object.
    - `PUT /tasks/{task_id}`: Update an existing task. Input: description, is_completed (optional). Output: updated Task object.
    - `DELETE /tasks/{task_id}`: Delete a task. Output: success message.

### Versioning Strategy
Initial API version will be `v1`. Future breaking changes will necessitate a new API version (e.g., `/v2/tasks`).

### Idempotency, Timeouts, Retries
- `POST /tasks` will not be inherently idempotent (multiple calls create multiple tasks).
- `PUT /tasks/{task_id}` and `DELETE /tasks/{task_id}` will be idempotent.
- Frontend will implement reasonable timeouts (e.g., 5-10 seconds) and retry mechanisms for transient network failures.

### Error Taxonomy with status codes
- `200 OK`: Successful operation.
- `201 Created`: Resource created successfully (e.g., `POST /tasks`).
- `204 No Content`: Successful deletion (e.g., `DELETE /tasks/{task_id}`).
- `400 Bad Request`: Invalid input/payload (e.g., empty description, malformed ID).
- `401 Unauthorized`: Missing or invalid JWT.
- `403 Forbidden`: Authenticated but not authorized to access resource (e.g., accessing another user's task).
- `404 Not Found`: Resource not found (e.g., `GET /tasks/{invalid_id}`).
- `500 Internal Server Error`: Unexpected server-side errors.

## Non-Functional Requirements (NFRs) and Budgets

### Performance
- p95 latency for critical API endpoints (login, create task, get tasks) under 200ms.
- Frontend page load time (LCP) under 2.5 seconds.
- System supports at least 100 concurrent authenticated users without significant performance degradation.

### Reliability
- API uptime SLO: 99.9% (less than 8.76 hours downtime per year).
- Error budget: 0.1% for non-critical errors.
- Degradation strategy: In case of database connectivity issues, provide informative error messages to the user.

### Security
- AuthN/AuthZ: JWT-based authentication, task ownership enforcement (Backend-only).
- Data handling: All sensitive data (passwords) hashed before storage. User data encrypted in transit (HTTPS).
- Secrets: JWT secret, database connection string stored in environment variables (e.g., `.env`).
- Auditing: Log security-relevant events (login attempts, failed authentication).

### Cost
Optimize database queries to minimize Neon compute unit consumption. Use serverless functions/hosting where appropriate to scale down to zero.

## Data Management and Migration

### Source of Truth
Neon PostgreSQL database.

### Schema Evolution
`SQLModel` migrations will be used to manage schema changes (e.g., Alembic with SQLModel).

### Migration and Rollback
Automated database migrations will be part of the deployment pipeline. Rollback strategy will involve reverting to previous database state (via migrations) and application version.

### Data Retention
User and task data will be retained indefinitely unless explicitly deleted by the user.

## Operational Readiness

### Observability
- **Logs**: Structured logging for backend (FastAPI, uvicorn) with severity levels (INFO, WARN, ERROR) and relevant context (user ID, request ID). Frontend logging for client-side errors.
- **Metrics**: Prometheus/Grafana (or similar) for API request rates, error rates, latency, database connection pooling, and resource utilization.
- **Traces**: Distributed tracing (e.g., OpenTelemetry) to track requests across frontend and backend services.

### Alerting
- Thresholds: Alert on API error rates > 1%, API latency p95 > 500ms, database connection failures, new user signup failures.
- On-call owners: DevOps/Backend team for critical alerts.

### Runbooks for common tasks
Document procedures for: database schema updates, service restarts, resolving common API errors, frontend deployment issues.

### Deployment and Rollback strategies
- Deployment: Containerized (Docker) deployment to a cloud platform (e.g., Vercel for Next.js, Fly.io/Render for FastAPI). CI/CD pipeline for automated builds and deployments.
- Rollback: Fast rollback to previous stable version in case of critical issues.

### Feature Flags and compatibility
No initial use of feature flags. Backwards compatibility for API should be considered with versioning.

## Risk Analysis and Mitigation

### Risk 1
- **Risk**: Security vulnerabilities (e.g., JWT secret exposure, SQL injection, XSS).
- **Blast radius**: Compromise of user data, unauthorized access.
- **Kill switches/guardrails**: Environment variables for secrets, strong password hashing, input validation, secure cookie settings.

### Risk 2
- **Risk**: Database performance bottlenecks (e.g., slow queries with many users/tasks).
- **Blast radius**: Slow application, poor user experience.
- **Kill switches/guardrails**: Database indexing, query optimization, connection pooling, monitoring, scaling Neon database.

### Risk 3
- **Risk**: Frontend-backend integration issues (e.g., API contract mismatches).
- **Blast radius**: Broken features, development delays.
- **Kill switches/guardrails**: Shared TypeScript types (if applicable), OpenAPI schema generation and validation, comprehensive integration tests.

## Evaluation and Validation

### Definition of Done (tests, scans)
- All user stories from `specs/002-multi-user-todo-app/spec.md` are covered by automated unit and integration tests.
- Backend unit tests (`pytest`) cover models, business logic, and API endpoint handlers.
- Frontend unit tests (`Jest`/`React Testing Library`) cover components and client-side logic.
- Integration tests verify end-to-end user flows (signup, login, CRUD operations via UI and API, task isolation).
- API contract tests (e.g., using `schemathesis`) ensure API adheres to OpenAPI specification.
- All tests pass successfully with acceptable code coverage (e.g., >80%).
- Static analysis (e.g., `ESLint`, `Black`, `isort`) passes without errors.

### Output Validation for format/requirements/safety
- Web UI is responsive and provides a consistent user experience.
- API responses adhere to defined contracts and error taxonomy.
- Authentication and authorization mechanisms function as expected, preventing unauthorized access and ensuring task isolation.
- Data persistence is verified in Neon PostgreSQL.
