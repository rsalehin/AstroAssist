"""Command-line entry point. `astroassist serve` starts the local workbench."""

from __future__ import annotations

import typer

from astroassist import __version__

app = typer.Typer(help="AstroAssist — provenance-first research workbench for astronomers.")


@app.command()
def version() -> None:
    """Print the installed version."""
    typer.echo(__version__)


@app.command()
def serve(host: str = "127.0.0.1", port: int = 8765, open_browser: bool = True) -> None:
    """Start the local FastAPI backend and open the browser workbench (M0 implements this)."""
    typer.echo(
        f"astroassist serve on http://{host}:{port} — not implemented yet (see docs/IMPLEMENTATION_PLAN.md M0-8)"
    )
    raise typer.Exit(code=2)


if __name__ == "__main__":
    app()
