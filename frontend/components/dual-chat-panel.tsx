"use client";

import { useMutation, useQuery, useQueryClient } from "@tanstack/react-query";
import { useMemo, useState } from "react";

import { api } from "@/lib/api";
import type { Message } from "@/lib/types";

type Props = {
  token: string;
  conversationId: string;
  mainThreadId: string | null;
  quickThreadId: string | null;
};

function contentText(message: Message): string {
  const fromText = message.content_json.text;
  if (typeof fromText === "string") {
    return fromText;
  }
  return JSON.stringify(message.content_json);
}

function MessageBubble({
  message,
  onInject,
  canInject
}: {
  message: Message;
  onInject?: () => void;
  canInject?: boolean;
}) {
  const isUser = message.role === "user";
  return (
    <article
      className={`animate-rise rounded-xl border px-3 py-2 text-sm ${
        isUser
          ? "ml-8 border-signal/35 bg-signal/10"
          : "mr-8 border-black/10 bg-white/85"
      }`}
    >
      <header className="mb-1 flex items-center justify-between text-[11px] uppercase tracking-wide text-black/55">
        <span>{message.role}</span>
        <span>{new Date(message.created_at).toLocaleTimeString()}</span>
      </header>
      <p className="whitespace-pre-wrap leading-relaxed">{contentText(message)}</p>
      {canInject ? (
        <div className="mt-2">
          <button
            onClick={onInject}
            className="bg-accent px-2.5 py-1 text-xs font-semibold text-white"
          >
            Add to Main Project
          </button>
        </div>
      ) : null}
    </article>
  );
}

function ThreadColumn({
  title,
  description,
  accent,
  messages,
  value,
  onChange,
  onSend,
  sending,
  emptyText,
  canSend,
  onInject,
  canInject
}: {
  title: string;
  description: string;
  accent: string;
  messages: Message[];
  value: string;
  onChange: (value: string) => void;
  onSend: () => void;
  sending: boolean;
  emptyText: string;
  canSend: boolean;
  onInject?: (message: Message) => void;
  canInject?: boolean;
}) {
  return (
    <section className="panel flex min-h-[460px] flex-col p-3">
      <header className="mb-3 flex items-end justify-between gap-2">
        <div>
          <h3 className="text-lg font-bold">{title}</h3>
          <p className="text-xs text-black/60">{description}</p>
        </div>
        <span className="badge" style={{ borderColor: accent, color: accent }}>
          Stream
        </span>
      </header>

      <div className="flex-1 space-y-2 overflow-y-auto pr-1">
        {messages.length ? (
          messages.map((message) => (
            <MessageBubble
              key={message.id}
              message={message}
              canInject={Boolean(canInject && onInject && message.role === "assistant")}
              onInject={
                onInject && message.role === "assistant"
                  ? () => onInject(message)
                  : undefined
              }
            />
          ))
        ) : (
          <p className="rounded-xl border border-dashed border-black/15 bg-white/70 px-3 py-4 text-sm text-black/60">
            {emptyText}
          </p>
        )}
      </div>

      <footer className="mt-3 flex items-end gap-2">
        <textarea
          value={value}
          onChange={(event) => onChange(event.target.value)}
          placeholder="Type your request..."
          rows={3}
          className="field min-h-24 flex-1 resize-y"
        />
        <button
          className="bg-ink px-4 py-2 text-sm font-semibold text-white"
          onClick={onSend}
          disabled={!canSend || sending}
        >
          {sending ? "Sending..." : "Send"}
        </button>
      </footer>
    </section>
  );
}

export function DualChatPanel({ token, conversationId, mainThreadId, quickThreadId }: Props) {
  const queryClient = useQueryClient();
  const [mainInput, setMainInput] = useState("");
  const [quickInput, setQuickInput] = useState("");
  const [injectStatus, setInjectStatus] = useState<string | null>(null);

  const mainMessagesQuery = useQuery({
    queryKey: ["messages", conversationId, mainThreadId],
    queryFn: () => api.listMessages(token, conversationId, mainThreadId as string),
    enabled: Boolean(mainThreadId)
  });

  const quickMessagesQuery = useQuery({
    queryKey: ["messages", conversationId, quickThreadId],
    queryFn: () => api.listMessages(token, conversationId, quickThreadId as string),
    enabled: Boolean(quickThreadId)
  });

  const runChatMutation = useMutation({
    mutationFn: async (payload: { threadId: string; prompt: string }) =>
      api.runChat(token, conversationId, payload.threadId, payload.prompt),
    onSuccess: (_, variables) => {
      queryClient.invalidateQueries({ queryKey: ["messages", conversationId, variables.threadId] });
      queryClient.invalidateQueries({ queryKey: ["orchestration-runs", conversationId] });
    }
  });

  const injectMutation = useMutation({
    mutationFn: async (message: Message) =>
      api.injectContext(token, conversationId, {
        from_thread_id: quickThreadId as string,
        from_message_id: message.id,
        to_thread_id: mainThreadId as string,
        to_message_id: null,
        context_block: {
          reference_id: message.id,
          text: contentText(message),
          source: "quick-thread"
        }
      }),
    onSuccess: () => {
      setInjectStatus("Injected into main context block.");
      queryClient.invalidateQueries({ queryKey: ["messages", conversationId, mainThreadId] });
    },
    onError: (error: Error) => {
      setInjectStatus(error.message);
    }
  });

  const mainMessages = useMemo(() => mainMessagesQuery.data ?? [], [mainMessagesQuery.data]);
  const quickMessages = useMemo(() => quickMessagesQuery.data ?? [], [quickMessagesQuery.data]);

  return (
    <section className="panel p-3 lg:col-span-8">
      <header className="mb-3 flex flex-wrap items-center justify-between gap-2">
        <div>
          <h2 className="text-xl font-black">Dual-Chat Interface</h2>
          <p className="text-sm text-black/65">
            Main Thread for strategic direction, Side Thread for quick experiments and contextual injection.
          </p>
        </div>
        {injectStatus ? <p className="text-xs text-signal">{injectStatus}</p> : null}
      </header>

      <div className="grid gap-3 md:grid-cols-2">
        <ThreadColumn
          title="Main Stream"
          description="Long-form project narrative and execution decisions"
          accent="#0f7b77"
          messages={mainMessages}
          value={mainInput}
          onChange={setMainInput}
          onSend={() => {
            if (!mainThreadId || !mainInput.trim()) {
              return;
            }
            runChatMutation.mutate({
              threadId: mainThreadId,
              prompt: mainInput.trim()
            });
            setMainInput("");
          }}
          sending={runChatMutation.isPending}
          emptyText="Start with a strategic prompt. Director Agent will plan and coordinate next tasks."
          canSend={Boolean(mainThreadId && mainInput.trim().length > 0)}
        />
        <ThreadColumn
          title="Quick-Access Stream"
          description="Fast checks, micro-prompts, and snippets to inject"
          accent="#e4572e"
          messages={quickMessages}
          value={quickInput}
          onChange={setQuickInput}
          onSend={() => {
            if (!quickThreadId || !quickInput.trim()) {
              return;
            }
            runChatMutation.mutate({
              threadId: quickThreadId,
              prompt: quickInput.trim()
            });
            setQuickInput("");
          }}
          sending={runChatMutation.isPending}
          emptyText="Use this lane to quickly prototype hooks, captions, or references."
          canSend={Boolean(quickThreadId && quickInput.trim().length > 0)}
          canInject={Boolean(mainThreadId && quickThreadId)}
          onInject={(message) => injectMutation.mutate(message)}
        />
      </div>
    </section>
  );
}
