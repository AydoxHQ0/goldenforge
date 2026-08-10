from collections.abc import Iterable

from goldenforge.models import Trace


def select_traces(traces: Iterable[Trace]) -> list[Trace]:
    """Select traces with negative user feedback."""
    selected: list[Trace] = []

    for trace in traces:
        if trace.feedback == "negative":
            selected.append(trace)

    return selected
