from collections.abc import Iterable
from pathlib import Path

from goldenforge.curate.basic import curate_candidates
from goldenforge.dataset.golden import build_golden_dataset
from goldenforge.dedupe.basic import deduplicate_traces
from goldenforge.discover.basic import discover_candidates
from goldenforge.ingest.jsonl import load_jsonl
from goldenforge.models import Trace
from goldenforge.normalize.basic import normalize_trace
from goldenforge.validate.basic import validate_trace


def build_pipeline(traces: Iterable[Trace]) -> list[dict]:
    """Run the GoldenForge pipeline on production traces."""

    valid_traces: list[Trace] = []

    for trace in traces:
        if validate_trace(trace) == []:
            valid_traces.append(normalize_trace(trace))

    deduplicated = deduplicate_traces(valid_traces)
    candidates = discover_candidates(deduplicated)
    curated = curate_candidates(candidates, max_items=2)

    return build_golden_dataset(
        [candidate.trace for candidate in curated]
    )


def build_pipeline_from_jsonl(path: str | Path) -> list[dict]:
    """Build a Golden Dataset directly from a JSONL trace file."""

    return build_pipeline(load_jsonl(path))
