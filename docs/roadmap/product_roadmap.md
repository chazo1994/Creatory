# Creatory Product Roadmap (Vertical Slice)

Philosophy: ship complete slices early, then deepen capability.

## Current Stage: Bootstrap Initialization (Active)

This repository is currently aligned to the initialization stage.

### Completed in Bootstrap Refactor

- [x] Monorepo structure aligned: `creatory_core`, `creatory_studio`, `mcp`, `workflows`, `infra`
- [x] Director orchestration + dual-stream chat runtime
- [x] Bridge Injector service for side-thread -> main-thread context promotion
- [x] Provider Abstraction Layer (catalog/test/routing preview)
- [x] Hybrid RAG query endpoint with citation payload
- [x] Workflow template source moved to `workflows/templates/*.yaml`
- [x] Circuit breaker guard for orchestration/workflow step limits
- [x] MCP registry manifest scaffold + API exposure
- [x] Docker compose moved under `infra/` and wired through `Makefile`

## Phase 1: Genesis Slice

Goal: deliver one complete creator flow (research -> script -> media draft -> review).

### Backend

- [ ] Persist provider profiles securely per workspace/project.
- [ ] Add actual tool execution adapters (search/image/tts) beyond mock invocations.
- [ ] Add checkpointer for long-running agent runs.
- [ ] Expand workflow runner from sequential execution to graph traversal.

### Frontend

- [ ] Improve settings UX with per-project provider overrides.
- [ ] Add artifact canvas preview mode linked to chat outputs.
- [ ] Add richer streaming timeline for orchestration events.

## Phase 2: Dual-Stream Depth + RAG Expansion

- [ ] Highlight-based contextual sub-thread creation from draft artifacts.
- [ ] Source citation UX in chat answers.
- [ ] Multi-format ingestion pipeline (docx, markdown, media transcript).
- [ ] Offline-first profile (local-only compose with local model providers).

## Phase 3: Workflow Ecosystem

- [ ] Visual workflow editor with editable node graph persistence.
- [ ] Community template import/export flows.
- [ ] Step-level retry policy and failure recovery graph branches.
- [ ] Workflow analytics dashboard (usage, cost, failure maps).

## Contributor Focus Now

Recommended contribution areas in current phase:

1. MCP registry/tool contracts and test fixtures.
2. Workflow template quality and validation tooling.
3. Provider adapter implementations in PAL.
4. Studio UX for library and settings modules.
