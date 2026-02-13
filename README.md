# Creatory

Creator-first open-source framework for orchestrating AI agents, tools, and workflows for content production.

## Vision

Creatory is built as a multi-agent "intellectual OS" for creators:

- Main Director Agent orchestrates long-form project execution.
- Dual-stream chat supports main + quick threads.
- Bridge Injector promotes quick-thread outputs into main context.
- Hybrid RAG keeps creator memory (knowledge + concept relationships).
- MCP toolbox makes tools pluggable without changing core orchestrator logic.

## Architecture (V0)

- `creatory_core/`: backend intelligence (FastAPI, orchestration services, PAL, RAG)
- `creatory_studio/`: frontend studio (Next.js, dual-chat, workflow view, settings center)
- `mcp/`: MCP servers/registry/sdk contracts
- `workflows/`: shareable workflow templates + schemas
- `infra/`: deployment assets (Docker Compose)
- `docs/`: product and architecture documents

## Tech Stack

- Backend: FastAPI, SQLAlchemy (async), Alembic
- Orchestration: Director runtime + workflow runtime + circuit breaker
- PAL (Provider Abstraction Layer): provider catalog/routing/testing primitives
- RAG: knowledge sources/chunks + concept graph-aware retrieval
- Database: PostgreSQL + pgvector
- Frontend: Next.js (App Router), TanStack Query, Zustand, React Flow
- DevOps: Docker Compose, pre-commit, Makefile

## Project Structure

```text
creatory/
├── creatory_core/
│   ├── agents/
│   ├── api/
│   ├── core/
│   ├── db/
│   ├── providers/
│   ├── rag/
│   ├── schemas/
│   ├── services/
│   ├── main.py
│   └── worker.py
├── creatory_studio/
│   ├── src/
│   │   ├── app/
│   │   ├── components/
│   │   ├── hooks/
│   │   ├── lib/
│   │   └── store/
│   └── Dockerfile
├── mcp/
│   ├── servers/
│   ├── registry/
│   └── sdk/
├── workflows/
│   ├── templates/
│   └── schemas/
├── infra/
│   ├── docker-compose.yml
│   └── docker-compose.dev.yml
├── docs/
├── alembic/
├── scripts/
└── tests/
```

## Prerequisites

- Docker + Docker Compose v2
- Python 3.12+
- Node.js 20+ and npm
- GNU Make

## Quick Start

### 1. Configure environment

```bash
cp .env.example .env
```

### 2. Run full stack (recommended)

```bash
make compose-up
```

Open:

- Studio: http://localhost:3000
- API docs: http://localhost:8000/docs

### 3. Stop services

```bash
make compose-down
```

## Local Development

### Backend

```bash
python3 -m venv .venv
source .venv/bin/activate
make install
make migrate
make run
```

In another terminal:

```bash
source .venv/bin/activate
make run-worker
```

### Frontend

```bash
make frontend-install
make frontend-dev
```

## Core API Surface (`/api/v1`)

- `auth`: register/login/token/me
- `workspaces`: workspace lifecycle + bootstrap defaults
- `conversations`: dual-thread chat objects + context injection
- `orchestration`: director run, run detail, SSE stream
- `providers`: PAL catalog, connection test, routing preview
- `workflows`: template CRUD + run execution
- `mcp`: server/tool registry + invocation + manifest endpoint
- `knowledge`: sources/chunks + hybrid RAG query
- `assets`: media asset tracking
- `agents`: agent personas and run traces

## Commands

- `make lint`
- `make format`
- `make test`
- `make migrate`
- `make run`
- `make run-worker`
- `make frontend-dev`
- `make compose-up`
- `make compose-up-dev`
- `make compose-down`

## Workflow Templates

Starter templates live in `workflows/templates/`.

- Bootstrap workspace currently imports `workflows/templates/short_video_pipeline.yaml`.
- Template schema: `workflows/schemas/workflow_template.schema.json`.

## MCP Registry

Bootstrap manifest:

- `mcp/registry/default_manifest.yaml`
- `mcp/registry/manifest.schema.json`

API endpoint:

- `GET /api/v1/mcp/registry/manifest`

## Contributing

Read:

- `CONTRIBUTING.md`
- `docs/archtecture/framework_architecture_v0.md`
- `docs/conceptual_blueprint_v0.md`
- `docs/roadmap/product_roadmap.md`

## License

MIT. See `LICENSE`.
