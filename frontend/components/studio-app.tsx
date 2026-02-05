"use client";

import { useMutation, useQuery } from "@tanstack/react-query";
import { useEffect, useMemo, useState } from "react";

import { AssetsPanel } from "@/components/assets-panel";
import { DualChatPanel } from "@/components/dual-chat-panel";
import { PromptLabPanel } from "@/components/prompt-lab-panel";
import { WorkflowPanel } from "@/components/workflow-panel";
import { api } from "@/lib/api";
import { useStudioStore } from "@/lib/studio-store";

function extractMainAndQuickThreadIds(threads: Array<{ id: string; kind: string }>) {
  const main = threads.find((thread) => thread.kind === "main")?.id ?? null;
  const quick = threads.find((thread) => thread.kind === "quick")?.id ?? null;
  return { main, quick };
}

export function StudioApp() {
  const {
    token,
    user,
    workspaces,
    selectedWorkspaceId,
    selectedConversationId,
    mainThreadId,
    quickThreadId,
    setAuth,
    setWorkspaces,
    selectWorkspace,
    selectConversation,
    setThreads,
    logout
  } = useStudioStore();

  const [authMode, setAuthMode] = useState<"login" | "register">("login");
  const [email, setEmail] = useState("creator@example.com");
  const [password, setPassword] = useState("creator123");
  const [displayName, setDisplayName] = useState("Creator");
  const [workspaceName, setWorkspaceName] = useState("Creator Studio");
  const [conversationTitle, setConversationTitle] = useState("New Campaign");

  const workspacesQuery = useQuery({
    queryKey: ["workspaces", token],
    queryFn: () => api.listWorkspaces(token as string),
    enabled: Boolean(token)
  });

  useEffect(() => {
    if (workspacesQuery.data) {
      setWorkspaces(workspacesQuery.data);
    }
  }, [setWorkspaces, workspacesQuery.data]);

  const conversationsQuery = useQuery({
    queryKey: ["conversations", token, selectedWorkspaceId],
    queryFn: () => api.listConversations(token as string, selectedWorkspaceId as string),
    enabled: Boolean(token && selectedWorkspaceId)
  });

  useEffect(() => {
    if (!selectedConversationId && conversationsQuery.data?.length) {
      selectConversation(conversationsQuery.data[0].id);
    }
  }, [selectedConversationId, conversationsQuery.data, selectConversation]);

  const threadsQuery = useQuery({
    queryKey: ["threads", token, selectedConversationId],
    queryFn: () => api.listThreads(token as string, selectedConversationId as string),
    enabled: Boolean(token && selectedConversationId)
  });

  useEffect(() => {
    if (threadsQuery.data) {
      const ids = extractMainAndQuickThreadIds(threadsQuery.data);
      setThreads(ids);
    }
  }, [setThreads, threadsQuery.data]);

  const authMutation = useMutation({
    mutationFn: async () => {
      if (authMode === "register") {
        return api.register(email, password, displayName);
      }
      return api.login(email, password);
    },
    onSuccess: (auth) => {
      setAuth(auth);
    }
  });

  const createWorkspaceMutation = useMutation({
    mutationFn: async () => api.createWorkspace(token as string, workspaceName),
    onSuccess: async (workspace) => {
      workspacesQuery.refetch();
      selectWorkspace(workspace.id);
    }
  });

  const createConversationMutation = useMutation({
    mutationFn: async () =>
      api.createConversation(token as string, selectedWorkspaceId as string, conversationTitle),
    onSuccess: async (conversation) => {
      conversationsQuery.refetch();
      selectConversation(conversation.id);
    }
  });

  const authError = authMutation.error instanceof Error ? authMutation.error.message : null;

  const selectedWorkspace = useMemo(
    () => workspaces.find((workspace) => workspace.id === selectedWorkspaceId) ?? null,
    [workspaces, selectedWorkspaceId]
  );

  return (
    <main className="space-y-3 pb-4">
      <section className="panel flex flex-wrap items-end justify-between gap-3 p-4">
        <div>
          <p className="text-xs font-semibold uppercase tracking-[0.22em] text-black/55">Creator-First Framework</p>
          <h1 className="text-3xl font-black sm:text-4xl">Creatory Studio</h1>
          <p className="mt-1 max-w-2xl text-sm text-black/70">
            Director Agent coordinates workflows, tools, and memory. Creator drives intent and approval.
          </p>
        </div>

        <div className="flex flex-wrap items-end gap-2 text-sm">
          {!token ? (
            <>
              <select
                className="field"
                value={authMode}
                onChange={(event) => setAuthMode(event.target.value as typeof authMode)}
              >
                <option value="login">login</option>
                <option value="register">register</option>
              </select>
              <input
                className="field"
                value={email}
                onChange={(event) => setEmail(event.target.value)}
                placeholder="email"
              />
              <input
                className="field"
                type="password"
                value={password}
                onChange={(event) => setPassword(event.target.value)}
                placeholder="password"
              />
              {authMode === "register" ? (
                <input
                  className="field"
                  value={displayName}
                  onChange={(event) => setDisplayName(event.target.value)}
                  placeholder="display name"
                />
              ) : null}
              <button
                className="bg-ink px-3 py-2 font-semibold text-white"
                onClick={() => authMutation.mutate()}
                disabled={authMutation.isPending}
              >
                {authMutation.isPending ? "Loading..." : authMode}
              </button>
            </>
          ) : (
            <>
              <span className="badge">{user?.email}</span>
              <input
                className="field"
                value={workspaceName}
                onChange={(event) => setWorkspaceName(event.target.value)}
                placeholder="workspace name"
              />
              <button
                className="bg-signal px-3 py-2 font-semibold text-white"
                onClick={() => createWorkspaceMutation.mutate()}
                disabled={createWorkspaceMutation.isPending}
              >
                + Workspace
              </button>
              <button className="bg-black/80 px-3 py-2 font-semibold text-white" onClick={logout}>
                Logout
              </button>
            </>
          )}
        </div>
      </section>

      {authError ? <p className="text-sm text-red-700">{authError}</p> : null}

      {token ? (
        <>
          <section className="panel flex flex-wrap items-center gap-2 p-3 text-sm">
            <span className="badge">Workspace</span>
            <select
              className="field min-w-56"
              value={selectedWorkspaceId ?? ""}
              onChange={(event) => selectWorkspace(event.target.value)}
            >
              {workspaces.map((workspace) => (
                <option key={workspace.id} value={workspace.id}>
                  {workspace.name}
                </option>
              ))}
            </select>
            <span className="badge">Conversation</span>
            <select
              className="field min-w-56"
              value={selectedConversationId ?? ""}
              onChange={(event) => selectConversation(event.target.value)}
              disabled={!conversationsQuery.data?.length}
            >
              {(conversationsQuery.data ?? []).map((conversation) => (
                <option key={conversation.id} value={conversation.id}>
                  {conversation.title || conversation.id.slice(0, 8)}
                </option>
              ))}
            </select>
            <input
              className="field"
              value={conversationTitle}
              onChange={(event) => setConversationTitle(event.target.value)}
              placeholder="conversation title"
            />
            <button
              className="bg-accent px-3 py-2 font-semibold text-white"
              onClick={() => createConversationMutation.mutate()}
              disabled={!selectedWorkspaceId || createConversationMutation.isPending}
            >
              + Conversation
            </button>
            {selectedWorkspace ? <span className="text-black/60">Slug: {selectedWorkspace.slug}</span> : null}
          </section>

          {selectedWorkspaceId && selectedConversationId && mainThreadId && quickThreadId ? (
            <section className="grid gap-3 lg:grid-cols-12">
              <DualChatPanel
                token={token}
                conversationId={selectedConversationId}
                mainThreadId={mainThreadId}
                quickThreadId={quickThreadId}
              />
              <WorkflowPanel
                token={token}
                workspaceId={selectedWorkspaceId}
                conversationId={selectedConversationId}
              />
              <AssetsPanel token={token} workspaceId={selectedWorkspaceId} />
              <PromptLabPanel token={token} workspaceId={selectedWorkspaceId} />
            </section>
          ) : (
            <section className="panel p-6 text-center text-sm text-black/65">
              Create a workspace and conversation to start the full Creator Studio modules.
            </section>
          )}
        </>
      ) : (
        <section className="panel p-6 text-center text-sm text-black/65">
          Authenticate with your backend account to open the studio runtime.
        </section>
      )}
    </main>
  );
}
