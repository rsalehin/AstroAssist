/** @type {import('tailwindcss').Config} */
export default {
  darkMode: "class",
  content: ["./index.html", "./src/**/*.{ts,tsx}"],
  theme: {
    extend: {
      colors: {
        // Semantic tokens; concrete values live in src/theme/tokens.ts and index.css.
        surface: "rgb(var(--aa-surface) / <alpha-value>)",
        panel: "rgb(var(--aa-panel) / <alpha-value>)",
        ink: "rgb(var(--aa-ink) / <alpha-value>)",
        muted: "rgb(var(--aa-muted) / <alpha-value>)",
        accent: "rgb(var(--aa-accent) / <alpha-value>)",
        border: "rgb(var(--aa-border) / <alpha-value>)",
      },
    },
  },
  plugins: [],
};
