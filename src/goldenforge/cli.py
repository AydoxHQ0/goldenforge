from pathlib import Path

import typer
from rich.console import Console

from goldenforge.dataset.export import export_json
from goldenforge.dataset.golden import build_golden_dataset
from goldenforge.ingest.jsonl import load_jsonl
from goldenforge.normalize.basic import normalize_trace
from goldenforge.select.basic import select_traces
from goldenforge.validate.basic import validate_trace


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
    input_path: Path,
    output_path: Path,
):
    """Build a Golden Dataset from a JSONL trace file."""

    traces = list(load_jsonl(input_path))

    normalized = [
        normalize_trace(trace)
        for trace in traces
    ]

    valid = [
        trace
        for trace in normalized
        if not validate_trace(trace)
    ]

    selected = select_traces(valid)

    dataset = build_golden_dataset(selected)

    export_json(dataset, output_path)

    console.print(
        f"Processed {len(traces)} traces → "
        f"{len(selected)} selected → "
        f"{len(dataset)} Golden Dataset examples."
    )

    console.print(f"Exported to: {output_path}")


if __name__ == "__main__":
    app()
