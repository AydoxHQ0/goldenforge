from pathlib import Path
from typing import Iterator
import json

from goldenforge.models import Trace


def load_jsonl(path: str | Path) -> Iterator[Trace]:
    """Load production AI traces from a JSONL file."""

    path = Path(path)

    with path.open("r", encoding="utf-8") as file:
        for line_number, line in enumerate(file, start=1):
            line = line.strip()

            if not line:
                continue

            try:
                data = json.loads(line)
                yield Trace.model_validate(data)
            except Exception as exc:
                raise ValueError(
                    f"Invalid JSONL record at line {line_number}: {exc}"
                ) from exc
