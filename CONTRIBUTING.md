# Contributing to Creatory

Creatory is a creator-first open-source framework for multi-agent content production.
This guide defines contribution rules for a stable and extensible ecosystem.

## 1. Core Principles

- Creator-first: optimize creator control, speed, and output quality.
- Agent-centric: tools are orchestrated by agents, not isolated scripts.
- Human-in-the-loop: critical creative outputs require review checkpoints.
- Extensible by design: add capabilities via MCP or workflow templates.
- Production quality: typed schemas, tests, and reproducible runtime.

## 2. Repo Layout

- `creatory_core/`: backend runtime and APIs
- `creatory_studio/`: frontend studio
- `mcp/`: tool protocol registry + server conventions
- `workflows/`: shareable template recipes + schemas
- `infra/`: docker compose and deployment assets
- `docs/`: product/architecture specs

## 3. Setup

```bash
cp .env.example .env
python3 -m venv .venv
source .venv/bin/activate
make install
make migrate
make test
```

Frontend:

```bash
make frontend-install
make frontend-dev
```

## 4. Branch & Commit Convention

- Branches: `feat/<name>`, `fix/<name>`, `docs/<name>`, `refactor/<name>`, `test/<name>`
- Commits: Conventional Commits (`feat:`, `fix:`, `docs:`, `refactor:`, `test:`)

## 5. Pull Request Requirements

Each PR should include:

- Problem statement
- Proposed solution and scope
- Testing evidence
- Backward compatibility notes
- Security/privacy impact (if external APIs/tools are involved)

Keep PRs small and focused.

## 6. Contribution Tracks

### 6.1 PAL (Provider Abstraction Layer)

- Add provider specs, routing behavior, and connection checks in `creatory_core/providers/`.
- Keep provider logic vendor-agnostic and deterministic.
- Avoid hard-coding API keys or tenant-specific endpoints.

### 6.2 MCP Tools

- Add or document tool manifests under `mcp/registry/`.
- New tool contracts must define input/output schema and error shape.
- For runtime integration, ensure each tool is traceable through invocation logs.

### 6.3 Workflow Templates

- Add YAML templates in `workflows/templates/`.
- Validate shape against `workflows/schemas/workflow_template.schema.json`.
- Include at least one HITL node for non-trivial generation flows.

### 6.4 Frontend Studio

- Place source under `creatory_studio/src/`.
- Keep dual-stream UX behavior consistent.
- Preserve API typing in `creatory_studio/src/lib/types.ts`.

## 7. Code Quality Standards

- Backend:
  - `ruff check creatory_core tests`
  - `black --check creatory_core tests`
- Frontend:
  - `cd creatory_studio && npm run lint`
  - `cd creatory_studio && npm run build`
- Tests:
  - `pytest`

## 8. Database Changes

Any schema change must include:

- Alembic revision (`alembic/versions/`)
- SQL migration update (`sql/migrations/`)
- Upgrade/downgrade notes in PR description

## 9. Security & Privacy

- Never commit secrets or credentials.
- Mask sensitive payloads in logs and traces.
- Document external data flow when adding provider/tool integrations.

## 10. RFC Expectations

Open an RFC issue before major changes:

- Breaking API contracts
- Orchestrator state model changes
- Workflow schema changes
- Provider routing policy changes

## 11. Definition of Done

A contribution is done when:

- Code, docs, and schema are aligned
- CI-local checks pass
- Review feedback is addressed
- Another contributor can run and validate without private context
