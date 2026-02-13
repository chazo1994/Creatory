"use client";

import "@xyflow/react/dist/style.css";

import { useMutation, useQuery } from "@tanstack/react-query";
import { useEffect, useMemo, useState } from "react";
import { Background, Controls, Edge, MiniMap, Node, ReactFlow } from "@xyflow/react";

import { api } from "@/lib/api";

type Props = {
  token: string;
  workspaceId: string;
  conversationId: string | null;
};

export function WorkflowPanel({ token, workspaceId, conversationId }: Props) {
  const [selectedTemplateId, setSelectedTemplateId] = useState<string | null>(null);

  const templatesQuery = useQuery({
    queryKey: ["workflow-templates", workspaceId],
    queryFn: () => api.listTemplates(token, workspaceId)
  });

  useEffect(() => {
    if (!selectedTemplateId && templatesQuery.data?.length) {
      setSelectedTemplateId(templatesQuery.data[0].id);
    }
  }, [selectedTemplateId, templatesQuery.data]);

  const templateDetailQuery = useQuery({
    queryKey: ["workflow-template", selectedTemplateId],
    queryFn: () => api.getTemplate(token, selectedTemplateId as string),
    enabled: Boolean(selectedTemplateId)
  });

  const runMutation = useMutation({
    mutationFn: async () => api.runTemplate(token, selectedTemplateId as string, conversationId),
    onSuccess: () => {
      templateDetailQuery.refetch();
    }
  });

  const flowNodes = useMemo<Node[]>(() => {
    if (!templateDetailQuery.data) {
      return [];
    }

    return templateDetailQuery.data.nodes.map((node, index) => ({
      id: node.node_key,
      position: {
        x: node.position_x ?? index * 220 + 60,
        y: node.position_y ?? 120
      },
      data: {
        label: `${node.node_key} · ${node.type}`
      },
      style: {
        border: "1px solid rgba(19,16,13,0.18)",
        borderRadius: 12,
        padding: 8,
        fontSize: 12,
        background: node.type === "human_gate" ? "#ffe5da" : "#ffffff"
      }
    }));
  }, [templateDetailQuery.data]);

  const flowEdges = useMemo<Edge[]>(() => {
    if (!templateDetailQuery.data) {
      return [];
    }

    return templateDetailQuery.data.edges.map((edge) => ({
      id: `${edge.source_node_key}-${edge.target_node_key}`,
      source: edge.source_node_key,
      target: edge.target_node_key,
      animated: true,
      style: {
        strokeWidth: 1.7,
        stroke: "#0f7b77"
      }
    }));
  }, [templateDetailQuery.data]);

  return (
    <section className="panel p-3 lg:col-span-4">
      <header className="mb-3 flex flex-wrap items-center justify-between gap-2">
        <div>
          <h2 className="text-xl font-black">Visual Workflow Editor</h2>
          <p className="text-sm text-black/65">
            Node-based agentic workflow with explicit human-in-the-loop checkpoint.
          </p>
        </div>
        <button
          className="bg-accent px-3 py-1.5 text-sm font-semibold text-white"
          disabled={!selectedTemplateId || runMutation.isPending}
          onClick={() => runMutation.mutate()}
        >
          {runMutation.isPending ? "Running..." : "Run Step-by-Step"}
        </button>
      </header>

      <div className="mb-3 flex flex-wrap items-center gap-2">
        <label className="text-xs font-semibold uppercase tracking-wide text-black/60">
          Template
        </label>
        <select
          value={selectedTemplateId ?? ""}
          onChange={(event) => setSelectedTemplateId(event.target.value)}
          className="field min-w-64"
        >
          {(templatesQuery.data ?? []).map((template) => (
            <option key={template.id} value={template.id}>
              {template.name} v{template.version}
            </option>
          ))}
        </select>
      </div>

      <div className="h-[280px] overflow-hidden rounded-xl border border-black/10 bg-white/70">
        {templateDetailQuery.data ? (
          <ReactFlow nodes={flowNodes} edges={flowEdges} fitView>
            <Background color="#b4b0a6" gap={18} />
            <MiniMap
              pannable
              zoomable
              style={{ background: "rgba(251,248,242,0.9)", border: "1px solid rgba(0,0,0,0.08)" }}
            />
            <Controls />
          </ReactFlow>
        ) : (
          <div className="flex h-full items-center justify-center text-sm text-black/55">
            {templatesQuery.isLoading ? "Loading templates..." : "No template available yet."}
          </div>
        )}
      </div>

      {runMutation.data ? (
        <div className="mt-3 rounded-xl border border-black/10 bg-white/80 p-2 text-xs">
          <p className="font-semibold">Latest run: {runMutation.data.status}</p>
          <ul className="mt-2 space-y-1">
            {runMutation.data.steps.map((step) => (
              <li key={step.id}>
                {step.node_key}: {step.status}
              </li>
            ))}
          </ul>
        </div>
      ) : null}
    </section>
  );
}
