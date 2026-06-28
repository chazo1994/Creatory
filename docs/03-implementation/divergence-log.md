# ⚠️ Divergence Log — Code vs Design

> **Layer:** Implementation. Lists places where the running code **deviates from**
> [`../02-design/`](../02-design/). Per the one-way trace rule in
> [`../README.md`](../README.md), **design is the source of truth** — every entry
> here is resolved by either (a) updating the code to match design, or (b) writing
> a design section first and then keeping the code. Code is never the spec by
> default.

Each entry: ID · what the code does · what design says · resolution direction.

---

## WF-1 — Workflow runner ignores edges (executes by canvas position) · **HIGH PRIORITY**

- **Priority:** raised. Re-use and **automation** ([automation.md](../02-design/automation.md))
  execute the saved graph headless, with no Director in the loop — so correct edge
  traversal is a prerequisite for the entire OPERATE pillar, not a cosmetic fix.
- **Code:** [`creatory_core/services/workflow_runner.py`](../../creatory_core/services/workflow_runner.py)
  orders nodes by `position_x` then `node_key` and runs them as a flat list. Edges
  and `condition_expr` are never read.
- **Design:** [workflow-model.md](../02-design/workflow-model.md) §4 — the Runtime
  MUST traverse **edges** in topological order; `position_x/y` are editor layout
  hints and MUST NOT drive execution.
- **Resolution:** update the runner to build the graph from edges and traverse
  topologically. **(Code → match design.)**

## WF-2 — `condition_expr` unimplemented

- **Code:** field exists in DB, JSON schema, and Pydantic (`WorkflowEdgePayload`)
  but is never evaluated.
- **Design:** [workflow-model.md](../02-design/workflow-model.md) §4.1 defines it as
  an optional boolean over upstream outputs — but the **expression grammar is not
  yet pinned**, so the field is currently *Reserved*.
- **Resolution:** design the grammar first (design gap), then implement evaluation.
  **(Design → then code.)**

## WF-3 — `router` and `memory` node types are undesigned

- **Code:** `node_type` enum (DB / JSON schema / Pydantic) includes `router` and
  `memory`. No template uses them; the runner has no behavior for them.
- **Design:** [workflow-model.md](../02-design/workflow-model.md) §3 marks both as
  **Reserved — not yet designed**. Templates MUST NOT use them.
- **Resolution:** either design these node types (§3 / §7) or remove the unused
  enum values. Until then, validation SHOULD reject templates using them.

## WF-4 — No `join_policy` / `output_schema` support

- **Code:** neither concept exists.
- **Design:** [workflow-model.md](../02-design/workflow-model.md) §3.1 (output
  schema, SHOULD) and §4.2 (`join_policy`, default `all`).
- **Resolution:** implement when edge traversal (WF-1) lands. **(Code → match
  design.)**

## OR-1 — HITL implemented only as a node type

- **Code:** `WAITING_HUMAN` is set **only** when a `human_gate` node is reached
  ([workflow_runner.py](../../creatory_core/services/workflow_runner.py)).
- **Design:** [orchestration.md](../02-design/orchestration.md) §6 and
  [workflow-model.md](../02-design/workflow-model.md) §6 — HITL is a cross-cutting
  concern (also pause on critical failure / policy triggers), not just one node.
- **Resolution:** the cross-cutting triggers are a **design gap**; design them
  before implementing. Current node-only behavior is acceptable for V0.

## OR-2 — Director hardcodes a single agent slug

- **Code:** [`creatory_core/services/director.py`](../../creatory_core/services/director.py)
  references a fixed `DIRECTOR_AGENT_SLUG`.
- **Design:** [orchestration.md](../02-design/orchestration.md) §2 treats the
  Director as a role that coordinates a registry of agents.
- **Resolution:** confirm whether a fixed system Director slug is the intended V0
  simplification (then document it) or should be registry-driven. **(Design
  clarification needed.)**
