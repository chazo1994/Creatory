import { create } from "zustand";

import type { AuthResponse, Workspace } from "@/lib/types";

type StudioState = {
  token: string | null;
  user: AuthResponse["user"] | null;
  workspaces: Workspace[];
  selectedWorkspaceId: string | null;
  selectedConversationId: string | null;
  mainThreadId: string | null;
  quickThreadId: string | null;
  setAuth: (auth: AuthResponse) => void;
  setWorkspaces: (workspaces: Workspace[]) => void;
  selectWorkspace: (workspaceId: string | null) => void;
  selectConversation: (conversationId: string | null) => void;
  setThreads: (threadIds: { main?: string | null; quick?: string | null }) => void;
  logout: () => void;
};

export const useStudioStore = create<StudioState>((set) => ({
  token: null,
  user: null,
  workspaces: [],
  selectedWorkspaceId: null,
  selectedConversationId: null,
  mainThreadId: null,
  quickThreadId: null,
  setAuth: (auth) =>
    set({
      token: auth.token.access_token,
      user: auth.user
    }),
  setWorkspaces: (workspaces) =>
    set((state) => {
      const current = state.selectedWorkspaceId;
      const selectedWorkspaceId =
        current && workspaces.some((workspace) => workspace.id === current)
          ? current
          : workspaces[0]?.id ?? null;

      return {
        workspaces,
        selectedWorkspaceId
      };
    }),
  selectWorkspace: (workspaceId) =>
    set({
      selectedWorkspaceId: workspaceId,
      selectedConversationId: null,
      mainThreadId: null,
      quickThreadId: null
    }),
  selectConversation: (conversationId) =>
    set({
      selectedConversationId: conversationId,
      mainThreadId: null,
      quickThreadId: null
    }),
  setThreads: ({ main, quick }) =>
    set({
      mainThreadId: main ?? null,
      quickThreadId: quick ?? null
    }),
  logout: () =>
    set({
      token: null,
      user: null,
      workspaces: [],
      selectedWorkspaceId: null,
      selectedConversationId: null,
      mainThreadId: null,
      quickThreadId: null
    })
}));
