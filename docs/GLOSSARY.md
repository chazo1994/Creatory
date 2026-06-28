# Glossary — Canonical Terms

One meaning per term. If you need a new meaning, pick a new term. This file exists
because several terms were previously overloaded across docs (especially
"workflow" and "agentic workflow"); the definitions here are authoritative.

## Orchestration

| Term | Canonical meaning | Do **not** use it for |
| --- | --- | --- |
| **Director** | The single orchestrating agent that decodes creator intent, plans, and delegates. A *role/actor*. | A runtime engine; a chat UI. |
| **Chat-based orchestration** | The conversational operating mode of the Director, where a plan is produced from a chat prompt and executed on the fly. A *mode of the Director*. | A standalone agent; the node-based workflow runtime. |
| **Workflow** | A **declarative graph** (nodes + edges) describing a reusable pipeline. Always the node/edge artifact. | The Director's chat planning (that is "chat-based orchestration"). |
| **Workflow Template** | A versioned, shareable, schema-governed `Workflow` definition (YAML/JSON). | A single run instance. |
| **Workflow Run** | One execution instance of a `Workflow Template`. | The template itself. |
| **Workflow Runtime / Runner** | The engine that executes a `Workflow Run` by traversing nodes/edges. Distinct from the Director. | The Director. |
| **Agentic** | Adjective meaning "driven by agent reasoning rather than fixed code." Describes a *style*, not a component. | A specific feature or file. |

> Deprecated phrase: **"Agentic Workflow"** as a single noun. It was used for the
> philosophy, the node editor feature, *and* the runtime. Split it: use
> **"Workflow"** (the artifact), **"node-based path"** (the feature), or
> **"agentic orchestration"** (the style).

## Workflow graph

| Term | Canonical meaning |
| --- | --- |
| **Node** | A step in a `Workflow`. It **references** a behavior by type + config; it does not *embody* it. See [02-design/workflow-model.md](02-design/workflow-model.md). |
| **Node type** | The kind of step. Canonical set is defined **only** in the design doc, and is the source of truth over code enums. |
| **Edge** | A directed connection declaring order and optional `condition_expr` data/condition flow between two nodes. |
| **Human Gate** | A node type that pauses a run (`WAITING_HUMAN`) for explicit creator approval. The *node-level* expression of HITL. |
| **HITL (Human-in-the-Loop)** | The cross-cutting principle that humans approve critical outputs. Broader than the `human_gate` node. |

## Re-use & Automation

| Term | Canonical meaning |
| --- | --- |
| **Director-generated workflow** | A graph **compiled by the Director** from chat intent, then saved. The primary way templates are created (not hand-drawing). See [02-design/workflow-model.md](02-design/workflow-model.md) §9. |
| **Execution trace** | The node/edge structure the Director emits while planning; the seed that becomes a saved template. |
| **Template inputs** | The typed signature of a template — a template is a **function** invoked with new inputs. |
| **Replay** | Re-execute the same graph with the same inputs (deterministic). |
| **Re-run** | Re-execute the same graph with **new inputs** — the core automation case. |
| **Re-plan** | Hand the goal back to the Director to regenerate the graph (explicit creator action, never silent). |
| **Run mode** | `interactive` (human present, synchronous HITL) vs `autonomous` (headless, async HITL). |
| **Trigger** | What activates a run: `manual` / `scheduled` / `event`. |
| **Async HITL** | Human approval that does not block a headless run — via `approve_to_publish` (default), `pause_resume`, or `auto_approve`. See [02-design/automation.md](02-design/automation.md) §4. |
| **Output sink** | Where an autonomous run's product goes: Asset Library or auto-publish via MCP. |

## Interaction

| Term | Canonical meaning |
| --- | --- |
| **Main thread** | Source-of-truth conversation for project state. |
| **Sub-thread (quick / contextual)** | Isolated side conversation triggered from a context point; never auto-pollutes the main thread. |
| **Bridge / Bridge Injector** | The single component that normalizes and promotes a context block from a sub-thread into the main thread. |
| **Injection** | The explicit, user-initiated promotion of sub-thread content into the main thread via the Bridge. |

## Platform

| Term | Canonical meaning |
| --- | --- |
| **PAL (Provider Abstraction Layer)** | The layer that decouples the system from specific LLM/media vendors (local or cloud). |
| **MCP (Model Context Protocol)** | The standard extension mechanism for external tools. |
| **Hybrid RAG** | Retrieval combining vector (semantic) and graph (relational) stores. |
| **Circuit Breaker** | Guardrail that halts a run exceeding a step or budget limit. |
