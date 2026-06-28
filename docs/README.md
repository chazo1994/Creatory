# Creatory Documentation

This documentation is organized into **three strictly separated layers**. The
single most important rule: **do not mix layers inside one document.** A concept
doc never names a schema field; a design doc never pastes Python; an
implementation note never argues product philosophy.

| Layer | Folder | Answers | Contains | Never contains |
| --- | --- | --- | --- | --- |
| **1. Concept** (Ý tưởng) | [`01-concept/`](01-concept/) | *What* and *why* | Vision, philosophy, product requirements, user value | Schemas, field names, file paths, tech-stack choices |
| **2. Design** (Thiết kế chi tiết) | [`02-design/`](02-design/) | *How*, structurally | Component responsibilities, data contracts, node/edge models, runtime behavior, interfaces — code-agnostic but precise | Vision rationale; concrete `.py`/`.sql` code; "current status" notes |
| **3. Implementation** (Hiện trạng) | [`03-implementation/`](03-implementation/) | *What is actually built* | V0 snapshot, what diverges from design, rollout status | New design decisions (those belong in layer 2 first) |

## The one-way trace rule

Information and authority flow **downward only**:

```
Concept  ──defines goals for──▶  Design  ──defines contracts for──▶  Implementation
   ▲                                ▲                                      │
   └──────────── traces back to ────┴──────── traces back to ─────────────┘
```

- **Design is the source of truth.** When code and design disagree, design wins.
  Code that runs ahead of design is not "the spec" — it is an **undesigned
  divergence** and must be logged in
  [`03-implementation/divergence-log.md`](03-implementation/divergence-log.md)
  until design catches up or the code is removed.
- Every design doc traces up to a concept/requirement. Every implementation note
  traces up to a design section. Never the reverse.

## How to make a change

1. **Changing the product idea?** Edit `01-concept/`, then check which design docs
   must follow.
2. **Changing structure/contracts?** Edit `02-design/` first. Open an RFC for
   changes to the orchestrator state model, workflow schema, injection semantics,
   or provider routing (see governance below).
3. **Changing code?** If it matches design, just build it. If it deviates, either
   update design first, or record it in the divergence log.

## Index

### 01 — Concept
- [vision.md](01-concept/vision.md) — Intellectual OS vision, core philosophy
- [business-requirements.md](01-concept/business-requirements.md) — functional & non-functional requirements (FR/NFR)
- [founder-brainstorm.md](01-concept/founder-brainstorm.md) — original raw founder notes (historical source)

### 02 — Design
- [architecture.md](02-design/architecture.md) — module layout & communication architecture
- [orchestration.md](02-design/orchestration.md) — Director, Workflow Runtime, Bridge, multi-thread model
- [**workflow-model.md**](02-design/workflow-model.md) — **the node/edge workflow contract (canonical)**; Director-generated graphs, parameterization, re-use
- [automation.md](02-design/automation.md) — re-use & autonomous production (triggers, run modes, async HITL)
- [knowledge-rag.md](02-design/knowledge-rag.md) — Hybrid RAG design
- [mcp-tools.md](02-design/mcp-tools.md) — MCP extension layer
- [frontend.md](02-design/frontend.md) — Studio frontend boundaries
- [data-model.md](02-design/data-model.md) — relational + vector data contracts

### 03 — Implementation
- [v0-snapshot.md](03-implementation/v0-snapshot.md) — what exists today
- [divergence-log.md](03-implementation/divergence-log.md) — where code differs from design

### Cross-cutting
- [GLOSSARY.md](GLOSSARY.md) — canonical terms (one meaning per term)
- [roadmap/product_roadmap.md](roadmap/product_roadmap.md) — delivery phasing
- [research/](research/) — external reference notes (see [reference_policy.md](research/reference_policy.md))

## Normative levels (used in design docs)

- **MUST** — mandatory to be architecturally correct.
- **SHOULD** — strongly recommended; deviations need justification.
- **MAY** — optional.

## Governance

- Major changes to the **orchestrator state model, workflow schema, injection
  semantics, or provider routing policy** MUST have an RFC before merge.
- PRs SHOULD demonstrate alignment across concept → design → code.
- Any deviation from `01-concept/` interaction semantics MUST be documented in the
  changelog.

> Motto: **Creator thinks — Agent executes — Framework scales.**
