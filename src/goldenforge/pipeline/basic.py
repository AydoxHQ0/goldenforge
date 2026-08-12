from collections.abc import Iterable
from pathlib import Path

from goldenforge.dataset.golden import build_golden_dataset
from goldenforge.dedupe.basic import deduplicate_traces
from goldenforge.ingest.jsonl import load_jsonl
from goldenforge.models import Trace
from goldenforge.normalize.basic import normalize_trace
from goldenforge.select.basic import select_traces
from goldenforge.validate.basic import validate_trace


def build_pipeline(traces: Iterable[Trace]) -> list[dict]:
    """Run the GoldenForge pipeline on production traces."""

    valid_traces: list[Trace] = []

    for trace in traces:
        if validate_trace(trace) == []:
            valid_traces.append(normalize_trace(trace))

    selected = select_traces(valid_traces)
    deduplicated = deduplicate_traces(selected)

    return build_golden_dataset(deduplicated)


def build_pipeline_from_jsonl(path: str | Path) -> list[dict]:
    """Build a Golden Dataset directly from a JSONL log file."""

    return build_pipeline(load_jsonl(path))
