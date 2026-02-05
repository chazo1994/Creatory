# Database Schema Draft

This document proposes the first relational schema for Creatory using:

- PostgreSQL as the primary transactional store.
- pgvector for semantic retrieval.
- Optional graph layer (can be in PostgreSQL first, external graph DB later).

Execution source of truth:

- Alembic revision: `alembic/versions/20260206_0001_base_schema.py`
- SQL migration files: `sql/migrations/0001_base_schema.up.sql`, `sql/migrations/0001_base_schema.down.sql`

The design prioritizes:

- Dual-stream conversation (`main` and `quick` threads).
- Agent orchestration state and task traceability.
- Reusable workflow templates and runtime execution history.
- Hybrid RAG with vector and concept relationship storage.

## 1. Extensions and Enums

```sql
CREATE EXTENSION IF NOT EXISTS pgcrypto;
CREATE EXTENSION IF NOT EXISTS vector;

CREATE TYPE thread_kind AS ENUM ('main', 'quick');
CREATE TYPE message_role AS ENUM ('user', 'assistant', 'tool', 'system');
CREATE TYPE run_status AS ENUM ('queued', 'running', 'waiting_human', 'succeeded', 'failed', 'cancelled');
CREATE TYPE source_type AS ENUM ('url', 'file', 'text', 'image', 'audio', 'video');
CREATE TYPE asset_type AS ENUM ('image', 'video', 'audio', 'document');
CREATE TYPE node_type AS ENUM ('agent', 'tool', 'human_gate', 'router', 'memory');
CREATE TYPE transport_type AS ENUM ('stdio', 'http', 'sse');
```

## 2. Identity and Workspace

```sql
CREATE TABLE users (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  email TEXT UNIQUE NOT NULL,
  password_hash TEXT NOT NULL,
  display_name TEXT,
  avatar_url TEXT,
  created_at TIMESTAMPTZ NOT NULL DEFAULT now(),
  updated_at TIMESTAMPTZ NOT NULL DEFAULT now()
);

CREATE TABLE workspaces (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  name TEXT NOT NULL,
  slug TEXT UNIQUE NOT NULL,
  owner_id UUID NOT NULL REFERENCES users(id),
  created_at TIMESTAMPTZ NOT NULL DEFAULT now(),
  updated_at TIMESTAMPTZ NOT NULL DEFAULT now()
);

CREATE TABLE workspace_memberships (
  workspace_id UUID NOT NULL REFERENCES workspaces(id) ON DELETE CASCADE,
  user_id UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
  role TEXT NOT NULL CHECK (role IN ('owner', 'admin', 'editor', 'viewer')),
  created_at TIMESTAMPTZ NOT NULL DEFAULT now(),
  PRIMARY KEY (workspace_id, user_id)
);
```

## 3. Dual-Stream Conversations

```sql
CREATE TABLE conversations (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  workspace_id UUID NOT NULL REFERENCES workspaces(id) ON DELETE CASCADE,
  creator_id UUID NOT NULL REFERENCES users(id),
  title TEXT,
  status TEXT NOT NULL DEFAULT 'active' CHECK (status IN ('active', 'archived')),
  created_at TIMESTAMPTZ NOT NULL DEFAULT now(),
  updated_at TIMESTAMPTZ NOT NULL DEFAULT now()
);

CREATE TABLE threads (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  conversation_id UUID NOT NULL REFERENCES conversations(id) ON DELETE CASCADE,
  kind thread_kind NOT NULL,
  parent_thread_id UUID REFERENCES threads(id),
  created_by UUID NOT NULL REFERENCES users(id),
  created_at TIMESTAMPTZ NOT NULL DEFAULT now()
);

CREATE TABLE messages (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  thread_id UUID NOT NULL REFERENCES threads(id) ON DELETE CASCADE,
  role message_role NOT NULL,
  content_json JSONB NOT NULL,
  token_count INT,
  created_by UUID REFERENCES users(id),
  created_at TIMESTAMPTZ NOT NULL DEFAULT now()
);

CREATE TABLE context_injections (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  conversation_id UUID NOT NULL REFERENCES conversations(id) ON DELETE CASCADE,
  from_thread_id UUID NOT NULL REFERENCES threads(id) ON DELETE CASCADE,
  from_message_id UUID NOT NULL REFERENCES messages(id) ON DELETE CASCADE,
  to_thread_id UUID NOT NULL REFERENCES threads(id) ON DELETE CASCADE,
  to_message_id UUID REFERENCES messages(id) ON DELETE SET NULL,
  context_block JSONB NOT NULL,
  injected_by UUID NOT NULL REFERENCES users(id),
  created_at TIMESTAMPTZ NOT NULL DEFAULT now()
);

CREATE INDEX idx_messages_thread_created_at ON messages(thread_id, created_at);
CREATE INDEX idx_threads_conversation_kind ON threads(conversation_id, kind);
```

## 4. Agents, Tasks, and Orchestration State

```sql
CREATE TABLE agents (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  workspace_id UUID REFERENCES workspaces(id) ON DELETE CASCADE,
  slug TEXT NOT NULL,
  display_name TEXT NOT NULL,
  persona_prompt TEXT NOT NULL,
  config_json JSONB NOT NULL DEFAULT '{}'::jsonb,
  is_system BOOLEAN NOT NULL DEFAULT false,
  created_at TIMESTAMPTZ NOT NULL DEFAULT now(),
  UNIQUE (workspace_id, slug)
);

CREATE TABLE agent_runs (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  conversation_id UUID REFERENCES conversations(id) ON DELETE SET NULL,
  thread_id UUID REFERENCES threads(id) ON DELETE SET NULL,
  agent_id UUID NOT NULL REFERENCES agents(id),
  status run_status NOT NULL DEFAULT 'queued',
  input_json JSONB NOT NULL DEFAULT '{}'::jsonb,
  output_json JSONB NOT NULL DEFAULT '{}'::jsonb,
  error_json JSONB,
  started_at TIMESTAMPTZ,
  ended_at TIMESTAMPTZ,
  created_at TIMESTAMPTZ NOT NULL DEFAULT now()
);

CREATE TABLE tasks (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  agent_run_id UUID NOT NULL REFERENCES agent_runs(id) ON DELETE CASCADE,
  parent_task_id UUID REFERENCES tasks(id) ON DELETE CASCADE,
  task_type TEXT NOT NULL,
  status run_status NOT NULL DEFAULT 'queued',
  input_json JSONB NOT NULL DEFAULT '{}'::jsonb,
  output_json JSONB NOT NULL DEFAULT '{}'::jsonb,
  error_json JSONB,
  started_at TIMESTAMPTZ,
  ended_at TIMESTAMPTZ,
  created_at TIMESTAMPTZ NOT NULL DEFAULT now()
);

CREATE TABLE task_events (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  task_id UUID NOT NULL REFERENCES tasks(id) ON DELETE CASCADE,
  event_type TEXT NOT NULL,
  payload_json JSONB NOT NULL DEFAULT '{}'::jsonb,
  created_at TIMESTAMPTZ NOT NULL DEFAULT now()
);

CREATE INDEX idx_agent_runs_status_created_at ON agent_runs(status, created_at);
CREATE INDEX idx_tasks_run_status ON tasks(agent_run_id, status);
```

## 5. Workflow Templates and Runtime

```sql
CREATE TABLE workflow_templates (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  workspace_id UUID NOT NULL REFERENCES workspaces(id) ON DELETE CASCADE,
  name TEXT NOT NULL,
  description TEXT,
  version INT NOT NULL DEFAULT 1,
  is_public BOOLEAN NOT NULL DEFAULT false,
  definition_json JSONB NOT NULL DEFAULT '{}'::jsonb,
  created_by UUID NOT NULL REFERENCES users(id),
  created_at TIMESTAMPTZ NOT NULL DEFAULT now(),
  updated_at TIMESTAMPTZ NOT NULL DEFAULT now(),
  UNIQUE (workspace_id, name, version)
);

CREATE TABLE workflow_nodes (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  template_id UUID NOT NULL REFERENCES workflow_templates(id) ON DELETE CASCADE,
  node_key TEXT NOT NULL,
  type node_type NOT NULL,
  config_json JSONB NOT NULL DEFAULT '{}'::jsonb,
  position_x NUMERIC(10,2),
  position_y NUMERIC(10,2),
  UNIQUE (template_id, node_key)
);

CREATE TABLE workflow_edges (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  template_id UUID NOT NULL REFERENCES workflow_templates(id) ON DELETE CASCADE,
  source_node_key TEXT NOT NULL,
  target_node_key TEXT NOT NULL,
  condition_expr TEXT,
  metadata_json JSONB NOT NULL DEFAULT '{}'::jsonb
);

CREATE TABLE workflow_runs (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  template_id UUID NOT NULL REFERENCES workflow_templates(id),
  conversation_id UUID REFERENCES conversations(id) ON DELETE SET NULL,
  status run_status NOT NULL DEFAULT 'queued',
  input_json JSONB NOT NULL DEFAULT '{}'::jsonb,
  output_json JSONB NOT NULL DEFAULT '{}'::jsonb,
  started_at TIMESTAMPTZ,
  ended_at TIMESTAMPTZ,
  created_by UUID NOT NULL REFERENCES users(id),
  created_at TIMESTAMPTZ NOT NULL DEFAULT now()
);

CREATE TABLE workflow_run_steps (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  workflow_run_id UUID NOT NULL REFERENCES workflow_runs(id) ON DELETE CASCADE,
  node_key TEXT NOT NULL,
  status run_status NOT NULL DEFAULT 'queued',
  attempt INT NOT NULL DEFAULT 1,
  input_json JSONB NOT NULL DEFAULT '{}'::jsonb,
  output_json JSONB NOT NULL DEFAULT '{}'::jsonb,
  error_json JSONB,
  started_at TIMESTAMPTZ,
  ended_at TIMESTAMPTZ,
  created_at TIMESTAMPTZ NOT NULL DEFAULT now()
);

CREATE INDEX idx_workflow_runs_template_status ON workflow_runs(template_id, status);
CREATE INDEX idx_workflow_run_steps_run_node ON workflow_run_steps(workflow_run_id, node_key);
```

## 6. MCP Servers, Tools, and Tool Calls

```sql
CREATE TABLE mcp_servers (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  workspace_id UUID NOT NULL REFERENCES workspaces(id) ON DELETE CASCADE,
  name TEXT NOT NULL,
  transport transport_type NOT NULL,
  endpoint TEXT,
  auth_config_json JSONB NOT NULL DEFAULT '{}'::jsonb,
  is_active BOOLEAN NOT NULL DEFAULT true,
  created_at TIMESTAMPTZ NOT NULL DEFAULT now(),
  UNIQUE (workspace_id, name)
);

CREATE TABLE mcp_tools (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  mcp_server_id UUID NOT NULL REFERENCES mcp_servers(id) ON DELETE CASCADE,
  tool_name TEXT NOT NULL,
  description TEXT,
  input_schema JSONB NOT NULL,
  output_schema JSONB,
  capabilities_json JSONB NOT NULL DEFAULT '{}'::jsonb,
  created_at TIMESTAMPTZ NOT NULL DEFAULT now(),
  UNIQUE (mcp_server_id, tool_name)
);

CREATE TABLE tool_invocations (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  task_id UUID REFERENCES tasks(id) ON DELETE SET NULL,
  workflow_run_step_id UUID REFERENCES workflow_run_steps(id) ON DELETE SET NULL,
  mcp_tool_id UUID NOT NULL REFERENCES mcp_tools(id),
  request_json JSONB NOT NULL DEFAULT '{}'::jsonb,
  response_json JSONB NOT NULL DEFAULT '{}'::jsonb,
  status run_status NOT NULL DEFAULT 'queued',
  error_code TEXT,
  latency_ms INT,
  started_at TIMESTAMPTZ,
  ended_at TIMESTAMPTZ,
  created_at TIMESTAMPTZ NOT NULL DEFAULT now()
);

CREATE INDEX idx_tool_invocations_tool_status ON tool_invocations(mcp_tool_id, status);
```

## 7. Knowledge Store (Hybrid RAG)

```sql
CREATE TABLE knowledge_sources (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  workspace_id UUID NOT NULL REFERENCES workspaces(id) ON DELETE CASCADE,
  source_type source_type NOT NULL,
  uri TEXT,
  title TEXT,
  metadata_json JSONB NOT NULL DEFAULT '{}'::jsonb,
  ingest_status TEXT NOT NULL DEFAULT 'pending' CHECK (ingest_status IN ('pending', 'processing', 'ready', 'failed')),
  created_by UUID NOT NULL REFERENCES users(id),
  created_at TIMESTAMPTZ NOT NULL DEFAULT now()
);

CREATE TABLE knowledge_chunks (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  source_id UUID NOT NULL REFERENCES knowledge_sources(id) ON DELETE CASCADE,
  chunk_index INT NOT NULL,
  content TEXT NOT NULL,
  token_count INT,
  metadata_json JSONB NOT NULL DEFAULT '{}'::jsonb,
  UNIQUE (source_id, chunk_index)
);

CREATE TABLE chunk_embeddings (
  chunk_id UUID PRIMARY KEY REFERENCES knowledge_chunks(id) ON DELETE CASCADE,
  model_name TEXT NOT NULL,
  embedding VECTOR(1536) NOT NULL,
  content_hash TEXT NOT NULL,
  created_at TIMESTAMPTZ NOT NULL DEFAULT now()
);

CREATE TABLE concept_nodes (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  workspace_id UUID NOT NULL REFERENCES workspaces(id) ON DELETE CASCADE,
  concept_key TEXT NOT NULL,
  label TEXT NOT NULL,
  node_type TEXT NOT NULL,
  metadata_json JSONB NOT NULL DEFAULT '{}'::jsonb,
  UNIQUE (workspace_id, concept_key)
);

CREATE TABLE concept_edges (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  workspace_id UUID NOT NULL REFERENCES workspaces(id) ON DELETE CASCADE,
  src_concept_id UUID NOT NULL REFERENCES concept_nodes(id) ON DELETE CASCADE,
  dst_concept_id UUID NOT NULL REFERENCES concept_nodes(id) ON DELETE CASCADE,
  relation_type TEXT NOT NULL,
  weight NUMERIC(6,4) NOT NULL DEFAULT 1.0,
  metadata_json JSONB NOT NULL DEFAULT '{}'::jsonb,
  created_at TIMESTAMPTZ NOT NULL DEFAULT now()
);

CREATE INDEX idx_chunks_source ON knowledge_chunks(source_id);
CREATE INDEX idx_concept_edges_src_dst ON concept_edges(src_concept_id, dst_concept_id);
```

For pgvector approximate search:

```sql
CREATE INDEX idx_chunk_embeddings_ivfflat
ON chunk_embeddings USING ivfflat (embedding vector_cosine_ops)
WITH (lists = 100);
```

## 8. Media Assets and Audit

```sql
CREATE TABLE media_assets (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  workspace_id UUID NOT NULL REFERENCES workspaces(id) ON DELETE CASCADE,
  owner_id UUID NOT NULL REFERENCES users(id),
  type asset_type NOT NULL,
  storage_uri TEXT NOT NULL,
  source_message_id UUID REFERENCES messages(id) ON DELETE SET NULL,
  source_tool_invocation_id UUID REFERENCES tool_invocations(id) ON DELETE SET NULL,
  metadata_json JSONB NOT NULL DEFAULT '{}'::jsonb,
  created_at TIMESTAMPTZ NOT NULL DEFAULT now()
);

CREATE TABLE audit_logs (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  workspace_id UUID NOT NULL REFERENCES workspaces(id) ON DELETE CASCADE,
  actor_id UUID REFERENCES users(id),
  action TEXT NOT NULL,
  target_type TEXT NOT NULL,
  target_id UUID,
  payload_json JSONB NOT NULL DEFAULT '{}'::jsonb,
  created_at TIMESTAMPTZ NOT NULL DEFAULT now()
);

CREATE INDEX idx_audit_workspace_created_at ON audit_logs(workspace_id, created_at DESC);
```

## 9. Phase-by-Phase Rollout

Phase 1 (MVP):

- `users`, `workspaces`, `workspace_memberships`
- `conversations`, `threads`, `messages`, `context_injections`
- `agents`, `agent_runs`, `tasks`
- `mcp_servers`, `mcp_tools`, `tool_invocations`

Phase 2:

- `workflow_templates`, `workflow_nodes`, `workflow_edges`
- `workflow_runs`, `workflow_run_steps`
- `media_assets`

Phase 3:

- `knowledge_sources`, `knowledge_chunks`, `chunk_embeddings`
- `concept_nodes`, `concept_edges`
- retrieval analytics and quality scoring tables

## 10. Notes for Implementation

- Keep `JSONB` only for flexible payloads; avoid hiding core relations in JSON.
- Use explicit status enums for deterministic orchestration behavior.
- Add row-level security if multi-tenant deployment is planned.
- Consider time-based partitioning for `messages`, `task_events`, and `audit_logs` when scale grows.
