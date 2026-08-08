import typer
from rich.console import Console

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


if __name__ == "__main__":
    app()
