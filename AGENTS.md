# 🤖 Agent Operating Guide (Creatory)

> Entry point for coding agents. It is **symlinked as `CLAUDE.md`** so Claude Code
> uses the same file. Kept intentionally short — the full documentation (layer
> definitions, index, and governance) is the single source of truth in
> **[`docs/README.md`](docs/README.md)**. Read that first.

## Hard rules when working in this repo

1. **Design is the source of truth.** Specs live in
   [`docs/02-design/`](docs/02-design/). If code conflicts with design, design wins.
2. **Never mix the doc layers** (concept / design / implementation).
3. **Code ahead of design is a divergence, not a new spec** — record it in
   [`docs/03-implementation/divergence-log.md`](docs/03-implementation/divergence-log.md).
4. Major changes to the orchestrator state model, workflow schema, injection
   semantics, or provider routing **need an RFC first** (see governance in
   [`docs/README.md`](docs/README.md)).

## Where to look

| You want to… | Read |
| --- | --- |
| Product vision / requirements | [`docs/01-concept/`](docs/01-concept/) |
| Orchestration (Director / Runtime / Bridge, multi-thread) | [`docs/02-design/orchestration.md`](docs/02-design/orchestration.md) |
| **Design or modify a workflow** | [`docs/02-design/workflow-model.md`](docs/02-design/workflow-model.md) |
| Re-use / scheduling / autonomous content production | [`docs/02-design/automation.md`](docs/02-design/automation.md) |
| Module layout & communication | [`docs/02-design/architecture.md`](docs/02-design/architecture.md) |
| Data contracts | [`docs/02-design/data-model.md`](docs/02-design/data-model.md) |
| Canonical term meanings | [`docs/GLOSSARY.md`](docs/GLOSSARY.md) |
| What's built / what diverges from design | [`docs/03-implementation/`](docs/03-implementation/) |
