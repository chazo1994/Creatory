# 🏗️ Architecture (Design Layer)

> **Layer:** Design. Structural "how": module responsibilities and how modules
> communicate. Code-agnostic but precise. Traces up to
> [`../01-concept/vision.md`](../01-concept/vision.md). Current build status lives
> in [`../03-implementation/v0-snapshot.md`](../03-implementation/v0-snapshot.md),
> **not here**.

## 1. Module Map

```text
creatory/
├── creatory_core/      # Backend engine ("the brain")
│   ├── agents/         # Director + specialized agent personas
│   ├── providers/      # Provider Abstraction Layer (PAL): LLM/media vendors
│   ├── api/            # HTTP interface (versioned via URL routing)
│   ├── db/             # Persistent + vector storage
│   ├── rag/            # Hybrid knowledge retrieval (vector + graph)
│   └── services/       # Core business logic: Director, Bridge, Workflow Runtime
├── creatory_studio/    # Frontend studio ("the workshop", Next.js)
├── mcp/                # External tool servers (Model Context Protocol)
│   ├── servers/        # Individual tool servers (media, web, git)
│   ├── registry/       # Tool discovery & manifests
│   └── sdk/            # Protocol communication layer
├── workflows/          # Shared workflow blueprints
│   ├── templates/      # Reusable pipeline recipes (YAML)
│   └── schemas/        # JSON schema contracts validating templates
├── docs/               # This documentation
└── infra/              # Deployment & CI/CD
```

## 2. Module Responsibilities

| Module | Responsibility |
| --- | --- |
| `creatory_core/agents/` | Hosts the **Director** (planning/delegation) and specialized agents. Maintains long-term project context. |
| `creatory_core/providers/` | **PAL** — decouples the system from specific AI vendors (local or cloud). |
| `creatory_core/api/` | Gateway exposing functionality to the Studio. Versioning via routing prefix, keeping the folder layout flat. |
| `creatory_core/rag/` | Hybrid knowledge engine combining semantic (vector) and relational (graph) retrieval. |
| `creatory_core/services/` | Glue logic: the **Bridge** (sub-thread → main-thread context) and the **Workflow Runtime** (executes node/edge templates). |
| `creatory_studio/` | Chat-first UX, contextual popups, injection UI, workflow visualization, settings. See [frontend.md](frontend.md). |
| `mcp/` | Keeps the core lean: capabilities live as independent tool servers discovered via the registry. See [mcp-tools.md](mcp-tools.md). |
| `workflows/` | Shareable pipeline definitions and their validation schemas. See [workflow-model.md](workflow-model.md). |

> Detailed orchestration responsibilities (Director vs Workflow Runtime vs Bridge)
> are normative and specified in [orchestration.md](orchestration.md).

## 3. Module Communication

1. **Streaming (SSE):** `creatory_core` streams AI responses to `creatory_studio`
   for a live chat experience.
2. **Context Injection (Bridge):** Promoting a sub-thread merges its context block
   into the main thread state as a system-level update — through the Bridge only.
3. **Visual Sync:** The workflow viewer receives real-time node progress as a run
   advances.
4. **Tool Execution (MCP):** Agents call tools over the MCP standard, so any
   community-built tool integrates without core changes.

## 4. Cross-Cutting Design Principles

- **Vendor independence:** the core orchestrator MUST NOT be coupled to
  vendor-specific APIs; isolation lives in PAL and MCP.
- **Multi-modal by design:** RAG and storage handle text, image metadata, and
  audio transcripts, not just text.
- **Separation of concerns:** AI reasoning (`creatory_core`) is cleanly separated
  from the user workspace (`creatory_studio`) and from capabilities (`mcp`).
