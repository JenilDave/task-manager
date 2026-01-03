# Task Manager

A small FastAPI service to create and manage tasks, task statuses and status history using SQLAlchemy and Alembic.

Project Summary
- Purpose: Manage tasks, statuses, and status-history with an async FastAPI backend.
- Key features: JWT auth, service-layer business logic, Alembic migrations, Pydantic request/response schemas.

Tech Stack
- Language: Python
- Web: FastAPI
- ORM: SQLAlchemy 2.x (declarative mapping)
- Migrations: Alembic
- Validation: Pydantic
- Async DB driver: configured by `DATABASE_URL`

Quick Start
- Install uv if not available:
```bash
pip install uv
```

- Install dependencies
```bash
# Preferred — installs using uv.lock
uv sync
```

- Refer `.env.example` file for setting up env vars for the project

- Run migrations:
```bash
uv run alembic revision --autogenerate -m "describe change"
uv run alembic upgrade head
```

- Run the app:
```bash
uv run uvicorn main:app --reload
```

Environment / Config
- `DB_URL`: SQLAlchemy async URL.
- JWT secret & algorithm: defined in constants.py.
- Other environment-specific settings can be added as needed.

Database & Migrations
- Alembic reads `target_metadata` from the `Base` defined in base.py via env.py.
- Ensure:
  - All models inherit from the same `Base`.
  - Every model/table has a primary key column.
  - Model modules are imported before Alembic autogenerate runs (either explicitly in `env.py` or via a dynamic import snippet).
- Debug registered tables by temporarily printing `Base.metadata.tables.keys()` in env.py.

API
- Routers live under api.
- Centralized auth dependency: deps.py exposes `get_current_user` and a router-friendly alias (e.g., `CurrentUser`) so routers avoid importing ORM models.
- Schemas (Pydantic) are in schema. Example: user.py provides `UserOut` and `CreateUserPayload`.

Project Layout
- Root
  - main.py — application entrypoint
  - pyproject.toml — dependencies
  - alembic — migration config and versions
- Source (src/)
  - api — FastAPI routers and dependencies (`deps.py`)
  - db — SQLAlchemy models and `Base` (`base.py`)
  - schema — Pydantic schemas (`user.py`)
  - service — business logic and DB operations (e.g., `user_service.py`, `task_service.py`)
  - utils — helpers (DB session provider, constants, logger)

Design Guidelines
- Keep routers thin (routing + validation). Move business logic to service.
- Use Pydantic DTOs for responses; enable `from_attributes = True` / `orm_mode = True` so Pydantic can serialize ORM objects (see user.py).
- Centralize auth and dependency logic in deps.py to reuse `get_current_user` across routers.

Common Troubleshooting
- Empty autogenerate migration:
  - Confirm `Base` used by Alembic matches the `Base` your models inherit from.
  - Ensure model files are imported (Alembic only detects models loaded into `Base.metadata`).
  - Ensure models define a primary key.
  - Remove empty revision files, fix code, then re-run autogenerate.
- __pycache__ is harmless.

Useful Commands
```bash
# create a migration after model changes
alembic revision --autogenerate -m "message"
# apply migrations
alembic upgrade head
# run app
uvicorn main:app --reload
# quick import test
python -c "import importlib; importlib.import_module('src.api.deps'); print('deps OK')"
```

Contributing
- Create feature branches and open PRs.
- Add migrations for schema changes and avoid committing empty revisions.
- Keep tests for services and critical flows.

License
- MIT
