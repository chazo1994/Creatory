# ⚙️ Automation — Re-use & Autonomous Production (Design Layer)

> **Layer:** Design (normative). Specifies how a trusted, Director-generated
> workflow becomes a **repeatable, schedulable content-production unit**. This is
> the **OPERATE** pillar — arguably the platform's long-term moat: "set it once,
> produce content on a cadence." Traces up to
> [`../01-concept/business-requirements.md`](../01-concept/business-requirements.md)
> **FR-04B** (Workflow Re-use & Automation) and
> [`../01-concept/vision.md`](../01-concept/vision.md) §3 (*idea → finished
> product*). Builds on [workflow-model.md](workflow-model.md) §9–§11.

## 1. Why automation requires the *static* graph

The Director remains the system's planner — its work is **not** thrown away in
production; it is *frozen into the graph*. The Director-as-actor simply is not
invoked at run time in autonomous mode (§1 decision below).
What is unsuitable for production is **re-planning from scratch on every run** (the
Director's *dynamic* mode): it is costly, non-deterministic, and needs a human
conversation. Automation instead **amortizes** the Director's planning — plan once,
freeze it into a graph — and **re-runs the frozen graph**, because production needs:

- Repeatable structure and predictable cost.
- Headless execution — **no human in the loop**, and the Director is
  **compile-time only** (decision below): it produced the graph at authoring time;
  at run time the Runtime executes that graph deterministically and does **not**
  re-invoke the Director.
- Scheduling / triggering and horizontal scale (run N times).
- Stable, auditable output.

**Sweet spot:** the topology is frozen, but each `agent`/`tool` node stays
*agentic* — it reasons over fresh input. The Director's *planning* is amortized
into the frozen graph; its *reasoning* persists as the agent nodes the graph runs.
The Director-as-actor does not re-enter at run time. Repeatable, not robotic.

> **Design-led decision (Director scope in autonomous runs): compile-time only.**
> In autonomous mode the Director's sole role is to have generated the graph during
> authoring. It does **not** supervise, handle exceptions, or re-plan mid-run.
> Run-time behavior is entirely the Runtime's: deterministic graph traversal plus
> the non-interactive recovery in §6. Rationale: maximum determinism, predictable
> cost, and a clean split — **Director = planning, Runtime = execution**. If a run
> genuinely needs the Director again, that is an explicit, creator-initiated
> **re-plan** ([workflow-model.md](workflow-model.md) §11), never an automatic
> in-run intervention.

## 2. Run modes

A `Workflow Run` executes in one of:

| `run_mode` | Human present? | HITL handling | Typical trigger |
| --- | --- | --- | --- |
| `interactive` | Yes | Synchronous gate (blocks for approval) | Manual run from Studio |
| `autonomous` | No | **Async** gate (see §4) | Schedule / event |

The same template runs in either mode; mode is a property of the **run/trigger**,
not the template.

## 3. Triggers

A **trigger** binds a template (with default inputs) to an activation source.

| Trigger type | Activation | Notes |
| --- | --- | --- |
| `manual` | Creator clicks "Run" | Default; `interactive`. |
| `scheduled` | Cron-like schedule | `autonomous`; e.g. "every day 07:00". |
| `event` | Inbound webhook / new-content signal (new video, RSS item, etc.) | `autonomous`; event payload maps to template `inputs`. |

A trigger MUST record: the template + version, bound/default `inputs`, `run_mode`,
the `hitl_policy` (§4), and the output sink (§5). Triggers MUST be auditable and
individually disableable.

## 4. Async HITL — the core tension of automation

A scheduled 3am run **cannot block on synchronous human approval**. HITL must
survive the absence of a human. Each trigger declares a **`hitl_policy`**:

| `hitl_policy` | Behavior at a `human_gate` | Trade-off |
| --- | --- | --- |
| **`approve_to_publish`** *(default)* | Run completes to a **draft**; output is queued; the run does **not** publish until a human approves the batch later. | Safest. Decouples generation from approval; nothing goes out unreviewed. |
| `pause_resume` | Run sets `WAITING_HUMAN`, sends a notification, and **resumes** when the human approves (possibly hours later). | Keeps a single linear run; needs durable wait + timeout. |
| `auto_approve` | Gate is skipped; run proceeds and publishes. | Fastest, least safe; only for low-risk, well-trusted templates. |

> **Design-led decision (D1): default is `approve_to_publish`.** It preserves the
> Creator-First / creative-sovereignty principle (a human approves what ships)
> while still letting generation run unattended. *(Alternatives above are
> selectable per trigger.)*

> **This is where the durable design pays off.** The `run_status = waiting_human`
> state already persists ([data-model.md](data-model.md) §1 enum; §4–§5 tables).
> An autonomous run
> can sit in `WAITING_HUMAN` for hours and resume later — so `pause_resume` and the
> approval queue are built on a foundation that already exists, not a new
> mechanism. Each gated run MUST be durable across process restarts.

### 4.1 Timeouts
A `pause_resume` or `approve_to_publish` gate SHOULD carry an expiry policy
(e.g. auto-cancel or escalate after N hours) so stuck runs don't accumulate
silently.

## 5. Output sinks

An autonomous run's product MUST go somewhere explicit. The trigger declares a
**sink**:

- **Asset Library** (default) — store as a draft asset for later review.
- **Auto-publish via MCP** — push to an external platform through an MCP tool
  (see [mcp-tools.md](mcp-tools.md)). Auto-publish MUST respect the `hitl_policy`
  (i.e. only after approval unless `auto_approve`).

## 6. Failure handling without a human in the loop

Headless runs have no human to ask, and (per §1) the Director is **not** in the
run-time loop, so the **Runtime alone** MUST define non-interactive recovery:

- **Retry** transient node failures with bounded backoff (counts toward the
  circuit breaker step budget — see [orchestration.md](orchestration.md) §6).
- **Fallback** SHOULD be allowed per node (e.g. cheaper model / alternate tool).
- **Dead-letter**: after retries are exhausted, mark the run `failed`, stop, and
  **alert** the owner. An autonomous run MUST NOT loop indefinitely.

## 7. Data-contract additions (for [data-model.md](data-model.md))

These are required to implement automation and are flagged there as design intent,
source-of-truth being this document:

- Template `inputs` declaration (the signature — [workflow-model.md](workflow-model.md) §10).
- A `triggers` / `schedules` table: template ref + version, `run_mode`,
  `hitl_policy`, default `inputs`, sink, enabled flag, schedule/event config.
- `workflow_runs` gains `run_mode` and the originating `trigger_id`.
- A node-level `cache_key` to support idempotent re-runs
  ([workflow-model.md](workflow-model.md) §11.1).

## 8. Non-goals (current stage)

- No autonomous run MAY publish externally without satisfying its `hitl_policy`.
- Automation MUST NOT silently `re-plan` (regenerate the graph) — scheduled jobs
  use **re-run** (same graph, new inputs); re-plan is an explicit creator action
  ([workflow-model.md](workflow-model.md) §11).
- No unbounded autonomous loops (§6).
