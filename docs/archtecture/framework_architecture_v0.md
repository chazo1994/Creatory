## Creatory Framework Architecture V0 (Bootstrap-Aligned)

This document describes the architecture currently implemented in this repository after the V0 refactor.

### 1. Monorepo Layout

```text
creatory/
├── creatory_core/            # Backend intelligence engine
│   ├── agents/               # Agent personas and orchestration hooks
│   ├── providers/            # Provider Abstraction Layer (PAL)
│   ├── api/                  # FastAPI routes (/api/v1/*)
│   ├── db/                   # ORM models and session layer
│   ├── rag/                  # Hybrid retrieval logic
│   ├── services/             # Bridge, workflow runtime, bootstrap services
│   ├── schemas/              # Pydantic contracts
│   ├── main.py               # API entrypoint
│   └── worker.py             # Orchestrator worker entrypoint
├── creatory_studio/          # Frontend studio (Next.js)
│   └── src/
│       ├── app/
│       │   ├── chat/         # Main dual-stream studio page
│       │   ├── library/      # Project/library module shell
│       │   └── settings/     # Provider settings center
│       ├── components/       # UI modules (chat/workflow/assets/prompt/settings)
│       ├── hooks/            # Reusable UI hooks (SSE, context injection)
│       ├── lib/              # API client + types
│       └── store/            # Zustand global state
├── mcp/                      # MCP toolbox
│   ├── servers/
│   ├── registry/
│   └── sdk/
├── workflows/                # Shared workflow DNA
│   ├── templates/
│   └── schemas/
├── infra/                    # Deployment assets
│   ├── docker-compose.yml
│   └── docker-compose.dev.yml
└── docs/
```

### 2. Backend Modules

#### 2.1 Director and Stateful Orchestration

- Director runtime: `creatory_core/services/director.py`
- Chat execution endpoint: `POST /api/v1/orchestration/conversations/{conversation_id}/threads/{thread_id}/chat`
- SSE run stream: `GET /api/v1/orchestration/runs/{run_id}/stream`

#### 2.2 Bridge Injector

- Injection service: `creatory_core/services/bridge.py`
- API endpoint: `POST /api/v1/conversations/{conversation_id}/inject`
- Behavior: writes `context_injections` + injects system context message into target thread.

#### 2.3 PAL (Provider Abstraction Layer)

- Provider catalog + test: `creatory_core/providers/`
- API endpoints:
  - `GET /api/v1/providers/catalog`
  - `POST /api/v1/providers/test`
  - `POST /api/v1/providers/routing/preview`

#### 2.4 Hybrid RAG

- Retrieval service: `creatory_core/rag/hybrid.py`
- API endpoint: `POST /api/v1/knowledge/query`
- Behavior: lexical chunk retrieval + concept-graph bonus + citation list.

#### 2.5 Circuit Breaker

- Safety guard: `creatory_core/services/circuit_breaker.py`
- Enforced in director/workflow runtime with `CIRCUIT_BREAKER_MAX_STEPS`.

### 3. Workflow System

- Template source of truth: `workflows/templates/*.yaml`
- Bootstrap loader: `creatory_core/services/workflow_catalog.py`
- Workspace default template import: `creatory_core/services/workspace_bootstrap.py`
- Runtime execution: `creatory_core/services/workflow_runner.py`
- Schema contract: `workflows/schemas/workflow_template.schema.json`

### 4. MCP System

- Registry manifest: `mcp/registry/default_manifest.yaml`
- Schema: `mcp/registry/manifest.schema.json`
- API endpoint: `GET /api/v1/mcp/registry/manifest`

### 5. Frontend Studio

- Main runtime UI: `creatory_studio/src/components/studio-app.tsx`
- Dual-stream UI: `creatory_studio/src/components/dual-chat-panel.tsx`
- Settings Center: `creatory_studio/src/components/settings-center.tsx`
- Workflow visualization: `creatory_studio/src/components/workflow-panel.tsx`

### 6. Deployment and Runtime

- Compose files live in `infra/`.
- Root `Makefile` maps commands to `infra/docker-compose*.yml`.
- Backend container entrypoint: `scripts/run_api.sh` -> `creatory_core.main:app`.

### 7. Current Phase Note

This is the bootstrap implementation for the initial phase:

- Workflow editor is currently view/run-first (not full drag-edit persistence).
- Provider connection checks are bootstrap-safe runtime validations (no secret vault yet).
- MCP execution path remains mock-friendly while manifest and contracts are stabilized.
