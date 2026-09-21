"""Command-line entry point. `astroassist serve` starts the local workbench."""

from __future__ import annotations

from pathlib import Path

import typer

from astroassist import __version__

app = typer.Typer(help="AstroAssist — provenance-first research workbench for astronomers.")

eval_app = typer.Typer(help="Evaluation, fixtures and benchmarks.")
app.add_typer(eval_app, name="eval")


@app.command()
def version() -> None:
    """Print the installed version."""
    typer.echo(__version__)


@eval_app.command("fixtures")
def eval_fixtures(
    ts: bool = typer.Option(False, "--ts", help="Emit a TypeScript fixtures module."),
    out: Path | None = typer.Option(None, "--out", help="Output path (defaults per format)."),
) -> None:
    """Generate artifact fixtures shared by backend tests and the frontend [F-EVAL-001]."""
    from astroassist.eval.fixtures import write_ts_fixtures

    if not ts:
        typer.echo("Only --ts is supported in M0.")
        raise typer.Exit(code=2)
    written = write_ts_fixtures(out)
    typer.echo(f"Wrote {written}")


@app.command()
def serve(
    host: str = "127.0.0.1",
    port: int = 8765,
    profile: str | None = typer.Option(None, "--profile", help="Model profile (e.g. mock)."),
    open_browser: bool = typer.Option(True, "--open-browser/--no-open-browser"),
) -> None:
    """Start the local FastAPI backend and (optionally) open the browser workbench."""
    import os

    if profile:
        os.environ["ASTROASSIST_MODEL_PROFILE"] = profile

    import uvicorn

    from astroassist.core.config import load_settings
    from astroassist.server.app import create_app

    settings = load_settings()
    settings.host, settings.port = host, port
    app_instance = create_app(settings)

    if open_browser:
        import threading
        import webbrowser

        threading.Timer(1.0, lambda: webbrowser.open(f"http://{host}:{port}")).start()

    typer.echo(f"AstroAssist serving on http://{host}:{port} (profile={settings.model_profile})")
    uvicorn.run(app_instance, host=host, port=port, log_level="info")


if __name__ == "__main__":
    app()
