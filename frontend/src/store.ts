import { create } from "zustand";

import type { Artifact } from "./types/artifacts";

interface AppState {
  artifacts: Artifact[];
  selected: Artifact | null;
  trace: Record<string, unknown>[];
  addArtifact: (a: Artifact) => void;
  addTrace: (t: Record<string, unknown>) => void;
  select: (a: Artifact | null) => void;
}

export const useStore = create<AppState>((set) => ({
  artifacts: [],
  selected: null,
  trace: [],
  addArtifact: (a) => set((s) => ({ artifacts: [...s.artifacts, a] })),
  addTrace: (t) => set((s) => ({ trace: [...s.trace, t] })),
  select: (a) => set({ selected: a }),
}));
