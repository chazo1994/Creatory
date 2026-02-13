"use client";

import { useMutation, useQuery } from "@tanstack/react-query";
import { useMemo, useState } from "react";

import { api } from "@/lib/api";
import { useStudioStore } from "@/store/studio-store";

export function SettingsCenter() {
  const { token } = useStudioStore();
  const [providerSlug, setProviderSlug] = useState("openai");
  const [endpoint, setEndpoint] = useState("");
  const [apiKey, setApiKey] = useState("");
  const [model, setModel] = useState("");
  const [prompt, setPrompt] = useState("Draft a TikTok script from this topic");

  const catalogQuery = useQuery({
    queryKey: ["providers-catalog", token],
    queryFn: () => api.listProviderCatalog(token as string),
    enabled: Boolean(token)
  });

  const providers = useMemo(() => catalogQuery.data ?? [], [catalogQuery.data]);

  const testMutation = useMutation({
    mutationFn: async () =>
      api.testProviderConnection(token as string, {
        provider_slug: providerSlug,
        endpoint: endpoint || null,
        api_key: apiKey || null,
        model: model || null
      }),
  });

  const routePreviewMutation = useMutation({
    mutationFn: async () =>
      api.previewProviderRoute(token as string, {
        prompt,
        prefer_local: false
      })
  });

  return (
    <section className="panel p-4">
      <header>
        <h1 className="text-2xl font-black">Provider Settings Center</h1>
        <p className="mt-1 text-sm text-black/65">
          Configure PAL providers and validate connectivity before running orchestration.
        </p>
      </header>

      {!token ? (
        <p className="mt-4 rounded-xl border border-dashed border-black/20 bg-white/70 p-3 text-sm text-black/60">
          Authenticate in Chat first to access provider settings.
        </p>
      ) : (
        <>
          <div className="mt-4 grid gap-3 md:grid-cols-2">
            <label className="text-sm">
              <span className="mb-1 block text-xs uppercase tracking-wide text-black/55">Provider</span>
              <select
                value={providerSlug}
                onChange={(event) => setProviderSlug(event.target.value)}
                className="field w-full"
              >
                {providers.map((provider) => (
                  <option key={provider.slug} value={provider.slug}>
                    {provider.display_name} ({provider.kind}/{provider.mode})
                  </option>
                ))}
              </select>
            </label>
            <label className="text-sm">
              <span className="mb-1 block text-xs uppercase tracking-wide text-black/55">Endpoint</span>
              <input
                className="field w-full"
                value={endpoint}
                onChange={(event) => setEndpoint(event.target.value)}
                placeholder="http://localhost:11434"
              />
            </label>
            <label className="text-sm">
              <span className="mb-1 block text-xs uppercase tracking-wide text-black/55">API Key</span>
              <input
                className="field w-full"
                value={apiKey}
                onChange={(event) => setApiKey(event.target.value)}
                placeholder="Optional for local providers"
                type="password"
              />
            </label>
            <label className="text-sm">
              <span className="mb-1 block text-xs uppercase tracking-wide text-black/55">Model</span>
              <input
                className="field w-full"
                value={model}
                onChange={(event) => setModel(event.target.value)}
                placeholder="gpt-4.1-mini"
              />
            </label>
          </div>

          <div className="mt-3 flex flex-wrap gap-2">
            <button
              className="bg-accent px-3 py-2 text-sm font-semibold text-white"
              onClick={() => testMutation.mutate()}
              disabled={testMutation.isPending}
            >
              {testMutation.isPending ? "Testing..." : "Test Connection"}
            </button>
          </div>

          {testMutation.data ? (
            <p className="mt-3 rounded-xl border border-black/10 bg-white/80 p-2 text-sm">
              <span className="font-semibold">Result:</span> {testMutation.data.message}
            </p>
          ) : null}

          <div className="mt-6 border-t border-black/10 pt-4">
            <h2 className="text-lg font-bold">Routing Preview</h2>
            <p className="text-sm text-black/65">
              Simulate PAL routing between draft and refine models for your current prompt.
            </p>
            <textarea
              value={prompt}
              onChange={(event) => setPrompt(event.target.value)}
              className="field mt-2 min-h-24 w-full"
            />
            <button
              className="mt-2 bg-signal px-3 py-2 text-sm font-semibold text-white"
              onClick={() => routePreviewMutation.mutate()}
              disabled={routePreviewMutation.isPending}
            >
              {routePreviewMutation.isPending ? "Routing..." : "Preview Route"}
            </button>
            {routePreviewMutation.data ? (
              <div className="mt-2 rounded-xl border border-black/10 bg-white/80 p-2 text-sm">
                <p>
                  Draft: <span className="font-semibold">{routePreviewMutation.data.draft_provider}</span>
                </p>
                <p>
                  Refine: <span className="font-semibold">{routePreviewMutation.data.refine_provider}</span>
                </p>
                <p className="text-black/60">{routePreviewMutation.data.reason}</p>
              </div>
            ) : null}
          </div>
        </>
      )}
    </section>
  );
}
