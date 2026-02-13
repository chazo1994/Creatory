import { API_BASE_URL } from "@/lib/config";
import type {
  Agent,
  AuthResponse,
  Conversation,
  MediaAsset,
  Message,
  Provider,
  ProviderConnectionTestResult,
  ProviderRoutingPreview,
  Thread,
  WorkflowRun,
  WorkflowTemplate,
  WorkflowTemplateDetail,
  Workspace
} from "@/lib/types";

type Method = "GET" | "POST" | "PUT" | "PATCH" | "DELETE";

async function request<T>(
  path: string,
  options: {
    method?: Method;
    token?: string;
    body?: unknown;
    headers?: Record<string, string>;
  } = {}
): Promise<T> {
  const headers: Record<string, string> = {
    "Content-Type": "application/json",
    ...options.headers
  };

  if (options.token) {
    headers.Authorization = `Bearer ${options.token}`;
  }

  const response = await fetch(`${API_BASE_URL}${path}`, {
    method: options.method ?? "GET",
    headers,
    body: options.body === undefined ? undefined : JSON.stringify(options.body),
    cache: "no-store"
  });

  if (!response.ok) {
    const payload = (await response.json().catch(() => ({}))) as {
      detail?: string | Array<{ loc?: Array<string | number>; msg?: string }>;
    };
    const detail = payload.detail;
    if (Array.isArray(detail)) {
      const message = detail
        .map((item) => {
          const loc = (item.loc ?? []).filter((part) => part !== "body").join(".");
          const label = loc ? `${loc}: ` : "";
          return `${label}${item.msg ?? "Invalid value"}`;
        })
        .join("; ");
      throw new Error(message || `Request failed with status ${response.status}`);
    }
    throw new Error((detail as string) ?? `Request failed with status ${response.status}`);
  }

  return (await response.json()) as T;
}

export const api = {
  register(email: string, password: string, displayName?: string) {
    return request<AuthResponse>("/auth/register", {
      method: "POST",
      body: {
        email,
        password,
        display_name: displayName || null
      }
    });
  },

  login(email: string, password: string) {
    return request<AuthResponse>("/auth/login", {
      method: "POST",
      body: { email, password }
    });
  },

  listWorkspaces(token: string) {
    return request<Workspace[]>("/workspaces", { token });
  },

  createWorkspace(token: string, name: string) {
    return request<Workspace>("/workspaces", {
      method: "POST",
      token,
      body: { name }
    });
  },

  listConversations(token: string, workspaceId: string) {
    return request<Conversation[]>(`/conversations?workspace_id=${workspaceId}`, { token });
  },

  createConversation(token: string, workspaceId: string, title: string) {
    return request<Conversation>("/conversations", {
      method: "POST",
      token,
      body: {
        workspace_id: workspaceId,
        title
      }
    });
  },

  listThreads(token: string, conversationId: string) {
    return request<Thread[]>(`/conversations/${conversationId}/threads`, { token });
  },

  listMessages(token: string, conversationId: string, threadId: string) {
    return request<Message[]>(`/conversations/${conversationId}/threads/${threadId}/messages`, {
      token
    });
  },

  runChat(
    token: string,
    conversationId: string,
    threadId: string,
    prompt: string,
    assistantAgentSlug?: string
  ) {
    return request<{
      user_message: Message;
      assistant_message: Message;
      agent_run: { id: string; status: string };
      tasks: Array<{ id: string; task_type: string; status: string }>;
    }>(`/orchestration/conversations/${conversationId}/threads/${threadId}/chat`, {
      method: "POST",
      token,
      body: {
        prompt,
        assistant_agent_slug: assistantAgentSlug ?? null,
        metadata_json: {}
      }
    });
  },

  injectContext(
    token: string,
    conversationId: string,
    payload: {
      from_thread_id: string;
      from_message_id: string;
      to_thread_id: string;
      to_message_id?: string | null;
      context_block: Record<string, unknown>;
    }
  ) {
    return request(`/conversations/${conversationId}/inject`, {
      method: "POST",
      token,
      body: payload
    });
  },

  listTemplates(token: string, workspaceId: string) {
    return request<WorkflowTemplate[]>(`/workflows/templates?workspace_id=${workspaceId}`, {
      token
    });
  },

  getTemplate(token: string, templateId: string) {
    return request<WorkflowTemplateDetail>(`/workflows/templates/${templateId}`, { token });
  },

  runTemplate(token: string, templateId: string, conversationId: string | null) {
    return request<WorkflowRun>(`/workflows/templates/${templateId}/run`, {
      method: "POST",
      token,
      body: {
        conversation_id: conversationId,
        input_json: {
          mode: "studio",
          timestamp: new Date().toISOString()
        }
      }
    });
  },

  listAssets(token: string, workspaceId: string) {
    return request<MediaAsset[]>(`/assets?workspace_id=${workspaceId}`, { token });
  },

  createAsset(
    token: string,
    workspaceId: string,
    payload: {
      type: "image" | "video" | "audio" | "document";
      storageUri: string;
      metadata?: Record<string, unknown>;
    }
  ) {
    return request<MediaAsset>("/assets", {
      method: "POST",
      token,
      body: {
        workspace_id: workspaceId,
        type: payload.type,
        storage_uri: payload.storageUri,
        metadata_json: payload.metadata ?? {}
      }
    });
  },

  listAgents(token: string, workspaceId: string) {
    return request<Agent[]>(`/agents?workspace_id=${workspaceId}`, { token });
  },

  createAgent(
    token: string,
    workspaceId: string,
    payload: {
      slug: string;
      displayName: string;
      personaPrompt: string;
    }
  ) {
    return request<Agent>("/agents", {
      method: "POST",
      token,
      body: {
        workspace_id: workspaceId,
        slug: payload.slug,
        display_name: payload.displayName,
        persona_prompt: payload.personaPrompt,
        config_json: {
          source: "prompt-lab"
        },
        is_system: false
      }
    });
  },

  listProviderCatalog(token: string) {
    return request<Provider[]>("/providers/catalog", { token });
  },

  testProviderConnection(
    token: string,
    payload: {
      provider_slug: string;
      endpoint?: string | null;
      api_key?: string | null;
      model?: string | null;
    }
  ) {
    return request<ProviderConnectionTestResult>("/providers/test", {
      method: "POST",
      token,
      body: payload
    });
  },

  previewProviderRoute(
    token: string,
    payload: {
      prompt: string;
      prefer_local?: boolean;
    }
  ) {
    return request<ProviderRoutingPreview>("/providers/routing/preview", {
      method: "POST",
      token,
      body: payload
    });
  }
};
