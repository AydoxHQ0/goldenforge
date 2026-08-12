from pathlib import Path

import typer
from rich.console import Console

from goldenforge.dataset.export import export_json
from goldenforge.pipeline.basic import build_pipeline_from_jsonl


app = typer.Typer(
    name="goldenforge",
    help="Transform production AI traces into high-quality Golden Datasets.",
)

console = Console()


@app.command()
def version():
    """Show the GoldenForge version."""
    console.print("GoldenForge v0.1.0")


@app.command()
def hello():
    """Verify that GoldenForge is working."""
    console.print("GoldenForge is ready.")


@app.command()
def build(
    input_path: Path = typer.Argument(
        ...,
        help="Path to the input JSONL trace file.",
        exists=True,
        readable=True,
    ),
    output_path: Path = typer.Argument(
        ...,
        help="Path where the Golden Dataset JSON will be written.",
    ),
):
    """Build a Golden Dataset from a JSONL trace file."""

    dataset = build_pipeline_from_jsonl(input_path)

    output_path.parent.mkdir(parents=True, exist_ok=True)
    export_json(dataset, output_path)

    console.print(
        f"[green]Golden Dataset created successfully.[/green]\n"
        f"Examples: {len(dataset)}\n"
        f"Exported to: {output_path}"
    )


if __name__ == "__main__":
    app()
