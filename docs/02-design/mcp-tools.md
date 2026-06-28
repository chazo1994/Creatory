# 🛠️ Tools & MCP Extension Layer (Design Layer)

> **Layer:** Design (normative). Traces up to
> [`../01-concept/business-requirements.md`](../01-concept/business-requirements.md)
> FR-05/FR-06 and NFR (Extensibility).

## Principles

- **MCP (Model Context Protocol)** MUST be the primary extension mechanism for the
  tool ecosystem.
- The runtime core MUST be separated from tool/provider-specific logic — adding a
  tool MUST NOT require changing the core orchestrator.
- Tool contracts MUST define clear **input schema, output schema, and error
  shapes**.
- Contributor guidance for MCP tools MUST live in
  [`../../CONTRIBUTING.md`](../../CONTRIBUTING.md).

## Structure

| Part | Responsibility |
| --- | --- |
| `mcp/servers/` | Independent tool servers (media gen, web search/scrape, git, etc.). |
| `mcp/registry/` | Tool discovery + manifests so the Director can find tools dynamically. |
| `mcp/sdk/` | Protocol communication layer. |

## Relationship to workflows

A workflow `tool` node references a tool group from the registry (see
[workflow-model.md](workflow-model.md) §3). Tool input/output schemas are what make
a node's `output_schema` validation possible.

## Data contracts

See [data-model.md](data-model.md) §6 (`mcp_servers`, `mcp_tools`,
`tool_invocations`).
