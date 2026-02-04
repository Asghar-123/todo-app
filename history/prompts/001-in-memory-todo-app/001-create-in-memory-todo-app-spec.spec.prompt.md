---
id: 001
title: Create In-Memory Todo App Spec
stage: spec
date: 2026-02-03
surface: agent
model: claude-sonnet-4-5-20250929
feature: in-memory-todo-app
branch: 001-in-memory-todo-app
user: system
command: /sp.specify
labels: ["specification", "todo-app", "in-memory"]
links:
  spec: specs/001-in-memory-todo-app/spec.md
  ticket: null
  adr: null
  pr: null
files:
  - specs/001-in-memory-todo-app/spec.md
  - specs/001-in-memory-todo-app/checklists/requirements.md
tests:

---

## Prompt

Phase I: In-Memory Python Console Todo App

Target audience:
- Reviewers evaluating spec-driven, agentic development
- Python learners at intermediate level

Objective:
Build a command-line todo application in Python that stores tasks entirely in memory and demonstrates spec → plan → tasks → implementation using Claude Code and Spec-Kit Plus.

Required features:
- Add todo
- View todos
- Update todo
- Delete todo
- Mark todo as completed

Success criteria:
- All five features function correctly
- Console-based interaction only (stdin/stdout)
- Data exists only during runtime (no persistence)
- Clean, readable, modular Python code
- Clear traceability from spec to implementation

Constraints:
- Python 3.11+
- UV for environment management
- Python standard library only
- In-memory data structures (list/dict/class)
- No manual coding; implementation via Claude Code only

Not building:
- File or database storage
- Web, GUI, or API interfaces
- Advanced todo features (search, tags, reminders)
- AI functionality (future phases)

## Response snapshot

Created feature specification and quality checklist for 'In-Memory Python Console Todo App'.

## Outcome

- ✅ Impact: Spec created, ready for planning.
- 🧪 Tests: N/A
- 📁 Files: Two files created: `spec.md`, `requirements.md`
- 🔁 Next prompts: `/sp.clarify` or `/sp.plan`
- 🧠 Reflection: User requested PHR after noticing it was missed. The process for generating a feature spec involves creating the spec file and a checklist, but the PHR creation was not explicitly included in the initial execution flow. This PHR documents the spec creation.

## Evaluation notes (flywheel)

- Failure modes observed: PHR generation was missed in the initial `/sp.specify` execution.
- Graders run and results (PASS/FAIL): N/A
- Prompt variant (if applicable): N/A
- Next experiment (smallest change to try): Ensure PHR is integrated into the `/sp.specify` command's execution flow.
