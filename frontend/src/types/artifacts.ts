// TypeScript shapes mirroring astroassist.core.artifacts. Kept intentionally loose:
// the generic card renders any artifact from `kind` + `summary` + known fields.

export interface Provenance {
  artifact_id: string;
  method: string;
  source?: string | null;
  source_version?: string | null;
  tool?: string | null;
  citation_keys?: string[];
}

export interface QuantityValue {
  value: number | number[];
  unit: string;
}

export interface BaseArtifact {
  id: string;
  kind: string;
  summary: string;
  provenance: Provenance;
  parent_id?: string | null;
  [key: string]: unknown;
}

export type Artifact = BaseArtifact;

export interface StreamEvent {
  type: "trace" | "artifact" | "token" | "interrupt" | "done";
  [key: string]: unknown;
}
