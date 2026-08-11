from goldenforge.models import Trace


def selection_score(trace: Trace) -> float:
    """Return a transparent value score for Golden Dataset selection."""

    score = 0.0

    if trace.feedback == "negative":
        score += 3.0

    if trace.evaluation:
        score += 2.0

    if trace.context:
        score += 1.0

    if trace.tools:
        score += 1.0

    if trace.metadata:
        score += 1.0

    if trace.input.strip():
        score += 1.0

    if trace.output.strip():
        score += 1.0

    return score
