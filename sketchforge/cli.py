# Typer/Click CLI entry point
import typer
from typing import Optional
from .watcher import start_watcher
from sketchforge.engine.capturer import ProjectCapturer
from sketchforge.utils import create_backup # Add this
from sketchforge.tui import SketchForgeApp

from sketchforge.core import parse
from sketchforge.engine.generator import ProjectGenerator

app = typer.Typer()

@app.command()
def watch(
    sketch_file: str = typer.Argument(..., help="Path to your live_sketch.txt file"),
    output: str = typer.Option(".", help="Directory where code is generated")
):
    """
    Watches a sketch file and auto-updates the project in real-time.
    """
    typer.echo(f"🚀 SketchForge initializing for {sketch_file}...")
    start_watcher(sketch_file, output)


@app.command()
def capture(
        path: str = typer.Argument(".", help="Path to the existing project"),
        output: str = typer.Option("sketch.txt", help="Output sketch file name")
):
    """
    Reverse engineers a project. Creates a timestamped backup if output exists.
    """
    typer.echo(f"📸 Capturing structure of '{path}'...")

    capturer = ProjectCapturer(path)
    result = capturer.capture()

    # --- SAFETY LAYER ---
    create_backup(output)
    # --------------------

    with open(output, "w", encoding="utf-8") as f:
        f.write(result)

    typer.echo(f"✅ Captured! Saved to {output}")

@app.command()
def interactive(
    sketch_file: str = typer.Argument("sketch.txt", help="File to edit")
):
    """
    Launches the Interactive Terminal UI.
    """
    app = SketchForgeApp(sketch_file)
    app.run()


@app.command()
def build(
        sketch_file: str = typer.Argument(..., help="Path to the sketch file"),
        output: str = typer.Option(".", help="Directory to generate code in")
):
    """
    Generates the project structure from a sketch file (One-time build).
    """
    typer.echo(f"🔨 Building project from {sketch_file}...")

    try:
        # 1. Read
        with open(sketch_file, "r", encoding="utf-8") as f:
            content = f.read()

        # 2. Parse (Rust)
        tree = parse(content)

        # 3. Generate (Python)
        generator = ProjectGenerator(output)
        generator.generate(tree)

        typer.echo(f"✅ Build complete in '{output}'")

    except FileNotFoundError:
        typer.echo(f"❌ Error: File '{sketch_file}' not found.")
    except Exception as e:
        typer.echo(f"❌ Unexpected error: {e}")

if __name__ == "__main__":
    app()