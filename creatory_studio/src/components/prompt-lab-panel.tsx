"use client";

import { useMutation, useQuery } from "@tanstack/react-query";
import { useState } from "react";

import { api } from "@/lib/api";

type Props = {
  token: string;
  workspaceId: string;
};

function slugify(value: string): string {
  return value
    .trim()
    .toLowerCase()
    .replace(/[^a-z0-9]+/g, "-")
    .replace(/-{2,}/g, "-")
    .replace(/^-|-$/g, "");
}

export function PromptLabPanel({ token, workspaceId }: Props) {
  const [displayName, setDisplayName] = useState("Hook Strategist");
  const [personaPrompt, setPersonaPrompt] = useState(
    "Focus on platform-native hooks, retention pacing, and clear calls to action."
  );

  const agentsQuery = useQuery({
    queryKey: ["agents", workspaceId],
    queryFn: () => api.listAgents(token, workspaceId)
  });

  const createAgentMutation = useMutation({
    mutationFn: async () =>
      api.createAgent(token, workspaceId, {
        slug: slugify(displayName),
        displayName,
        personaPrompt
      }),
    onSuccess: () => {
      agentsQuery.refetch();
    }
  });

  return (
    <section className="panel p-3 lg:col-span-4">
      <header className="mb-3">
        <h2 className="text-xl font-black">Prompt Engineering Lab</h2>
        <p className="text-sm text-black/65">Create specialized agent personas and tune prompt behavior.</p>
      </header>

      <div className="space-y-2">
        <input
          className="field w-full"
          value={displayName}
          onChange={(event) => setDisplayName(event.target.value)}
          placeholder="Agent display name"
        />
        <textarea
          className="field min-h-24 w-full"
          value={personaPrompt}
          onChange={(event) => setPersonaPrompt(event.target.value)}
          placeholder="Persona prompt"
        />
        <button
          className="bg-ink px-3 py-2 text-sm font-semibold text-white"
          disabled={!displayName || !personaPrompt || createAgentMutation.isPending}
          onClick={() => createAgentMutation.mutate()}
        >
          {createAgentMutation.isPending ? "Saving..." : "Save Agent Persona"}
        </button>
      </div>

      <div className="mt-3 max-h-[220px] space-y-2 overflow-y-auto pr-1">
        {(agentsQuery.data ?? []).map((agent) => (
          <article key={agent.id} className="rounded-xl border border-black/10 bg-white/85 p-2">
            <header className="mb-1 flex items-center justify-between">
              <strong className="text-sm">{agent.display_name}</strong>
              <span className="badge text-xs">{agent.slug}</span>
            </header>
            <p className="max-h-14 overflow-hidden text-xs text-black/75">{agent.persona_prompt}</p>
          </article>
        ))}
        {!agentsQuery.data?.length ? (
          <p className="rounded-xl border border-dashed border-black/15 bg-white/70 px-3 py-4 text-sm text-black/60">
            No custom agent yet. System agents are bootstrapped when workspace is created.
          </p>
        ) : null}
      </div>
    </section>
  );
}
