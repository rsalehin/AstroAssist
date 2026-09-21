import { expect, test } from "@playwright/test";

test("echo round-trip renders an artifact card", async ({ page }) => {
  await page.goto("/");

  const input = page.getByTestId("composer-input");
  await expect(input).toBeEnabled();
  await input.fill("hello");
  await page.getByTestId("composer-send").click();

  const card = page.getByTestId("artifact-card").first();
  await expect(card).toBeVisible();
  await expect(card).toHaveAttribute("data-kind", "ScientificValue");
  await expect(card).toContainText("Echo of: hello");
});
