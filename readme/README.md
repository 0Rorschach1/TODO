# To Do List Project (Phase 1 - In-Memory)

This is a Python OOP-based To Do List application with in-memory storage and CLI interface.
It supports managing projects and tasks with constraints as per the project specification.

## Setup
1. Install Poetry: `pip install poetry`
2. Install dependencies: `poetry install`
3. Copy `.env.example` to `.env` and set values.
4. Run: `poetry run python main.py`

## Features
- Create, edit, delete projects (with cascade delete for tasks)
- Add, edit, change status, delete tasks within projects
- List projects and tasks
- Constraints: Word limits, unique names, max limits from .env, valid dates/statuses

