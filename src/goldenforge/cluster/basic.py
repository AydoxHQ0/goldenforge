from collections.abc import Iterable

from goldenforge.models import Trace


def _tokenize(text: str) -> set[str]:
    """Normalize text into lowercase word tokens."""

    return set(text.lower().split())


def _jaccard_similarity(left: set[str], right: set[str]) -> float:
    """Calculate Jaccard similarity between two token sets."""

    if not left and not right:
        return 1.0

    if not left or not right:
        return 0.0

    return len(left & right) / len(left | right)


def cluster_traces(
    traces: Iterable[Trace],
    threshold: float = 0.5,
) -> list[list[Trace]]:
    """Group traces using deterministic lexical similarity."""

    clusters: list[list[Trace]] = []
    tokenized: dict[str, set[str]] = {}

    for trace in traces:
        tokens = _tokenize(trace.input)
        tokenized[trace.id] = tokens

        assigned = False

        for cluster in clusters:
            representative = cluster[0]
            similarity = _jaccard_similarity(
                tokens,
                tokenized[representative.id],
            )

            if similarity >= threshold:
                cluster.append(trace)
                assigned = True
                break

        if not assigned:
            clusters.append([trace])

    return clusters