# 🧬 Workflow Model (Design Layer — Canonical)

> **Layer:** Design (normative, **source of truth**). This document defines the
> node/edge workflow contract. When code, JSON schema, or DB enums disagree with
> this file, **this file wins** and the gap is recorded in
> [`../03-implementation/divergence-log.md`](../03-implementation/divergence-log.md).
> Terms are fixed in [`../GLOSSARY.md`](../GLOSSARY.md). Uses MUST/SHOULD/MAY.

Traces up to: [`../01-concept/business-requirements.md`](../01-concept/business-requirements.md)
FR-04 (Agentic Node Editor), and [`../01-concept/vision.md`](../01-concept/vision.md) §3.

---

## 1. What a Workflow Is

A **Workflow** is a **declarative directed graph** of `nodes` and `edges` that
describes a reusable content-production pipeline. It is the *node-based path* of
[orchestration.md](orchestration.md) §1 — distinct from the Director's chat-based
planning.

- A **Workflow Template** is a versioned, shareable definition (authored as
  YAML/JSON, validated by a schema).
- A **Workflow Run** is one execution of a template by the **Workflow Runtime**.

> **How graphs are primarily created (read §9 first).** The default authoring
> surface is **not** a blank canvas. A creator works with the **Director**
> (chat-based), and the Director **generates** the graph. The graph is the
> durable, inspectable, re-runnable, schedulable form of that plan — see §9
> (Director-generated workflows), §10 (parameterization), §11 (re-use), and
> [automation.md](automation.md) (scheduling / autonomous runs). Hand-drawing a
> graph node-by-node is a later, optional refinement path, consistent with the
> concept that this is *agentic reasoning made visible, not visual programming*.

## 2. Core Principle: a Node *references*, it does not *embody*

> **Design decision (resolves the "represents vs invokes" ambiguity):**
> A node does **not** *contain* an agent or tool. A node **references** a behavior
> by its `type` plus a `config_json` that points to the concrete actor (e.g. an
> agent by `slug`, a tool by `tool_group`). This keeps templates portable: the
> same template runs against different agent/tool registries per workspace.

So a node is: `{ node_key, type, config_json, position_x?, position_y? }`.

## 3. Node Types

The canonical node-type set is defined **here** and nowhere else.

| Type | Status | Meaning | Required `config_json` |
| --- | --- | --- | --- |
| `agent` | **Active** | Invoke an agent persona to produce output. | `agent` (slug), plus optional `output` name, `style`, etc. |
| `tool` | **Active** | Invoke an MCP tool / tool group. | `tool_group` (or `tool`), plus tool-specific params. |
| `human_gate` | **Active** | Pause the run for explicit creator approval (HITL). | `label`; `approval_required` (bool); `required` (bool). |
| `router` | **Reserved** | *Intended* conditional branch / fan-out selector. **Not yet designed.** | — (undefined) |
| `memory` | **Reserved** | *Intended* read/write to the knowledge layer. **Not yet designed.** | — (undefined) |

> **Design-led ruling on `router` and `memory`:** these values currently exist in
> code (DB enum + JSON schema + Pydantic) but were never specified at the design
> level. Per the source-of-truth rule, they are **Reserved, not Active**:
> templates MUST NOT use them until this section defines their `config_json`,
> semantics, and runtime behavior. Their presence in code is logged as a
> divergence. To activate either, design it here **first**, then unblock code.

### 3.1 Per-node output contract (SHOULD)

Every `agent`/`tool` node SHOULD declare an `output_schema` in its `config_json`.
The Runtime SHOULD validate node output against it before passing data along an
edge, and retry or fail the step on mismatch. This turns "an agent returned some
text" into a typed, dependable pipeline.

```yaml
- node_key: "script"
  type: "agent"
  config_json:
    agent: "script-writer"
    output: "script"
    output_schema:           # SHOULD: validate before the edge carries it
      type: object
      required: ["hook", "body", "cta"]
      properties:
        hook: { type: string }
        body: { type: string }
        cta:  { type: string }
```

## 4. Edges and Traversal

An **edge** is `{ source_node_key, target_node_key, condition_expr?, metadata_json? }`.

- The graph MUST be acyclic for V0 (no loops). Loop/iteration support is a future
  extension (§7).
- The Runtime MUST execute nodes by **traversing edges** in topological order — a
  node becomes eligible only when its incoming edges are satisfied. Execution
  order MUST NOT depend on canvas coordinates (`position_x`/`position_y` are
  layout hints for the editor only, never execution order).

### 4.1 Conditional edges — `condition_expr`

> **Design decision (defines a previously-unspecified field):** `condition_expr`
> is an optional boolean expression evaluated against the **run context** (the
> accumulated `output` values of completed upstream nodes). If present and it
> evaluates false, the edge is **not** taken.

- Expression language: a small, safe, side-effect-free boolean expression over
  named upstream outputs (e.g. `script.cta != "" && research.score > 0.7`). The
  concrete grammar MUST be pinned in this section before code implements it; until
  then, `condition_expr` is **Reserved** like router/memory.
- A node with no satisfied incoming edge is **skipped** (status recorded), not
  failed.

### 4.2 Fan-in / join policy

> **Design decision (new):** when a node has multiple incoming edges, its
> `config_json.join_policy` declares how it waits:

| `join_policy` | Meaning |
| --- | --- |
| `all` (default) | Wait for **every** satisfied incoming edge (barrier). |
| `any` | Proceed as soon as the **first** incoming edge completes. |

## 5. Template Format

Templates live in `workflows/templates/*.yaml` and are validated by
`workflows/schemas/workflow_template.schema.json`. Top-level shape:

```yaml
name: "Short Video Pipeline"        # required
description: "..."                  # optional
version: 1                          # required, integer >= 1
definition_json:                    # free-form template metadata
  objective: "..."
  category: "short-form"
nodes: [ ... ]                      # required, >= 1
edges: [ ... ]                      # required
```

- `version` MUST increment on any breaking change to a published template.
- Templates SHOULD be community-shareable artifacts; they MUST validate against the
  JSON schema in CI.

## 6. HITL in Workflows

- The `human_gate` node is the **node-level** expression of HITL: reaching it sets
  the run to `WAITING_HUMAN` and halts until a creator signal resumes it.
- HITL is also a **cross-cutting concern** (see [orchestration.md](orchestration.md)
  §6): the Runtime SHOULD support pausing for human review on critical failures or
  policy triggers, not only at explicit `human_gate` nodes. The cross-cutting
  trigger rules are a planned extension and MUST be designed here before
  implementation.

## 7. Future Extensions (designed before built)

These are intentionally **not** in V0. Each MUST get a design section here before
any code lands:

- **`router` node** — conditional branching / dynamic fan-out.
- **`memory` node** — typed read/write against the knowledge layer.
- **`condition_expr` grammar** — the pinned expression language.
- **Loops / map-fanout** — e.g. "generate N variants", "regenerate until
  approved" (requires relaxing the acyclic constraint with a bounded iteration
  guard tied to the circuit breaker).
- **Node-based drag-and-drop editor** — authoring UI (currently viewer-only).

## 8. State & Persistence

Runtime state (runs, per-node steps, status enum) is a data-contract concern —
see [data-model.md](data-model.md) §5 (`workflow_runs`, `workflow_run_steps`) and
the run-status lifecycle `queued → running → waiting_human → succeeded | failed |
cancelled`.

---

## 9. Director-generated Workflows (dynamic → static)

> This is the **primary** model for how workflows come to exist. It reconciles two
> facts: (a) today's models are excellent at *planning* control flow at runtime,
> and (b) re-use, sharing, and automation require a *frozen, repeatable* artifact.

**Mental model: the Director is a compiler; the graph is its bytecode.**

```
intent (chat) ──▶ Director ──compile──▶ Workflow Graph ──▶ Runtime ──▶ output
                    ▲                       │  (inspect / edit / save        │
                    └──── re-plan ──────────┘   as parameterized template)   │
                                            └──── HITL gate ◀────────────────┘
```

- The **Director** decodes intent and **emits an execution trace** — a node/edge
  structure — even while it runs dynamically. That trace is the seed of a graph.
- A creator MAY save a successful trace as a **Workflow Template** (§10). Saving is
  the main way templates are born; hand-authoring on a canvas is secondary.
- Once saved, the graph is **static at run time**: topology is frozen, but each
  `agent`/`tool` node is still *agentic* (it reasons over fresh input). This is the
  sweet spot — **repeatable structure + adaptive nodes** — which makes re-use and
  automation possible without making output robotic.

### 9.1 The three orchestration modes this implies

| Mode | Who drives control flow | When | Source of truth |
| --- | --- | --- | --- |
| **Dynamic (Director)** | Director plans live | Authoring / exploration / re-plan | Conversation |
| **Static (Runtime)** | The frozen graph | Trusted re-run, manual | Template + run record |
| **Autonomous (Runtime, headless)** | The frozen graph, no human present | Scheduled / event-triggered | Template + run record + trigger |

The autonomous mode is specified in [automation.md](automation.md). It is *only*
possible because the graph is static — see the rationale there. In autonomous mode
the Director is **compile-time only**: it generated the graph during authoring and
does not re-enter at run time ([automation.md](automation.md) §1).

> **Design-led decision (D2 — dynamic fan-out & loops): default is delegate to the
> Director, not new node types.** Unknown-size fan-out ("one image per scene") and
> "regenerate until approved" loops are handled by the **Director** at compile time
> (it emits the right number of nodes) or by re-planning — *not* by `map`/`loop`
> nodes in V0. Dedicated `map`/`loop`/`router` nodes remain Reserved (§3, §7) and
> are added only if a concrete need outgrows the Director path. *(Alternative if
> you disagree: design bounded `map`/`loop` nodes with a circuit-breaker guard.)*

## 10. Parameterization — a Template is a Function

A saved template is **not** a frozen one-shot; it is a **function with typed
inputs**. Re-use = invoke it with new inputs.

- A template MUST declare its **`inputs`**: named slots with type and optional
  default (e.g. `topic: string`, `language: string = "vi"`).
- A `Workflow Run` binds inputs via `input_json` (already in
  [data-model.md](data-model.md) §5).
- Node configs reference inputs by name (e.g. `{{ inputs.topic }}`); the binding
  grammar is the same expression language pinned for `condition_expr` (§4.1).

```yaml
name: "Daily Short Video"
version: 1
inputs:                      # NEW: the template's signature
  topic:    { type: string }
  audience: { type: string, default: "general" }
nodes: [ ... ]               # nodes reference {{ inputs.topic }}, etc.
edges: [ ... ]
```

## 11. Three Levels of Re-use

When a creator re-runs a workflow they trust, distinguish:

| Level | What changes | Cost / determinism | Typical use |
| --- | --- | --- | --- |
| **Replay** | Nothing (same graph, same inputs) | Cheapest, deterministic | Reproduce an exact result |
| **Re-run** | New `input_json`, same graph | Cheap, structurally identical | **The core automation case** — same recipe, new topic |
| **Re-plan** | Hand the goal back to the Director to regenerate the graph | Expensive, non-deterministic | Context changed enough that the old graph no longer fits |

Re-run is the default for automation. Re-plan is an explicit creator action, not
something a scheduled job does silently.

### 11.1 Idempotency for expensive nodes (SHOULD)

Because re-run and automation execute the same nodes repeatedly — including costly
media generation — every `agent`/`tool` node SHOULD be **idempotent** and SHOULD
expose a **cache key** derived from its resolved config + bound inputs. The Runtime
SHOULD skip re-executing a node whose cache key is unchanged and whose prior output
is still valid, to avoid paying for identical generations.
