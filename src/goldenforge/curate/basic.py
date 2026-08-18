from collections.abc import Iterable

from goldenforge.models import Candidate


def curate_candidates(
    candidates: Iterable[Candidate],
    min_score: float = 0.0,
    max_items: int | None = None,
) -> list[Candidate]:
    """Curate discovered candidates into a bounded Golden Case set."""

    curated = [
        candidate
        for candidate in candidates
        if candidate.score >= min_score
    ]

    curated.sort(
        key=lambda candidate: candidate.score,
        reverse=True,
    )

    if max_items is not None:
        curated = curated[:max_items]

    return curated