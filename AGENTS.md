```
# 🤖 AGENTS & ORCHESTRATION FRAMEWORK (CREATOR-FIRST)

## 0. Document Control

| Field | Value |
| --- | --- |
| Document Type | Product + Architecture Spec (Normative + V0 Snapshot) |
| Status | Active |
| Owner | Core Maintainers |
| Version | v1.0 |
| Last Updated | 2026-02-20 |
| Canonical Vision Source | `docs/brainstorm.md` |
| Canonical Technical Sources | `docs/conceptual_blueprint_v0.md`, `docs/archtecture/framework_architecture_v0.md`, `docs/archtecture/frontend-architecture.md`, `docs/requirements/business_requirements.md`, `docs/roadmap/product_roadmap.md` |

---

## 1. Purpose & Scope

This document defines:

- The Multi-Agent orchestration architecture following a Creator-First approach.
- The multi-thread interaction standards.
- The boundaries of responsibility between Director, Workflow Runtime, Frontend, MCP, and Knowledge layers.
- The extension and contribution rules to keep the system consistent as the community scales.

---

## 2. How To Read This Spec

### 2.1 Normative Levels

- `MUST`: mandatory requirement to be considered architecturally correct.
- `SHOULD`: strongly recommended; deviations require clear justification.
- `MAY`: optional.

### 2.2 Sections Split

- Sections 3-10 are the **Normative Spec** (formal definitions).
- Section 11 is the **Implementation Snapshot (V0)** (current state, subject to change).
- Section 12 is **Non-goals / Out of Scope**.
- Section 13 is the **Traceability Matrix** for mapping to original source documents.

---

## 3. Product Vision (Normative)

- The platform must serve content creators under a `Creator-First` philosophy.
- AI must function as an `Agentic Orchestrator`, not merely a chatbot responder.
- Humans retain final creative decision authority (creative sovereignty).
- The system must be extensible via MCP Tools, Workflow Templates, and Specialized Agents.

---

## 4. Core Architecture (Normative)

### 4.1 Director Layer (Planning + State)

Main Director Agent:

- `MUST` be the primary touchpoint for the creator in the main flow.
- `MUST` perform intention decoding, planning, and conversation-based state tracking.
- `SHOULD` coordinate with PAL to select local/cloud model routing per task.
- `MUST NOT` handle detailed node-by-node execution of the workflow runtime.

### 4.2 Workflow Runtime Layer (Execution)

Workflow Runner:

- `MUST` execute workflow templates using nodes/edges.
- `MUST` support human gate states (`WAITING_HUMAN`) for HITL.
- `MUST` remain separated from the Director for testability, runtime swap flexibility, and observability.

### 4.3 Bridge Layer

Bridge Injector:

- `MUST` be the only place that standardizes context blocks injected from sub-thread to main thread.
- `MUST` log injections for auditing and context replay.
- Frontend `MUST` use the bridge API and `MUST NOT` re-implement business normalization logic.

### 4.4 Guardrails

- `MUST` include a circuit breaker limiting execution steps to prevent infinite loops.
- `SHOULD` include budget guardrails (token/cost) for production scale.
- HITL `MUST` serve as a quality and safety mechanism, not merely UX decoration.

---

## 5. Multi-thread Interaction (Normative)

This is the core mechanism, based on the original idea in `docs/brainstorm.md`.

### 5.1 Interaction Model

- Main Conversation:
  - Where the creator works with the Main Director Agent on strategy and content structure.
- Contextual Sub-Thread:
  - A contextual side flow for quick Q&A, detailed analysis, or local experimentation.

### 5.2 Trigger, Isolation, Injection

- Trigger:
  - A sub-thread `SHOULD` be opened from contextual actions (highlight/click/select point).
- Isolation:
  - A sub-thread `MUST` maintain its own context; it must not automatically pollute the main context.
- Injection:
  - Only when the user explicitly chooses, content/summary from the sub-thread may be promoted into the main context.
  - Injection `MUST` go through the Bridge API.

### 5.3 Source-of-Truth Rules

- The main thread is the source-of-truth for project state.
- The sub-thread is a temporary contextual workspace.
- After injection, the context block becomes a referenceable part of the main thread.

### 5.4 Vision vs Rollout

- Standard Vision:
  - One main thread + multiple contextual sub-threads per context zone.
- V0 Rollout:
  - 1 main thread + 1 quick side thread to simplify onboarding.
- Expansion:
  - Multiple contextual sub-threads while preserving `Isolation + Explicit Injection`.

---

## 6. Chat-based Workflow vs Main Director Agent (Normative)

- Main Director Agent:
  - The orchestrating actor (coordination role).
- Chat-based Workflow:
  - The conversational operating mode used by the Director.

Rules:

- Chat-based workflow `MUST` be treated as an interaction mode of the Director, not as an independent agent.
- Frontend `MUST` call orchestration endpoints; backend decides the appropriate agent/runtime.

---

## 7. Agentic Workflow Model (Normative)

### 7.1 Chat-Based Path

- Creator submits a prompt in the main conversation.
- Director responds with plan/routing/tasks to guide execution.

### 7.2 Node-Based Path

- A Node represents an Agent Persona, Tool (MCP), or Human Gate.
- An Edge represents data/condition flow.
- Workflow templates `SHOULD` be community-shareable artifacts (YAML/JSON schema-governed).

---

## 8. Knowledge Layer (Normative)

- The system `MUST` support Hybrid RAG at the architectural level (vector + graph semantics).
- Retrieval `SHOULD` return citation-capable context.
- Input `SHOULD` be diverse: text, image metadata, audio/transcript, links, raw documents.

---

## 9. Tools & MCP Extension Layer (Normative)

- MCP `MUST` be the primary extension mechanism for the tool ecosystem.
- Runtime core `MUST` be separated from tool/provider-specific logic.
- Tool contracts `MUST` define clear input/output schemas and error shapes.
- Contributor guidance for MCP tools `MUST` be defined in `CONTRIBUTING.md`.

---

## 10. Frontend Architecture (Normative)

### 10.1 Role Boundaries

- Frontend `MUST` focus on UX/state orchestration.
- Backend `MUST` handle state transitions and business invariants.
- Frontend `MUST NOT` duplicate backend orchestration logic.

### 10.2 Core Studio Modules

| Module | Responsibility |
| --- | --- |
| Dual-Chat Interface | Main conversation + quick/contextual interactions |
| Context Injection UX | Explicit promote from sub-thread to main |
| Workflow Panel | Workflow visualization/run control |
| Prompt Lab / Assets / Settings | Persona tuning, asset flow, provider controls |

---

## 11. Implementation Snapshot (V0)

- Monorepo aligned: `creatory_core/`, `creatory_studio/`, `mcp/`, `workflows/`, `infra/`.
- PAL endpoints V0: provider catalog, connection test, routing preview.
- Hybrid RAG query endpoint with citation-style response scaffold.
- Bridge injector runtime for side-thread → main-thread context block.
- Starter workflow templates located at `workflows/templates/`.
- Frontend workflow panel currently in viewer/runner mode; full drag-drop authoring belongs to a later phase.

---

## 12. Non-goals / Out of Scope (Current Stage)

- Do not treat sub-thread as a replacement for main project state.
- Do not allow bypassing HITL at critical creative steps by default.
- Do not tightly couple the core orchestrator to vendor-specific APIs.
- Do not commit to a full visual authoring editor in V0.
- Do not allow frontend to decide business injection semantics independently.

---

## 13. Traceability Matrix

| Topic | Canonical Source(s) | This Spec |
| --- | --- | --- |
| Creator-First + Agentic Orchestration | `docs/brainstorm.md`, `docs/requirements/business_requirements.md` | Sections 3, 4 |
| Multi-thread Interaction | `docs/brainstorm.md` | Section 5 |
| Director/Workflow/Bridge split | `docs/conceptual_blueprint_v0.md`, `docs/archtecture/framework_architecture_v0.md` | Sections 4, 6, 7 |
| Frontend module boundaries | `docs/archtecture/frontend-architecture.md` | Section 10 |
| MCP/RAG extension direction | `docs/brainstorm.md`, `docs/conceptual_blueprint_v0.md` | Sections 8, 9 |
| Delivery phasing | `docs/roadmap/product_roadmap.md` | Section 11 |

---

## 14. Governance & Contribution Rules

- Major changes to orchestrator state model, workflow schema, injection semantics, or provider routing policy `MUST` have an RFC before merge.
- PRs `SHOULD` demonstrate alignment across code/docs/schema.
- Any change that deviates from `docs/brainstorm.md` interaction semantics `MUST` be clearly documented in the changelog.

---

## 15. High-Level Roadmap

- Sprint 1: Core orchestration + dual-chat baseline.
- Sprint 2: Hybrid RAG + basic MCP toolchain.
- Sprint 3: Workflow visualization + robust run control.
- Sprint 4: Video/audio pipeline + community templates.
- Sprint 5: Production hardening + contributor ecosystem scaling.

---

> Motto: Creator thinks - Agent executes - Framework scales.
```
