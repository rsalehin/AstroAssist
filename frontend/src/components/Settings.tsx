import { useEffect, useState } from "react";

import { getSettings, type PublicSettings } from "../api/client";

export function Settings({ onClose }: { onClose: () => void }) {
  const [settings, setSettings] = useState<PublicSettings | null>(null);

  useEffect(() => {
    getSettings()
      .then(setSettings)
      .catch(() => setSettings(null));
  }, []);

  return (
    <div className="absolute inset-0 z-10 flex items-start justify-center bg-black/40 p-8">
      <div className="w-full max-w-md rounded-card border border-border bg-panel p-5" role="dialog">
        <div className="mb-3 flex items-center justify-between">
          <h2 className="text-lg font-semibold text-ink">Settings</h2>
          <button className="text-muted hover:text-ink" onClick={onClose} aria-label="Close">
            ✕
          </button>
        </div>
        {settings ? (
          <dl className="space-y-2 text-sm">
            <Row label="Model profile" value={settings.model_profile} />
            <Row label="Cache mode" value={settings.cache_mode} />
            <Row label="LangSmith tracing" value={String(settings.langsmith_tracing)} />
            <Row label="Backend" value={`${settings.host}:${settings.port}`} />
          </dl>
        ) : (
          <p className="text-sm text-muted">Loading…</p>
        )}
        <p className="mt-4 text-xs text-muted">
          Credentials are managed via the OS keyring and are never shown here.
        </p>
      </div>
    </div>
  );
}

function Row({ label, value }: { label: string; value: string }) {
  return (
    <div className="flex justify-between border-b border-border pb-1">
      <dt className="text-muted">{label}</dt>
      <dd className="font-mono text-ink">{value}</dd>
    </div>
  );
}
