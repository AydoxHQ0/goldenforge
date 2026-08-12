from collections.abc import Iterable

from goldenforge.models import Trace


def deduplicate_traces(traces: Iterable[Trace]) -> list[Trace]:
    """Remove exact duplicate traces while preserving order."""
    seen: set[tuple[str, str]] = set()
    unique: list[Trace] = []

    for trace in traces:
        key = (trace.input.strip(), trace.output.strip())

        if key in seen:
            continue

        seen.add(key)
        unique.append(trace)

    return unique
