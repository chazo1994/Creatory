# 🤖 AGENTS & ORCHESTRATION — Entry Point

This file is the entry point for humans and coding agents. The actual
specification is **layered** under [`docs/`](docs/) and split into three layers
that MUST NOT be mixed. Read [`docs/README.md`](docs/README.md) first.

| Document Type | Routing + governance entry point |
| --- | --- |
| Status | Active |
| Owner | Core Maintainers |
| Source of truth | **Design layer** (`docs/02-design/`) over code |

## The three layers

1. **Concept** — [`docs/01-concept/`](docs/01-concept/): vision, philosophy,
   requirements (*what* & *why*).
2. **Design** — [`docs/02-design/`](docs/02-design/): structural contracts,
   node/edge model, runtime behavior (*how*). **This is the source of truth.**
3. **Implementation** — [`docs/03-implementation/`](docs/03-implementation/): what
   is actually built, and where it diverges from design.

## Where to look

| You want to… | Read |
| --- | --- |
| Understand the product vision | [`docs/01-concept/vision.md`](docs/01-concept/vision.md) |
| See functional requirements | [`docs/01-concept/business-requirements.md`](docs/01-concept/business-requirements.md) |
| Understand orchestration (Director/Runtime/Bridge, multi-thread) | [`docs/02-design/orchestration.md`](docs/02-design/orchestration.md) |
| **Design or modify a workflow** | [`docs/02-design/workflow-model.md`](docs/02-design/workflow-model.md) |
| Re-use / scheduling / autonomous content production | [`docs/02-design/automation.md`](docs/02-design/automation.md) |
| Module layout & communication | [`docs/02-design/architecture.md`](docs/02-design/architecture.md) |
| Data contracts | [`docs/02-design/data-model.md`](docs/02-design/data-model.md) |
| Canonical term meanings | [`docs/GLOSSARY.md`](docs/GLOSSARY.md) |
| What's built / what diverges | [`docs/03-implementation/`](docs/03-implementation/) |

## Rules for contributors and agents

- **Do not mix layers** in one document (see [`docs/README.md`](docs/README.md)).
- **Design wins over code.** Code that runs ahead of design is a *divergence* and
  MUST be recorded in
  [`docs/03-implementation/divergence-log.md`](docs/03-implementation/divergence-log.md).
- Major changes to the **orchestrator state model, workflow schema, injection
  semantics, or provider routing policy** MUST have an RFC before merge.
- PRs SHOULD demonstrate alignment across concept → design → code.

> Motto: **Creator thinks — Agent executes — Framework scales.**
