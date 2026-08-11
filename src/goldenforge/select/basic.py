from collections.abc import Iterable

from goldenforge.models import Trace
from goldenforge.select.scoring import selection_score


def select_traces(traces: Iterable[Trace]) -> list[Trace]:
    """Select and rank traces with negative user feedback."""

    selected = [
        trace
        for trace in traces
        if trace.feedback == "negative"
    ]

    return sorted(
        selected,
        key=selection_score,
        reverse=True,
    )
