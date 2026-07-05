# 🗺️ CREATORY: VERTICAL SLICE ROADMAP

**Philosophy:** "Ship early, ship complete features."
**Core Tech Stack:** FastAPI, Next.js 15, PostgreSQL (pgvector), Docker, MCP.

---

### 📌 Progress Update (Initialization Refactor)

* [x] Monorepo aligned with `creatory_core/`, `creatory_studio/`, `mcp/`, `workflows/`, `infra/`.
* [x] Base PAL endpoints added (`catalog`, `test connection`, `routing preview`).
* [x] Hybrid RAG query endpoint + citation-style response scaffold added.
* [x] Bridge Injector runtime connected for side-thread -> main-thread context block injection.
* [x] Starter workflow templates moved to `workflows/templates/`.
* [x] Workflow tables and bootstrap runner/viewer landed for the first static template path.

---

### 🔀 Delivery Pivot (Workflow-First)

For the next delivery slice, **workflow execution, automation, and MCP-backed module
composition move up to Phase 1**.

- The immediate goal is to prove the **execution kernel** of Creatory first:
  reusable workflows, scheduling, HITL, auditability, and module execution.
- **Native chat and model-first UX are intentionally de-emphasized for now.**
  During this slice, the team MAY use existing operator tools such as
  **Codex** and **Claude Code** for workflow authoring, assisted execution, and
  manual testing.
- This is a **delivery-order change**, not a product-scope reduction. Product
  requirement priorities in the BRD remain valid; we are simply pulling the
  OPERATE pillar forward because it de-risks the core platform sooner.

---

### 📦 Phase 1: Workflow Kernel & Automation Slice (Week 1 - 4)
**Goal:** Build a reusable, schedulable workflow kernel and **01 complete flow**
that can run manually or autonomously with explicit HITL and MCP-backed modules.

#### 1. Workflow Runtime Correctness (Week 1)
* **Graph Execution Core:**
  * [ ] Update the workflow runner to execute by **edge traversal** in topological order.
  * [ ] Reject `router` and `memory` in template validation until they are designed.
  * [ ] Preserve `WAITING_HUMAN` as a durable run state and add **approve/resume** flow.
  * [ ] Add step-level tracing that makes node eligibility, execution, skip, and pause states auditable.
* **Template Contracts:**
  * [ ] Add template `inputs` and bind them into runs via `input_json`.
  * [ ] Add reserved support hooks for `join_policy` and per-node `output_schema`.
  * [ ] Keep `condition_expr` disabled until the expression grammar is designed.

#### 2. Automation Contracts & Scheduler (Week 2)
* **Run Model:**
  * [ ] Add `run_mode` (`interactive` / `autonomous`) to workflow runs.
  * [ ] Add `trigger_id` to workflow runs and persist trigger provenance.
  * [ ] Add node `cache_key` support for idempotent re-runs.
* **Triggers & Policies:**
  * [ ] Add trigger CRUD for `manual`, `scheduled`, and `event`.
  * [ ] Implement `hitl_policy`: `approve_to_publish`, `pause_resume`, `auto_approve`.
  * [ ] Add sink configuration: Asset Library draft or MCP publish target.
  * [ ] Add bounded retry / backoff / dead-letter handling for autonomous runs.

#### 3. MCP / Module Execution Layer (Week 3)
* **Execution Adapters:**
  * [ ] Replace mock MCP invocation with real transport-backed execution.
  * [ ] Support the minimum viable server/tool registry needed for workflow steps.
  * [ ] Add secure config/secret resolution for module execution.
* **Module Set for the First Flow:**
  * [ ] Research/search module.
  * [ ] File/document ingestion module.
  * [ ] Media generation module set (`image`, `tts`, optionally `video`).
  * [ ] Publish/export module via MCP sink.

#### 4. Thin Operator Surface (Week 4)
* **Control Plane, Not Chat-First UI:**
  * [ ] Template CRUD and run APIs finalized for operator use.
  * [ ] Trigger CRUD and schedule inspection.
  * [ ] Run detail, step detail, approval queue, and resume/approve endpoints.
  * [ ] Minimal Studio or admin surface for viewing runs and approving human gates.
* **Authoring Mode for This Slice:**
  * [ ] Accept manual YAML/JSON template authoring.
  * [ ] Accept Codex / Claude Code-assisted authoring as an interim operator workflow.
  * [ ] Defer native Director-generated workflow authoring to a later phase.

#### 5. End-to-End Demo Outcome
* [ ] Author a workflow template for a repeatable content task.
* [ ] Run it manually with `interactive` mode and pause at a `human_gate`.
* [ ] Approve/resume and complete the run to a draft asset or MCP sink.
* [ ] Re-run the same workflow with new `inputs`.
* [ ] Schedule the workflow as an `autonomous` run with an auditable trigger.

---

### 🧱 Phase 2: Operator Studio, Knowledge, and Local-First (Week 5 - 8)
**Goal:** Make the workflow kernel practical for repeated daily operation without
depending on the future chat surface.

#### 1. Operator Surfaces & Review UX (Week 5-6)
* [ ] Approval inbox for HITL-gated runs.
* [ ] Run history, retry controls, failure logs, and trigger health.
* [ ] Asset draft review and sink status tracking.

#### 2. Settings, Knowledge, and Asset Contracts (Week 6-7)
* [ ] Workspace/project settings for module and provider overrides where needed.
* [ ] Knowledge ingestion beyond bootstrap: PDF, MD, Docx, transcript-like sources.
* [ ] Asset Library integration as a first-class workflow sink/source.

#### 3. Local-First Operations (Week 8)
* [ ] Package a `local-only` Docker Compose profile for the workflow stack.
* [ ] Validate local-first execution paths for search, storage, and media modules.
* [ ] Harden secret/config handling for self-hosted operators.

---

### 🛠️ Phase 3: Director-Native Authoring, Chat, and Visual Editing (Week 9 - 12)
**Goal:** Bring back the conversational product layer on top of a stable execution
kernel.

#### 1. Director-Native Workflow Authoring (Week 9-10)
* [ ] Implement the Director path that emits workflow traces/graphs from user intent.
* [ ] Allow saving successful traces as reusable workflow templates.
* [ ] Re-introduce model/provider routing as a product-native capability rather than an operator-only tool.

#### 2. Chat and Dual-Stream UX (Week 10-11)
* [ ] Main conversation UI and project-aware chat state.
* [ ] Contextual sub-thread UX and Bridge-powered apply-to-main flow.
* [ ] Streaming responses and model-native orchestration polish.

#### 3. Visual Authoring & Beta Hardening (Week 12)
* [ ] Upgrade workflow viewer into richer authoring/debugging tools.
* [ ] Add analytics: run cost, latency, failure classes, trigger outcomes.
* [ ] Prepare release documentation and installation guidance.

---

### ✅ Contributor Checklist

To ensure progress, you can create GitHub Issues based on this checklist:

**Backend (Python/FastAPI):**
- [ ] Implement graph-based `WorkflowRuntime` traversal over `workflow_edges`.
- [ ] Add template `inputs`, binding resolution, and reserved-type validation.
- [ ] Build HITL resume/approve APIs and durable waiting-state handling.
- [ ] Add `Trigger` models, scheduler integration, and `run_mode` support.
- [ ] Replace mock MCP invocation with transport-backed execution adapters.
- [ ] Add node retry policy, dead-letter handling, and `cache_key` support.

**Frontend / Operator Surface:**
- [ ] Build workflow run viewer with step states and human-gate actions.
- [ ] Build trigger management and schedule inspection UI.
- [ ] Build approval queue and draft asset review surface.
- [ ] Keep native chat UX scoped down until the execution kernel is stable.

**DevOps / Platform:**
- [ ] Add worker/scheduler process for autonomous runs.
- [ ] Harden secret storage for module/provider configs.
- [ ] Package `local-only` stack profile for self-hosted operators.
- [ ] Add observability for trigger outcomes and workflow step failures.

---

With this roadmap, Creatory solves the current sequencing problem by proving the
hardest part of the platform first:
1. **Phase 1 proves execution:** workflows, automation, MCP modules, and HITL.
2. **Phase 2 makes it operable daily:** review, settings, local-first workflows.
3. **Phase 3 restores the full product surface:** Director-native authoring, chat,
   and richer visual UX on top of a stable kernel.
