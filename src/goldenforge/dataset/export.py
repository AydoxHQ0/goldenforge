import json
from pathlib import Path


def export_json(dataset: list[dict], output_path: str | Path) -> None:
    """Export a Golden Dataset to a JSON file."""

    path = Path(output_path)

    path.parent.mkdir(parents=True, exist_ok=True)

    with path.open("w", encoding="utf-8") as file:
        json.dump(dataset, file, indent=2, ensure_ascii=False)
