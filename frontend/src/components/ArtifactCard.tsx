import type { Artifact, QuantityValue } from "../types/artifacts";

function formatQuantity(q: QuantityValue | undefined): string | null {
  if (!q) return null;
  const value = Array.isArray(q.value) ? `[${q.value.join(", ")}]` : String(q.value);
  return q.unit ? `${value} ${q.unit}` : value;
}

function KindBadge({ kind }: { kind: string }) {
  return (
    <span className="rounded-chip bg-accent/15 px-2 py-0.5 text-xs font-medium text-accent">
      {kind}
    </span>
  );
}

/** Generic artifact card: renders any artifact from kind + summary + known fields. */
export function ArtifactCard({
  artifact,
  onSelect,
}: {
  artifact: Artifact;
  onSelect?: (artifact: Artifact) => void;
}) {
  const prov = artifact.provenance;
  const quantity = formatQuantity(artifact.value as QuantityValue | undefined);

  return (
    <article
      data-testid="artifact-card"
      data-kind={artifact.kind}
      onClick={onSelect ? () => onSelect(artifact) : undefined}
      className="rounded-card border border-border bg-panel p-3 text-sm shadow-sm"
    >
      <header className="mb-1 flex items-center justify-between gap-2">
        <KindBadge kind={artifact.kind} />
        {prov?.source ? <span className="text-xs text-muted">{prov.source}</span> : null}
      </header>
      <p className="font-medium text-ink">{artifact.summary}</p>
      {quantity ? (
        <p className="mt-1 font-mono text-base text-ink" data-testid="artifact-value">
          {quantity}
        </p>
      ) : null}
      {prov ? (
        <footer className="mt-2 text-xs text-muted">
          method: {prov.method}
          {prov.tool ? ` · tool: ${prov.tool}` : ""}
        </footer>
      ) : null}
    </article>
  );
}
