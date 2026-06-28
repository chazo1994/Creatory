# 🎛️ Orchestration (Design Layer)

> **Layer:** Design (normative). Defines the Director, Workflow Runtime, Bridge,
> and the multi-thread interaction model. Uses **MUST / SHOULD / MAY** per
> [`../README.md`](../README.md). Term definitions are fixed in
> [`../GLOSSARY.md`](../GLOSSARY.md). Traces up to
> [`../01-concept/vision.md`](../01-concept/vision.md) §2–3.

## 1. Orchestration Modes (Director-first)

Intent becomes execution through **one engine with three modes**. The **Director
is the primary engine**: it plans dynamically and *generates* the graph that the
other two modes later replay. The modes are not competing products — they are the
same plan at different lifecycle stages (see
[workflow-model.md §9](workflow-model.md)).

| Mode | Trigger | Who drives control flow | Structure | Source of truth |
| --- | --- | --- | --- | --- |
| **Dynamic (Director)** — *primary* | A prompt in the main conversation | The **Director** plans live and emits an execution trace | Ephemeral per turn; trace is the seed of a graph | Conversation state |
| **Static (Runtime)** | Running a saved `Workflow Template` | The frozen graph (authored by the Director, optionally edited) | Persistent node/edge graph + bound `inputs` | Template + run record |
| **Autonomous (Runtime, headless)** | A schedule or event, no human present | The frozen graph | Persistent graph + trigger | Template + run record + trigger ([automation.md](automation.md)) |

> **Two taxonomies, don't conflate them.** "Dynamic / Static / Autonomous" above
> are *lifecycle stages of one plan*. Separately, a `Workflow Run` has a
> **`run_mode`** of `interactive` or `autonomous` ([automation.md](automation.md)
> §2): Static mode = an interactive run, Autonomous mode = an autonomous run.
> Dynamic (the Director) is authoring, not a run.

Rules:

- Dynamic orchestration MUST be treated as **a mode of the Director**, not as an
  independent agent (see [GLOSSARY](../GLOSSARY.md)).
- A graph is created **primarily by the Director** (dynamic → saved), not by
  hand-drawing. Hand-authoring is an optional refinement of an existing graph.
- Static and autonomous modes execute the **same** persisted graph; they differ
  only in trigger and in whether a human is present (which changes HITL handling —
  see [automation.md](automation.md) and §6).
- The graph model, parameterization, and re-use levels are specified in
  [workflow-model.md](workflow-model.md) §1–§11.
- The frontend MUST call orchestration endpoints and MUST NOT decide which mode or
  runtime is used; the backend decides.

## 2. Director Layer (Planning + State)

- The Director MUST be the primary creator touchpoint in the main flow.
- It MUST perform intention decoding, planning, and conversation-based state
  tracking.
- It SHOULD coordinate with PAL to route each task to a local or cloud model
  (e.g. cheap/local for drafts, smart/cloud for final polish).
- It MUST NOT perform node-by-node execution of the workflow runtime — that is the
  Runtime's job (separation enables testability and observability).

## 3. Workflow Runtime Layer (Execution)

- The Workflow Runner MUST execute `Workflow Templates` by traversing nodes and
  **edges** (see [workflow-model.md](workflow-model.md) §4 for traversal
  semantics).
- It MUST support the `WAITING_HUMAN` state for HITL.
- It MUST remain separate from the Director for testability, runtime-swap
  flexibility, and observability.

## 4. Bridge Layer

- The Bridge Injector MUST be the **only** place that standardizes context blocks
  promoted from a sub-thread into the main thread.
- It MUST log injections for auditing and replay.
- The frontend MUST use the Bridge API and MUST NOT re-implement normalization.

> **Why normalization exists:** sub-threads may produce raw, model-specific, or
> partial output. The Bridge guarantees the main thread only ever receives a
> single, audited, referenceable context-block shape — so the main thread's
> source-of-truth state never depends on sub-thread internals.

## 5. Multi-thread Interaction

### 5.1 Model
- **Main conversation:** strategy and structure with the Director.
- **Contextual sub-thread:** isolated side flow for quick Q&A / analysis.

### 5.2 Trigger, Isolation, Injection
- **Trigger:** a sub-thread SHOULD open from a contextual action (highlight /
  click / select point).
- **Isolation:** a sub-thread MUST keep its own context and MUST NOT auto-pollute
  the main context.
- **Injection:** only on explicit user choice MAY sub-thread content be promoted to
  the main context, and it MUST go through the Bridge API.

### 5.3 Source-of-truth
- The **main thread** is the source of truth for project state.
- The **sub-thread** is a temporary contextual workspace.
- After injection, the context block becomes a referenceable part of the main
  thread.

## 6. Guardrails

- A **circuit breaker** MUST limit execution steps to prevent infinite loops.
- Budget guardrails (token/cost) SHOULD exist for production scale.
- **HITL** is a cross-cutting quality/safety mechanism — it is expressed at minimum
  as the `human_gate` node, but the principle applies beyond a single node type
  (see [workflow-model.md](workflow-model.md) §6).

## 7. Non-goals (current stage)

- A sub-thread MUST NOT replace main project state.
- Default flows MUST NOT bypass HITL at critical creative steps.
- The core orchestrator MUST NOT be tightly coupled to vendor APIs.
- The frontend MUST NOT decide business injection semantics independently.
