# 📦 V0 Implementation Snapshot

> **Layer:** Implementation. What is actually built today. This is a *status*
> record, not a spec — it traces up to [`../02-design/`](../02-design/). If
> anything here contradicts design, it is a divergence: see
> [divergence-log.md](divergence-log.md). Last consolidated: 2026-02-20.

## Repository

- Monorepo aligned: `creatory_core/`, `creatory_studio/`, `mcp/`, `workflows/`,
  `infra/`.

## Backend (`creatory_core`)

- **PAL bootstrap:** provider catalog + connection test + routing preview exposed
  via API and Studio Settings. Provider profiles are validated at runtime and are
  **not yet persisted** in dedicated provider tables (planned: encrypted profile
  storage at workspace/project scope).
- **Bridge Injector runtime:** side-thread → main-thread context blocks are
  written through the backend service for main-thread reuse.
- **Hybrid RAG bootstrap:** knowledge query endpoint returns citation-style
  context blocks.
- **Workflow source of truth:** starter workflow definitions load from
  `workflows/templates/*.yaml`.
- **Workflow runner:** executes a template's nodes (see divergence note WF-1 about
  edge traversal). Supports `WAITING_HUMAN` on `human_gate`. Circuit breaker caps
  step count.

## Frontend (`creatory_studio`)

- Routes split into `/chat`, `/library`, `/settings`.
- Workflow panel is in **viewer/runner** mode; full drag-and-drop authoring is a
  later phase.
- Reusable hooks include a run-stream listener and a context-injection helper
  under `creatory_studio/src/hooks/`.

## Data

- Base schema migration applied (`alembic/versions/20260206_0001_base_schema.py`,
  `sql/migrations/0001_base_schema.*`).
- Workflow tables (`workflow_templates/nodes/edges/runs/run_steps`) exist per
  [data-model.md](../02-design/data-model.md) §5.

## Roadmap pointer

Delivery phasing lives in [`../roadmap/product_roadmap.md`](../roadmap/product_roadmap.md).
