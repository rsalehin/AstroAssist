import { useState } from "react";

import { useStore } from "../store";
import { ArtifactCard } from "./ArtifactCard";
import { Chat } from "./Chat";
import { Settings } from "./Settings";

function ThemeToggle() {
  const [light, setLight] = useState(false);
  return (
    <button
      className="rounded-md border border-border px-2 py-1 text-xs text-muted hover:text-ink"
      onClick={() => {
        document.documentElement.classList.toggle("light");
        setLight((v) => !v);
      }}
    >
      {light ? "Light" : "Dark"}
    </button>
  );
}

export function Workbench() {
  const artifacts = useStore((s) => s.artifacts);
  const selected = useStore((s) => s.selected);
  const trace = useStore((s) => s.trace);
  const [showSettings, setShowSettings] = useState(false);

  return (
    <div className="relative flex h-screen flex-col bg-surface text-ink">
      <header className="flex items-center justify-between border-b border-border px-4 py-2">
        <div className="flex items-center gap-2">
          <span className="font-semibold">AstroAssist</span>
          <span className="text-xs text-muted">research workbench</span>
        </div>
        <div className="flex items-center gap-2">
          <ThemeToggle />
          <button
            data-testid="open-settings"
            className="rounded-md border border-border px-2 py-1 text-xs text-muted hover:text-ink"
            onClick={() => setShowSettings(true)}
          >
            Settings
          </button>
        </div>
      </header>

      <div className="grid flex-1 grid-cols-[220px_1fr_360px] overflow-hidden">
        <aside className="overflow-y-auto border-r border-border p-3 text-sm">
          <RailSection title="Objects" />
          <RailSection title="Data" />
          <RailSection title="Plots" />
          <RailSection title="Papers" />
        </aside>

        <main className="overflow-hidden border-r border-border">
          <Chat />
        </main>

        <aside className="overflow-y-auto p-3" data-testid="artifact-viewer">
          <h2 className="mb-2 text-sm font-semibold text-muted">Artifact viewer</h2>
          {selected ? (
            <ArtifactCard artifact={selected} />
          ) : artifacts.length ? (
            <div className="space-y-2">
              {artifacts.map((a) => (
                <ArtifactCard key={a.id} artifact={a} />
              ))}
            </div>
          ) : (
            <p className="text-sm text-muted">No artifacts yet.</p>
          )}
        </aside>
      </div>

      <footer className="border-t border-border px-4 py-1 text-xs text-muted" data-testid="trace-bar">
        RESEARCH TRACE · {trace.length} steps
      </footer>

      {showSettings ? <Settings onClose={() => setShowSettings(false)} /> : null}
    </div>
  );
}

function RailSection({ title }: { title: string }) {
  return (
    <div className="mb-3">
      <div className="text-xs font-semibold uppercase tracking-wide text-muted">{title}</div>
      <div className="mt-1 text-xs text-muted/70">—</div>
    </div>
  );
}
