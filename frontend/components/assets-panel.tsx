"use client";

import { useMutation, useQuery } from "@tanstack/react-query";
import { useState } from "react";

import { api } from "@/lib/api";

type Props = {
  token: string;
  workspaceId: string;
};

export function AssetsPanel({ token, workspaceId }: Props) {
  const [assetType, setAssetType] = useState<"image" | "video" | "audio" | "document">("image");
  const [storageUri, setStorageUri] = useState("");

  const assetsQuery = useQuery({
    queryKey: ["assets", workspaceId],
    queryFn: () => api.listAssets(token, workspaceId)
  });

  const createAssetMutation = useMutation({
    mutationFn: async () =>
      api.createAsset(token, workspaceId, {
        type: assetType,
        storageUri,
        metadata: { source: "studio-manual" }
      }),
    onSuccess: () => {
      setStorageUri("");
      assetsQuery.refetch();
    }
  });

  return (
    <section className="panel p-3 lg:col-span-4">
      <header className="mb-3">
        <h2 className="text-xl font-black">Media Asset Manager</h2>
        <p className="text-sm text-black/65">Track generated images, videos, audio, and docs from agent workflows.</p>
      </header>

      <div className="mb-3 grid gap-2 md:grid-cols-[120px_1fr_auto]">
        <select
          className="field"
          value={assetType}
          onChange={(event) => setAssetType(event.target.value as typeof assetType)}
        >
          <option value="image">image</option>
          <option value="video">video</option>
          <option value="audio">audio</option>
          <option value="document">document</option>
        </select>
        <input
          className="field"
          value={storageUri}
          onChange={(event) => setStorageUri(event.target.value)}
          placeholder="storage://bucket/asset"
        />
        <button
          className="bg-signal px-3 py-2 text-sm font-semibold text-white"
          onClick={() => createAssetMutation.mutate()}
          disabled={!storageUri || createAssetMutation.isPending}
        >
          Add
        </button>
      </div>

      <div className="max-h-[290px] space-y-2 overflow-y-auto pr-1">
        {(assetsQuery.data ?? []).map((asset) => (
          <article key={asset.id} className="rounded-xl border border-black/10 bg-white/85 p-2">
            <header className="mb-1 flex items-center justify-between text-xs">
              <span className="badge">{asset.type}</span>
              <span className="text-black/55">{new Date(asset.created_at).toLocaleDateString()}</span>
            </header>
            <p className="break-all text-sm">{asset.storage_uri}</p>
          </article>
        ))}
        {!assetsQuery.data?.length ? (
          <p className="rounded-xl border border-dashed border-black/15 bg-white/70 px-3 py-4 text-sm text-black/60">
            No assets yet. Add your first artifact or generate from workflow runs.
          </p>
        ) : null}
      </div>
    </section>
  );
}
