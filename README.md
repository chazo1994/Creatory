# Creatory

Creator-first open-source framework for orchestrating AI agents and tools to produce content.

## What Is Included

- `Main Director Agent` orchestration runtime for dual-stream conversations.
- `Dual-Chat` model with context injection from quick stream to main stream.
- `Workflow Templates` + visual node-based execution model.
- `MCP Registry` for MCP servers, tools, and tool invocation traces.
- `Hybrid RAG primitives` for knowledge sources/chunks and graph concepts.
- `Media Asset Manager` to track generated artifacts.
- `Frontend Creator Studio` (Next.js + React Flow + TanStack Query + Zustand).
- Production stack via Docker Compose: API, agent worker, PostgreSQL+pgvector, Redis, frontend.

## Tech Stack

- Backend: FastAPI, SQLAlchemy (async), Alembic
- Orchestration: agent run/task model + workflow run/step runtime
- Database: PostgreSQL + pgvector
- Cache/queue base: Redis
- Frontend: Next.js App Router, Tailwind, React Flow, TanStack Query, Zustand
- DevOps: Docker Compose, pre-commit, GitHub Actions

## Project Structure

```text
app/
  api/
  core/
  db/
  schemas/
  services/
  worker.py
frontend/
  app/
  components/
  lib/
alembic/
sql/migrations/
docs/
```

## Prerequisites (Install Required Packages)

Required tooling:

- Docker + Docker Compose v2
- Python 3.12
- Node.js 20+ and npm
- GNU Make
- Git

Install by command line (macOS + Homebrew):

```bash
brew update
brew install git make python@3.12 node@20
brew install --cask docker
```

Then verify your toolchain:

```bash
docker --version
docker compose version
python3 --version
node --version
npm --version
make --version
```

## Run The System From Command Line

### Option A: Full Stack with Docker (recommended)

```bash
cp .env.example .env
make compose-up
```

Open:

- Frontend Studio: http://localhost:3000
- API Docs (Swagger): http://localhost:8000/docs
- API Docs (ReDoc): http://localhost:8000/redoc

Stop services:

```bash
make compose-down
```

### Option B: Docker Dev Mode (hot reload)

```bash
cp .env.example .env
make compose-up-dev
```

### Option C: Local CLI Development (without running API/frontend in containers)

1. Prepare env and use localhost for DB/Redis in `.env`:

```bash
cp .env.example .env
# DATABASE_URL=postgresql+asyncpg://creatory:creatory@localhost:5432/creatory
# REDIS_URL=redis://localhost:6379/0
```

2. Start only data services:

```bash
docker compose up -d db redis
```

3. Start backend API:

```bash
python3 -m venv .venv
source .venv/bin/activate
make install
make migrate
make run
```

4. In a second terminal, start worker:

```bash
source .venv/bin/activate
make run-worker
```

5. In a third terminal, start frontend:

```bash
make frontend-install
make frontend-dev
```

## Core API Modules

- `/api/v1/auth`: register, login, token, me
- `/api/v1/workspaces`: create/list/get
- `/api/v1/conversations`: conversations, threads, messages, context injection
- `/api/v1/orchestration`: director chat turn, run detail, SSE stream
- `/api/v1/agents`: agent catalog and runs
- `/api/v1/workflows`: template CRUD and workflow execution
- `/api/v1/mcp`: MCP server/tool registry and invocation
- `/api/v1/assets`: media asset CRUD
- `/api/v1/knowledge`: sources and chunks

## Useful Commands

- `make lint`
- `make format`
- `make test`
- `make migrate`
- `make run-worker`
- `make compose-up`
- `make compose-up-dev`
- `make compose-down`
- `make frontend-install`
- `make frontend-dev`
- `make frontend-build`

## Migrations

- Alembic config: `alembic.ini`
- Current revision: `alembic/versions/20260206_0001_base_schema.py`
- SQL source: `sql/migrations/0001_base_schema.up.sql`, `sql/migrations/0001_base_schema.down.sql`

## Contributing

Read `CONTRIBUTING.md` for MCP tools, workflow templates, and agent persona contribution standards.
