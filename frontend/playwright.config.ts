import { defineConfig } from "@playwright/test";

const BACKEND = "http://127.0.0.1:8765";
const FRONTEND = "http://127.0.0.1:5173";

export default defineConfig({
  testDir: "./e2e",
  timeout: 30_000,
  expect: { timeout: 10_000 },
  fullyParallel: false,
  reporter: process.env.CI ? "list" : "line",
  use: { baseURL: FRONTEND, trace: "on-first-retry" },
  webServer: [
    {
      // Backend in mock profile with an isolated data dir.
      command:
        "uv run astroassist serve --host 127.0.0.1 --port 8765 --profile mock --no-open-browser",
      cwd: "..",
      url: `${BACKEND}/api/health`,
      reuseExistingServer: !process.env.CI,
      timeout: 120_000,
      env: { ASTROASSIST_MODEL_PROFILE: "mock", ASTROASSIST_DATA_DIR: "frontend/.e2e-tmp" },
    },
    {
      command: "npm run dev -- --port 5173 --strictPort",
      url: FRONTEND,
      reuseExistingServer: !process.env.CI,
      timeout: 120_000,
    },
  ],
});
