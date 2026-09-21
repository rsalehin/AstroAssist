import { useEffect, useRef, useState } from "react";

import { bootstrap, streamMessage } from "../api/client";
import { useStore } from "../store";
import type { Artifact, StreamEvent } from "../types/artifacts";
import { ArtifactCard } from "./ArtifactCard";

interface ChatMessage {
  id: string;
  role: "user" | "assistant";
  content: string;
  artifacts: Artifact[];
}

let counter = 0;
const nextId = () => `m${counter++}`;

export function Chat() {
  const [threadId, setThreadId] = useState<string | null>(null);
  const [messages, setMessages] = useState<ChatMessage[]>([]);
  const [input, setInput] = useState("");
  const [busy, setBusy] = useState(false);
  const addArtifact = useStore((s) => s.addArtifact);
  const addTrace = useStore((s) => s.addTrace);
  const select = useStore((s) => s.select);
  const bottomRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    bootstrap()
      .then((b) => setThreadId(b.thread_id))
      .catch(() => setThreadId(null));
  }, []);

  useEffect(() => {
    bottomRef.current?.scrollIntoView({ behavior: "smooth" });
  }, [messages]);

  async function send() {
    const text = input.trim();
    if (!text || !threadId || busy) return;
    setInput("");
    setBusy(true);
    const userMsg: ChatMessage = { id: nextId(), role: "user", content: text, artifacts: [] };
    const assistantId = nextId();
    setMessages((m) => [
      ...m,
      userMsg,
      { id: assistantId, role: "assistant", content: "", artifacts: [] },
    ]);

    const patch = (fn: (msg: ChatMessage) => ChatMessage) =>
      setMessages((m) => m.map((msg) => (msg.id === assistantId ? fn(msg) : msg)));

    try {
      await streamMessage(threadId, text, (event: StreamEvent) => {
        if (event.type === "token") {
          patch((msg) => ({ ...msg, content: msg.content + String(event.text ?? "") }));
        } else if (event.type === "artifact") {
          const artifact = event.artifact as Artifact;
          addArtifact(artifact);
          select(artifact);
          patch((msg) => ({ ...msg, artifacts: [...msg.artifacts, artifact] }));
        } else if (event.type === "trace") {
          addTrace(event as Record<string, unknown>);
        }
      });
    } finally {
      setBusy(false);
    }
  }

  return (
    <section className="flex h-full flex-col">
      <div className="flex-1 space-y-4 overflow-y-auto p-4" data-testid="chat-log">
        {messages.length === 0 ? (
          <p className="text-sm text-muted">
            Ask a question to begin. Try <span className="font-mono">hello</span>.
          </p>
        ) : null}
        {messages.map((msg) => (
          <div key={msg.id} data-role={msg.role} className="space-y-2">
            <div className="text-xs uppercase tracking-wide text-muted">{msg.role}</div>
            {msg.content ? <p className="whitespace-pre-wrap text-ink">{msg.content}</p> : null}
            {msg.artifacts.map((a) => (
              <ArtifactCard key={a.id} artifact={a} onSelect={select} />
            ))}
          </div>
        ))}
        <div ref={bottomRef} />
      </div>
      <form
        className="flex gap-2 border-t border-border p-3"
        onSubmit={(e) => {
          e.preventDefault();
          void send();
        }}
      >
        <input
          data-testid="composer-input"
          className="flex-1 rounded-md border border-border bg-surface px-3 py-2 text-ink placeholder:text-muted"
          placeholder="Ask AstroAssist…"
          value={input}
          disabled={!threadId}
          onChange={(e) => setInput(e.target.value)}
        />
        <button
          data-testid="composer-send"
          type="submit"
          disabled={!threadId || busy}
          className="rounded-md bg-accent px-4 py-2 font-medium text-white disabled:opacity-50"
        >
          Send
        </button>
      </form>
    </section>
  );
}
