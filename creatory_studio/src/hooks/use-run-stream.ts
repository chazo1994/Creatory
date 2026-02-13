"use client";

import { useEffect, useState } from "react";

type StreamEvent = {
  event: string;
  data: Record<string, unknown>;
};

function parseSSEChunk(chunk: string): StreamEvent[] {
  const events: StreamEvent[] = [];
  const parts = chunk.split("\n\n").map((part) => part.trim()).filter(Boolean);

  for (const part of parts) {
    const lines = part.split("\n");
    const eventName = lines.find((line) => line.startsWith("event:"))?.replace("event:", "").trim() || "message";
    const dataLine = lines.find((line) => line.startsWith("data:"))?.replace("data:", "").trim();
    if (!dataLine) {
      continue;
    }

    try {
      events.push({
        event: eventName,
        data: JSON.parse(dataLine) as Record<string, unknown>
      });
    } catch {
      // Ignore malformed chunks in bootstrap runtime.
    }
  }

  return events;
}

export function useRunStream(params: { apiBaseUrl: string; token: string | null; runId: string | null }) {
  const { apiBaseUrl, token, runId } = params;
  const [events, setEvents] = useState<StreamEvent[]>([]);
  const [isStreaming, setIsStreaming] = useState(false);

  useEffect(() => {
    if (!token || !runId) {
      return;
    }

    let active = true;
    const controller = new AbortController();

    async function consume() {
      setIsStreaming(true);
      setEvents([]);

      const response = await fetch(`${apiBaseUrl}/orchestration/runs/${runId}/stream`, {
        method: "GET",
        headers: {
          Authorization: `Bearer ${token}`
        },
        signal: controller.signal,
        cache: "no-store"
      });

      if (!response.ok || !response.body) {
        setIsStreaming(false);
        return;
      }

      const reader = response.body.getReader();
      const decoder = new TextDecoder("utf-8");
      let buffer = "";

      while (active) {
        const { done, value } = await reader.read();
        if (done) {
          break;
        }
        buffer += decoder.decode(value, { stream: true });
        const parsed = parseSSEChunk(buffer);
        if (parsed.length > 0) {
          setEvents((prev) => [...prev, ...parsed]);
          buffer = "";
        }
      }

      setIsStreaming(false);
    }

    consume().catch(() => {
      setIsStreaming(false);
    });

    return () => {
      active = false;
      controller.abort();
    };
  }, [apiBaseUrl, token, runId]);

  return { events, isStreaming };
}
