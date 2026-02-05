# Creatory

Creator-first, multi-agent orchestration framework for building content workflows.

## Tech Stack

- Backend: FastAPI
- Database: PostgreSQL + pgvector
- Orchestration model: Main Director Agent + dual-stream conversation + agentic workflow runtime
- DevOps: Docker Compose + Alembic + pre-commit + CI

## Project Structure

```text
app/
  api/
  core/
  db/
  schemas/
alembic/
docs/
scripts/
sql/migrations/
```

## Quick Start

1. Copy env file:

```bash
cp .env.example .env
```

2. Start production-like services:

```bash
docker compose up --build
```

3. Open API docs:

- Swagger: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

For hot-reload local development with Docker:

```bash
make compose-up-dev
```

## Local Development

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -e .[dev]
cp .env.example .env
make migrate
make run
```

## Useful Commands

- `make lint`
- `make format`
- `make test`
- `make migrate`
- `make downgrade`
- `make compose-up`
- `make compose-up-dev`
- `make compose-down`

## Initial API Scope

- Auth: register, login, token, me
- Workspaces: create, list, get
- Conversations: create, list
- Threads: create, list
- Messages: create, list
- Context injection from side thread to main thread

## Database and Migrations

- Alembic config: `alembic.ini`
- Migration runtime: `alembic/env.py`
- Initial revision: `alembic/versions/20260206_0001_base_schema.py`
- Upgrade SQL: `sql/migrations/0001_base_schema.up.sql`
- Downgrade SQL: `sql/migrations/0001_base_schema.down.sql`

When using Docker Compose, `migrate` service runs `alembic upgrade head` before API starts.

## Contribution

See `CONTRIBUTING.md`.
