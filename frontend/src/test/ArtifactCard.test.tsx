import { render, screen } from "@testing-library/react";
import userEvent from "@testing-library/user-event";
import { describe, expect, it, vi } from "vitest";

import { ArtifactCard } from "../components/ArtifactCard";
import type { Artifact } from "../types/artifacts";
import { echoValue, resolvedObject, scientificValue } from "./fixtures/artifacts";

describe("ArtifactCard", () => {
  it("renders a ScientificValue with kind, summary and value", () => {
    render(<ArtifactCard artifact={echoValue as Artifact} />);
    expect(screen.getByTestId("artifact-card")).toHaveAttribute("data-kind", "ScientificValue");
    expect(screen.getByText(echoValue.summary)).toBeInTheDocument();
    expect(screen.getByTestId("artifact-value")).toHaveTextContent("5");
  });

  it("shows unit and source for a Gaia distance value", () => {
    render(<ArtifactCard artifact={scientificValue as Artifact} />);
    expect(screen.getByTestId("artifact-value")).toHaveTextContent("pc");
    expect(screen.getByText("Gaia DR3")).toBeInTheDocument();
  });

  it("renders a non-value artifact from its summary", () => {
    render(<ArtifactCard artifact={resolvedObject as Artifact} />);
    expect(screen.getByText(resolvedObject.summary)).toBeInTheDocument();
    expect(screen.getByTestId("artifact-card")).toHaveAttribute("data-kind", "ResolvedObject");
  });

  it("fires onSelect when clicked", async () => {
    const onSelect = vi.fn();
    render(<ArtifactCard artifact={echoValue as Artifact} onSelect={onSelect} />);
    await userEvent.click(screen.getByTestId("artifact-card"));
    expect(onSelect).toHaveBeenCalledOnce();
  });
});
