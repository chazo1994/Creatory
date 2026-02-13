"use client";

import { useMutation, useQueryClient } from "@tanstack/react-query";

import { api } from "@/lib/api";
import type { Message } from "@/lib/types";

type Params = {
  token: string;
  conversationId: string;
  quickThreadId: string;
  mainThreadId: string;
};

export function useContextInjection({ token, conversationId, quickThreadId, mainThreadId }: Params) {
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: async (message: Message) =>
      api.injectContext(token, conversationId, {
        from_thread_id: quickThreadId,
        from_message_id: message.id,
        to_thread_id: mainThreadId,
        to_message_id: null,
        context_block: {
          reference_id: message.id,
          text: typeof message.content_json.text === "string" ? message.content_json.text : "",
          source: "quick-thread"
        }
      }),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ["messages", conversationId, mainThreadId] });
    }
  });
}
