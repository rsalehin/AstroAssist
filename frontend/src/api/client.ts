import type { StreamEvent } from "../types/artifacts";

export interface Bootstrap {
  workspace_id: string;
  thread_id: string;
}

export interface PublicSettings {
  model_profile: string;
  cache_mode: string;
  host: string;
  port: number;
  langsmith_tracing: boolean;
}

export async function bootstrap(): Promise<Bootstrap> {
  const res = await fetch("/api/bootstrap");
  if (!res.ok) throw new Error(`bootstrap failed: ${res.status}`);
  return (await res.json()) as Bootstrap;
}

export async function getSettings(): Promise<PublicSettings> {
  const res = await fetch("/api/settings");
  if (!res.ok) throw new Error(`settings failed: ${res.status}`);
  return (await res.json()) as PublicSettings;
}

/** POST a chat message and invoke `onEvent` for each SSE event in the stream. */
export async function streamMessage(
  threadId: string,
  text: string,
  onEvent: (event: StreamEvent) => void,
): Promise<void> {
  const res = await fetch(`/api/threads/${threadId}/messages`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ text }),
  });
  if (!res.ok || !res.body) throw new Error(`message failed: ${res.status}`);

  const reader = res.body.getReader();
  const decoder = new TextDecoder();
  let buffer = "";

  const processBlock = (block: string) => {
    for (const line of block.split(/\r?\n/)) {
      if (line.startsWith("data:")) {
        const payload = line.slice("data:".length).trim();
        if (payload) onEvent(JSON.parse(payload) as StreamEvent);
      }
    }
  };

  for (;;) {
    const { done, value } = await reader.read();
    if (done) break;
    buffer += decoder.decode(value, { stream: true });
    // SSE events are separated by a blank line (CRLF or LF).
    const blocks = buffer.split(/\r?\n\r?\n/);
    buffer = blocks.pop() ?? "";
    for (const block of blocks) processBlock(block);
  }
  if (buffer.trim()) processBlock(buffer);
}
