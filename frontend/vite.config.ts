/// <reference types="vitest/config" />
import react from "@vitejs/plugin-react";
import { defineConfig } from "vite";

export default defineConfig({
  plugins: [react()],
  server: {
    // Bind IPv4 explicitly so Windows (where `localhost` may resolve to ::1) matches the
    // 127.0.0.1 URLs used by Playwright and the dev proxy.
    host: "127.0.0.1",
    port: 5173,
    strictPort: true,
    proxy: {
      // Dev: proxy API calls to the FastAPI backend.
      "/api": "http://127.0.0.1:8765",
    },
  },
  test: {
    globals: true,
    environment: "jsdom",
    setupFiles: ["./src/test/setup.ts"],
    include: ["src/**/*.test.{ts,tsx}"],
    css: true,
  },
});
