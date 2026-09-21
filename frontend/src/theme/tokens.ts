// Design tokens (mirrored from the Figma token set; see docs/UI_UX.md).
// Concrete color values live as CSS variables in index.css; these names document intent.
export const tokens = {
  color: {
    surface: "var(--aa-surface)",
    panel: "var(--aa-panel)",
    ink: "var(--aa-ink)",
    muted: "var(--aa-muted)",
    accent: "var(--aa-accent)",
    border: "var(--aa-border)",
  },
  radius: { card: "0.75rem", chip: "9999px" },
  space: { pane: "1rem" },
} as const;

export type ThemeName = "dark" | "light";
