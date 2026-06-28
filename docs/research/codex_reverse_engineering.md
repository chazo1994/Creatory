# Codex Reverse Engineering Reference

## 0. Document Control

| Field | Value |
| --- | --- |
| Document Type | External Reference / Architecture Research |
| Status | Active |
| Owner | Core Maintainers |
| Version | v0.3 |
| Last Updated | 2026-06-28 |
| Reference Repo | `openai/codex` |
| Scope | Reverse-engineering for architecture learning only |

---

## 1. Purpose

This document captures how `openai/codex` is structured so the Creatory team can use it as an architecture reference while evolving the local orchestration runtime.

This document is **not**:

- a proposal to vendor Codex source into Creatory
- a proposal to replace the Creator-first interaction model
- a requirement to mirror Codex feature-for-feature

This document **is**:

- a map of Codex runtime layers
- a reverse-engineered description of the main execution flow
- a breakdown of Codex tools, MCP, apps, plugins, and skills surfaces
- a translation layer from Codex concepts into Creatory concepts

Reference-only guardrail:

- Codex may be cloned locally for reading under `.references/` or outside this repo.
- Codex source must not be imported, vendored, or wired into Creatory runtime/build paths.
- Architectural ideas may be re-expressed in Creatory, but upstream code should not be copied wholesale.
- If a Codex pattern strongly influences a Creatory design, cite the upstream file or document in the relevant RFC or research note.

---

## 2. Reading Notes

To keep the research honest, this document uses two labels:

- `Observed`: directly grounded in the inspected Codex source tree or project docs
- `Inference`: a conclusion drawn from multiple source files, but not stated as a single explicit sentence upstream

Unless otherwise noted, claims below are `Observed`.

Reference policy details are captured in [reference_policy.md](./reference_policy.md).

---

## 3. Reference Scope

The following Codex materials were reviewed on **2026-06-27**:

- Root repository overview: <https://github.com/openai/codex>
- Workspace layout: <https://github.com/openai/codex/blob/main/codex-rs/Cargo.toml>
- CLI entrypoint: <https://github.com/openai/codex/blob/main/codex-rs/cli/src/main.rs>
- App-server protocol: <https://github.com/openai/codex/blob/main/codex-rs/app-server/README.md>
- Runtime module map: <https://github.com/openai/codex/blob/main/codex-rs/core/src/lib.rs>
- Main session runtime: <https://github.com/openai/codex/blob/main/codex-rs/core/src/session/mod.rs>
- Thread manager: <https://github.com/openai/codex/blob/main/codex-rs/core/src/thread_manager.rs>
- Thread runtime facade: <https://github.com/openai/codex/blob/main/codex-rs/core/src/codex_thread.rs>
- Task runtime: <https://github.com/openai/codex/blob/main/codex-rs/core/src/tasks/mod.rs>
- Context assembly layer: <https://github.com/openai/codex/blob/main/codex-rs/core/src/context/mod.rs>
- AGENTS.md ingestion: <https://github.com/openai/codex/blob/main/codex-rs/core/src/agents_md.rs>
- MCP capability layer: <https://github.com/openai/codex/blob/main/codex-rs/core/src/mcp.rs>
- Context fragment types: <https://github.com/openai/codex/blob/main/codex-rs/context-fragments/src/lib.rs>
- Thread persistence: <https://github.com/openai/codex/blob/main/codex-rs/thread-store/src/lib.rs>
- Runtime state DB: <https://github.com/openai/codex/blob/main/codex-rs/state/src/lib.rs>
- Multi-agent mode logic: <https://github.com/openai/codex/blob/main/codex-rs/core/src/session/multi_agents.rs>
- Child-thread graph store: <https://github.com/openai/codex/blob/main/codex-rs/agent-graph-store/src/lib.rs>

The following Creatory files were used for comparison:

- [creatory_core/services/director.py](../../creatory_core/services/director.py)
- [creatory_core/services/workflow_runner.py](../../creatory_core/services/workflow_runner.py)
- [creatory_core/services/bridge.py](../../creatory_core/services/bridge.py)
- [creatory_core/db/models.py](../../creatory_core/db/models.py)
- [creatory_core/api/routes/conversations.py](../../creatory_core/api/routes/conversations.py)
- [creatory_core/api/routes/mcp.py](../../creatory_core/api/routes/mcp.py)
- [docs/02-design/architecture.md](../02-design/architecture.md)

---

## 4. Monorepo Topology

### 4.1 What the Repository Actually Is

`Observed`

Codex is not a single CLI binary with a few helper modules. It is a fairly large Rust workspace with multiple surfaces and runtime subsystems.

From the workspace definition and module exports, the repo is organized roughly like this:

```text
openai/codex
  -> cli / tui / app-server / mcp-server
  -> core runtime
  -> thread persistence and state DB
  -> context fragments and prompt layers
  -> MCP, skills, apps, plugins, connectors
  -> multi-agent graph and identity support
```

### 4.2 Practical Layering

`Observed`

The repo can be understood in 5 large bands:

1. Surface layer
   - CLI
   - TUI
   - app-server
   - MCP server entrypoints

2. Runtime/control layer
   - `ThreadManager`
   - `CodexThread`
   - session runtime
   - task orchestration

3. Context/prompt layer
   - typed context fragments
   - AGENTS.md ingestion
   - prompt templates

4. Capability layer
   - MCP runtime manager
   - skills
   - apps/connectors
   - plugins/hooks
   - dynamic tools

5. Persistence/state layer
   - thread store
   - runtime state DB
   - agent graph storage

This is important because it shows Codex is not architected as “chat handler + tool calls”. It is closer to an operating runtime with protocol frontends.

### 4.3 Key Crates and Runtime Roles

`Observed`

The following crates/modules are especially important for understanding Codex:

| Crate / Module | Role in the System |
| --- | --- |
| `cli` | CLI entry surface and command routing |
| `app-server` | JSON-RPC server surface for richer clients |
| `core/session` | Main execution runtime |
| `core/thread_manager` | Live thread control plane |
| `core/codex_thread` | Thread-scoped runtime facade |
| `core/tasks` | Explicit task kinds and task lifecycle |
| `core/context` | Model-visible context assembly |
| `core/mcp` | MCP capability/config manager |
| `core/agents_md` | Project instruction ingestion from `AGENTS.md` |
| `thread-store` | Storage-neutral thread persistence |
| `state` | Runtime state/metadata persistence |
| `context-fragments` | Shared structured context fragment types |
| `agent-graph-store` | Parent/child agent-thread topology |

---

## 5. Core Architecture Layers

### 5.1 Surface Protocols

`Observed`

Codex exposes multiple entry surfaces:

- CLI flow via `codex-rs/cli`
- interactive TUI
- `app-server`, which exposes a JSON-RPC 2.0 protocol
- MCP-facing surfaces

The app-server is particularly important for reverse-engineering because it describes the runtime in terms of `Thread`, `Turn`, and `Item`, which is more revealing than a CLI-only view.

### 5.2 ThreadManager as Control Plane

`Observed`

`ThreadManager` is the central control-plane object for live threads. Its job is not model prompting. Its job is to coordinate:

- thread creation/resume/fork
- runtime dependency injection
- environment selection
- auth/model managers
- skills/plugins/apps
- MCP manager
- persistence store
- optional child-thread graph

`Inference`

Architecturally, `ThreadManager` is the “runtime kernel edge” where protocol/UI surfaces hand work to the actual execution engine.

### 5.3 CodexThread as Thread Runtime Facade

`Observed`

`CodexThread` carries a thread-scoped snapshot of runtime configuration and provides thread-level operations such as:

- submitting a turn
- steering input while running
- injecting input if running
- inspecting token usage
- reading MCP resources
- calling MCP tools
- exposing runtime MCP config

This makes the thread a first-class live unit, not just a persistence row.

### 5.4 Session Runtime

`Observed`

The session module is the deepest runtime core. It manages:

- active work inside a thread
- turn/task lifecycle
- event emission
- runtime cancellation/interrupts
- context updates
- interaction with tools/MCP
- policy, budget, and runtime metadata

`Inference`

If Creatory needs one “missing architecture layer” the most, this is it. Today `director.py` is doing a thin version of orchestration, but not a session runtime.

### 5.5 Task Runtime

`Observed`

Codex has explicit task types in the runtime rather than one generic “assistant run”. The task module includes multiple kinds such as regular turns, review flows, compaction, and shell-related tasks.

This means:

- turns can execute under different policies
- cancellation is a first-class concern
- observability has a stable unit smaller than “whole thread”

### 5.6 Context Assembly Layer

`Observed`

Codex has a dedicated context system and separate context fragment crates/modules. The core context module references many specialized fragments such as:

- permissions
- skills
- apps
- plugins
- user instructions
- rollout/token budgets
- subagent notifications
- world state

`Observed`

`agents_md.rs` separately discovers and ingests `AGENTS.md` instructions from the working project tree.

`Inference`

This is a major design decision: Codex treats “what the model sees” as a structured assembly problem, not as one big string generated inline in service code.

### 5.7 Capability Layer

`Observed`

Codex keeps MCP runtime configuration behind a dedicated manager. The capability side also spans:

- skills
- apps
- plugins
- connectors
- hooks
- dynamic tools

This keeps the runtime extensible without collapsing tool logic into the session core.

### 5.8 Persistence Layer

`Observed`

Codex separates persistence concerns:

- `thread-store`: storage-neutral thread persistence interfaces
- `state`: SQLite-backed runtime state and metadata
- `agent-graph-store`: storage for parent/child thread topology

`Inference`

This split is useful because “thread transcript persistence”, “runtime metadata”, and “agent topology” are not forced into one storage model.

### 5.9 Safety and Governance Layer

`Observed`

Codex runtime carries explicit concepts for:

- approval policy
- permission profile
- workspace roots
- environment selection
- budget/token state

The runtime is therefore aware of execution policy, not just output generation.

---

## 6. Codex Runtime Flow

### 6.1 External Lifecycle

`Observed`

From the app-server protocol, the outer lifecycle looks like this:

```text
client
  -> initialize
  -> thread/start | thread/resume | thread/fork
  -> turn/start
  <- turn/item started/delta/completed events
  <- turn/completed
```

This is a strong signal that the real source-of-truth is not “chat request/response”, but a persistent thread with turn-level execution.

### 6.2 Expanded Runtime Sequence

`Inference`

Based on the thread manager, thread runtime, session runtime, task module, and app-server docs, the flow can be expanded like this:

```text
1. client initializes transport/session
2. client creates or resumes a thread
3. ThreadManager constructs a thread runtime
4. thread snapshot binds:
   - model/provider config
   - approval policy
   - permission profile
   - workspace roots
   - environment selections
   - skills/apps/plugins/MCP visibility
5. client starts a turn
6. session runtime builds model-visible context
7. session runtime selects or spawns a task kind
8. task executes, possibly:
   - reasoning over context
   - calling MCP tools
   - using shell/process/file capabilities
   - asking for user input or approvals
   - spawning child-thread work
9. item events stream out incrementally
10. turn completes and state is persisted
```

### 6.3 Thread Start, Resume, and Fork

`Observed`

Codex distinguishes:

- `thread/start`
- `thread/resume`
- `thread/fork`

That tells us a thread is treated as a durable runtime identity with lineage, not as a disposable request context.

`Inference`

Forking is especially important because it implies the runtime supports branching explorations without mutating the original thread state in place.

### 6.4 Turn Semantics

`Observed`

A turn is not just one model completion. It is the lifecycle envelope around:

- context preparation
- model work
- tool activity
- streamed events
- completion or interruption

This is much richer than storing a single assistant message.

### 6.5 Item/Event Stream

`Observed`

The app-server README describes item-based streaming during a turn.

`Inference`

This suggests the client can render progress at a finer granularity than “assistant is typing”. It can potentially distinguish:

- text generation progress
- tool activity
- approvals/user-input requests
- task transitions
- subagent or background activity

### 6.6 Interruptions and Steering

`Observed`

`CodexThread` supports operations such as steering input and injecting while a run is active.

`Inference`

This means Codex is built for interactive control during execution, not only for fire-and-forget requests.

---

## 7. Tool System and Capability Model

### 7.1 Important Distinction

`Observed`

Codex exposes both:

- client/server RPC methods
- model/runtime tools and capabilities

These are related, but not identical.

For example, an app-server method such as shell execution is part of the runtime surface. Whether and how that becomes model-visible depends on session policy, tool availability, and runtime configuration.

### 7.2 Major Capability Families

`Observed`

From the app-server and core runtime shape, Codex capability surface spans:

- local shell/process execution
- filesystem operations
- MCP tools and resources
- skills
- apps/connectors
- plugins
- hooks
- plan/goal/user-input flows

| Capability Family | What It Is Doing Architecturally |
| --- | --- |
| Shell/process | Lets the runtime act on the local execution environment |
| Filesystem/workspace | Exposes governed file and workspace operations |
| MCP | Connects thread runtime to external tools/resources with structured contracts |
| Skills | Supplies reusable instruction/workflow knowledge units |
| Apps/connectors | Bundles higher-level external capability surfaces |
| Plugins/hooks | Extends runtime behavior and capability registration |
| Planning/goal/user-input | Gives coordination and elicitation primitives a first-class API |

### 7.3 Shell and Process Capabilities

`Observed`

The app-server describes thread-level shell command operations such as `thread/shellCommand`.

`Inference`

This tells us Codex is not only a text agent. It is built as an execution-oriented coding runtime where shell/process work is normal, not bolted on.

### 7.4 File and Workspace Capabilities

`Observed`

The runtime carries concepts such as:

- workspace roots
- permission profiles
- file-oriented operations in the app-server surface

This means filesystem access is treated as a governed capability, not a hidden implementation detail.

### 7.5 MCP Capabilities

`Observed`

MCP is a first-class runtime concern:

- runtime MCP configuration is exposed per thread
- thread runtime can read MCP resources
- thread runtime can call MCP tools
- a dedicated MCP manager resolves config across runtime sources

`Inference`

Codex does not treat MCP as “just another HTTP call”. It treats it as part of the thread’s capability envelope.

### 7.6 Skills

`Observed`

The app-server includes skill discovery surfaces such as `thread/skills/list`.

`Inference`

Skills appear to function as instruction packages or workflow knowledge units that can be surfaced to the runtime and, through context assembly, influence model behavior without hard-coding everything into prompts.

### 7.7 Apps and Connectors

`Observed`

The app-server includes app discovery surfaces such as `thread/app/list`.

`Inference`

Apps/connectors appear to represent capability bundles that can be made available through a higher-level app abstraction rather than raw one-off tool definitions.

### 7.8 Plugins and Hooks

`Observed`

The repo structure and runtime surface indicate explicit support for plugins and hooks.

`Inference`

This means Codex is designed to let external behavior extend either:

- the capability catalog
- the runtime environment
- or the context/instruction system

without turning the core session engine into a large switch statement.

### 7.9 Plan, Goal, and User-Input Utilities

`Observed`

Codex also includes explicit operations related to:

- plan updates
- goal tracking
- user input requests

These are notable because they show coordination primitives are part of the runtime API itself, not only something improvised inside model output text.

### 7.10 Approval and Permission Model

`Observed`

Codex runtime carries approval and permission concepts at the thread/session level.

`Inference`

This likely explains why tool use can be mediated consistently across shell, filesystem, apps, and MCP. The policy sits above individual tool types.

---

## 8. Multi-Agent Model

### 8.1 What "Multi-Agent" Means in Codex

`Observed`

Codex contains:

- multi-agent mode logic
- child-thread graph storage
- agent identity support

This indicates multi-agent behavior is a real architecture concern, not only a prompt convention.

### 8.2 Thread-Centric Multi-Agent Topology

`Observed`

Codex is closer to this model:

```text
root thread
  -> child thread
  -> child thread
  -> child thread
```

than this model:

```text
agent row
  -> task row
  -> child task row
```

This matters because every child thread can carry:

- its own runtime config snapshot
- its own event stream
- its own context window and history
- its own tool visibility or policy

### 8.3 Multi-Agent Modes

`Observed`

The multi-agent module includes an `ExplicitRequestOnly` mode and logic tied to reasoning effort, including an `Ultra` case.

`Inference`

This suggests Codex can vary how proactively it fans out sub-agent behavior depending on runtime mode, not only on user prompting.

### 8.4 Why This Matters for Creatory

`Inference`

Creatory's existing dual-thread idea is actually very compatible with this pattern:

- main thread as strategic source-of-truth
- quick/context threads as isolated workspaces
- future specialist agents as explicit child threads

The part missing in Creatory is not the product concept. It is the live runtime abstraction.

---

## 9. State, Persistence, and Replay

### 9.1 Thread Store

`Observed`

Codex ships a storage-neutral thread persistence interface.

This implies the runtime can persist thread history and identity independently of a specific UI or transport surface.

### 9.2 Runtime State DB

`Observed`

Codex also uses a SQLite-backed state layer for runtime metadata.

The state crate is intentionally narrower than the whole session system.

`Inference`

This is a healthy split:

- transcript-like thread state belongs to a thread store
- runtime bookkeeping and derived metadata belong to a state DB

### 9.3 Replay and Auditability

`Inference`

Because the architecture is thread/turn/event oriented, it naturally supports:

- replay
- audit
- usage reporting
- post-mortem analysis
- richer frontend state reconstruction

This is harder to do cleanly in systems that only store raw messages and final tool outputs.

---

## 10. Mapping: Codex vs Creatory Today

| Topic | Codex Pattern | Creatory Current State | Gap |
| --- | --- | --- | --- |
| Runtime anchor | Thread/session is the live unit | `AgentRun` + `Task` are the main execution traces | Creatory lacks a true thread runtime |
| Thread lifecycle | Start, resume, fork are explicit | Threads are persisted, but not used as live runtime objects | No runtime thread manager |
| Turn lifecycle | Explicit `turn/start -> stream -> complete` | `director.py` writes one user message, one assistant message, and static tasks | No evented turn model |
| Context model | Structured fragments + AGENTS.md ingestion | Director assembles response text directly | No dedicated context assembler |
| Task model | First-class runtime task kinds | Planning/content are stored as DB tasks after the fact | No task runtime |
| Multi-agent | Child-thread graph | Parent-child thread data exists, but not used as sub-agent runtime | No spawned sub-thread execution |
| Workflow execution | Runtime can dispatch different task kinds and capabilities | `workflow_runner.py` is sequential and mostly stubbed | No real agent/tool node dispatch |
| MCP layer | Runtime capability manager | `mcp.py` stores catalog data and mock invocations | No live MCP runtime binding |
| Permissions | Runtime policy is attached to thread/session | Creatory has basic app permissions, but not thread runtime policy | Missing execution governance layer |
| Human-in-the-loop | Runtime can pause, request approval, and continue | Workflow runner supports `WAITING_HUMAN` | Good base, but still isolated |

---

## 11. What Creatory Should Learn from Codex

### 11.1 Promote Thread Runtime to a First-Class Concept

Creatory already has the right data skeleton:

- `Conversation`
- `Thread`
- `Message`
- `ContextInjection`

The next step is to let `Thread` become a live runtime unit, not just a storage grouping.

### 11.2 Add Turn and TurnEvent

Recommended direction:

```text
Conversation
  -> Thread
    -> Turn
      -> TurnEvent
      -> TaskExecution
```

This would immediately help:

- SSE streaming
- workflow state reflection
- pause/resume
- incremental UI rendering
- tool-call visibility
- audit/replay

### 11.3 Separate Context Assembly from Director Logic

Today, [`director.py`](../../creatory_core/services/director.py) mixes:

- message creation
- agent resolution
- plan construction
- provider routing
- final response assembly

Codex suggests a cleaner split:

```text
ThreadRuntime
  -> ContextAssembler
  -> TaskRuntime
  -> CapabilityManager
  -> EventStream
```

### 11.4 Keep MCP Behind a Capability Manager

Creatory should avoid letting the Director know transport details of tool execution.

Preferred direction:

```text
Director / Workflow node
  -> CapabilityManager
    -> MCP runtime client
      -> tool server
```

### 11.5 Use Child Threads for Future Sub-Agents

This aligns extremely well with the Creator-first interaction model:

- main thread remains source-of-truth
- quick/context threads remain isolated
- promoted context still goes through bridge semantics
- future specialist agents can be child threads rather than awkward nested tasks

---

## 12. What Should Stay Reference-Only

The goal is to learn from Codex, not to clone it.

The following should remain reference-only for now:

- the full Codex app-server protocol surface
- Codex-specific CLI/TUI/Desktop concerns
- shell-heavy local execution semantics
- plugin marketplace scale-out behavior
- deeper agent identity and attestation layers

These are powerful ideas, but they are not prerequisites for Creatory V0 or even early V1.

---

## 13. Summary

The main lesson from Codex is not “add more agents”.

The main lesson is:

> Treat orchestration as a thread/session runtime with explicit turns, events, policies, and capabilities.

Creatory already has a product vision compatible with that direction:

- dual-thread interaction
- explicit context injection
- workflow/HITL separation
- MCP-first extensibility

What is still missing is the runtime backbone that makes those ideas first-class in code.

---

## 14. Reference-Only Policy Reminder

This document exists to help the team study Codex safely.

Allowed:

- clone Codex into a gitignored reference folder such as `.references/openai-codex/`
- inspect source layout, runtime flow, and architectural patterns
- write internal notes, RFCs, and diagrams based on those observations

Not allowed:

- import Codex crates, packages, or runtime modules into Creatory
- vendor Codex source into `creatory_core/`, `creatory_studio/`, `mcp/`, or `workflows/`
- add Codex as a production dependency, build dependency, or submodule for app runtime
- copy upstream code into Creatory without an explicit legal and architectural decision
