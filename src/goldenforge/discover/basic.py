import re
from collections import Counter
from collections.abc import Iterable

from goldenforge.cluster.basic import cluster_traces
from goldenforge.models import Candidate, Trace
from goldenforge.select.scoring import selection_score


def _calculate_rarity(traces: list[Trace]) -> dict[str, float]:
    """Calculate input rarity across the complete production dataset."""

    frequencies = Counter(
        trace.input.strip()
        for trace in traces
    )

    return {
        input_text: 1.0 / frequency
        for input_text, frequency in frequencies.items()
    }


def _tokenize(text: str) -> set[str]:
    """Normalize text into a set of lowercase word tokens."""

    return set(re.findall(r"\b\w+\b", text.lower()))


def _jaccard_similarity(left: set[str], right: set[str]) -> float:
    """Calculate Jaccard similarity between two token sets."""

    if not left and not right:
        return 1.0

    if not left or not right:
        return 0.0

    return len(left & right) / len(left | right)


def _calculate_novelty(traces: list[Trace]) -> dict[str, float]:
    """Calculate lexical novelty against the other production traces."""

    tokenized = {
        trace.id: _tokenize(trace.input)
        for trace in traces
    }

    novelty: dict[str, float] = {}

    for trace in traces:
        current = tokenized[trace.id]
        max_similarity = 0.0

        for other in traces:
            if other.id == trace.id:
                continue

            similarity = _jaccard_similarity(
                current,
                tokenized[other.id],
            )
            max_similarity = max(max_similarity, similarity)

        novelty[trace.id] = 1.0 - max_similarity

    return novelty


def _calculate_diversity(traces: list[Trace]) -> dict[str, float]:
    """Calculate diversity from the representation of each cluster."""

    clusters = cluster_traces(traces)

    diversity: dict[str, float] = {}

    for cluster in clusters:
        cluster_size = len(cluster)
        signal = 1.0 / cluster_size

        for trace in cluster:
            diversity[trace.id] = signal

    return diversity


def discover_candidates(traces: Iterable[Trace]) -> list[Candidate]:
    """Discover production traces that are worth considering as Golden Cases."""

    all_traces = list(traces)
    rarity_by_input = _calculate_rarity(all_traces)
    novelty_by_id = _calculate_novelty(all_traces)
    diversity_by_id = _calculate_diversity(all_traces)

    candidates: list[Candidate] = []

    for trace in all_traces:
        if trace.feedback != "negative":
            continue

        score = selection_score(trace)
        rarity = rarity_by_input[trace.input.strip()]
        novelty = novelty_by_id[trace.id]
        diversity = diversity_by_id[trace.id]

        signals = {
            "failure": 1.0,
            "rarity": rarity,
            "novelty": novelty,
            "diversity": diversity,
            "evaluation": 1.0 if trace.evaluation else 0.0,
            "context": 1.0 if trace.context else 0.0,
            "tools": 1.0 if trace.tools else 0.0,
            "metadata": 1.0 if trace.metadata else 0.0,
        }

        reasons = ["negative user feedback"]

        if rarity == 1.0:
            reasons.append("rare production behavior")

        if novelty >= 0.8:
            reasons.append("high lexical novelty")

        if diversity == 1.0:
            reasons.append("unique behavioral cluster")

        if trace.evaluation:
            reasons.append("evaluation data available")

        if trace.context:
            reasons.append("rich context available")

        if trace.tools:
            reasons.append("tool usage available")

        if trace.metadata:
            reasons.append("production metadata available")

        candidates.append(
            Candidate(
                trace=trace,
                score=score,
                signals=signals,
                reason="; ".join(reasons),
            )
        )

    return sorted(
        candidates,
        key=lambda candidate: (
            candidate.score,
            candidate.signals["rarity"],
            candidate.signals["diversity"],
        ),
        reverse=True,
    )