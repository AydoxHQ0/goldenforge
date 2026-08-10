from goldenforge.models import Trace


def score_trace(trace: Trace) -> float:
    """Return a simple quality score for a trace."""

    if trace.feedback == "positive":
        return 1.0

    if trace.feedback == "negative":
        return 0.0

    return 0.5
