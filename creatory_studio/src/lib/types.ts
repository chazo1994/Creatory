export type Uuid = string;

export type AuthResponse = {
  token: {
    access_token: string;
    token_type: string;
    expires_in: number;
  };
  user: {
    id: Uuid;
    email: string;
    display_name?: string | null;
  };
};

export type Workspace = {
  id: Uuid;
  name: string;
  slug: string;
  owner_id: Uuid;
};

export type Conversation = {
  id: Uuid;
  workspace_id: Uuid;
  title?: string | null;
};

export type Thread = {
  id: Uuid;
  conversation_id: Uuid;
  kind: "main" | "quick";
  parent_thread_id?: Uuid | null;
};

export type Message = {
  id: Uuid;
  thread_id: Uuid;
  role: "user" | "assistant" | "tool" | "system";
  content_json: Record<string, unknown>;
  created_at: string;
};

export type WorkflowTemplate = {
  id: Uuid;
  workspace_id: Uuid;
  name: string;
  description?: string | null;
  version: number;
};

export type WorkflowTemplateDetail = WorkflowTemplate & {
  nodes: Array<{
    id: Uuid;
    node_key: string;
    type: "agent" | "tool" | "human_gate" | "router" | "memory";
    config_json: Record<string, unknown>;
    position_x?: number | null;
    position_y?: number | null;
  }>;
  edges: Array<{
    id: Uuid;
    source_node_key: string;
    target_node_key: string;
    condition_expr?: string | null;
    metadata_json: Record<string, unknown>;
  }>;
};

export type WorkflowRun = {
  id: Uuid;
  status: string;
  steps: Array<{
    id: Uuid;
    node_key: string;
    status: string;
    output_json: Record<string, unknown>;
  }>;
};

export type MediaAsset = {
  id: Uuid;
  workspace_id: Uuid;
  owner_id: Uuid;
  type: "image" | "video" | "audio" | "document";
  storage_uri: string;
  created_at: string;
  metadata_json: Record<string, unknown>;
};

export type Agent = {
  id: Uuid;
  workspace_id: Uuid;
  slug: string;
  display_name: string;
  persona_prompt: string;
};

export type Provider = {
  slug: string;
  display_name: string;
  kind: "llm" | "image" | "video" | "audio" | "search" | "scraper";
  mode: "cloud" | "local";
  default_model?: string | null;
  default_endpoint?: string | null;
  supports_streaming: boolean;
  metadata: Record<string, unknown>;
};

export type ProviderConnectionTestResult = {
  provider_slug: string;
  ok: boolean;
  message: string;
  latency_ms?: number | null;
  diagnostics: Record<string, unknown>;
};

export type ProviderRoutingPreview = {
  draft_provider: string;
  refine_provider: string;
  reason: string;
};
