from goldenforge.models import Trace


def normalize_trace(trace: Trace) -> Trace:
    """Normalize a trace into a consistent representation."""

    normalized = trace.model_copy(deep=True)

    normalized.input = normalized.input.strip()
    normalized.output = normalized.output.strip()

    if normalized.feedback is not None:
        normalized.feedback = normalized.feedback.strip()

    return normalized
