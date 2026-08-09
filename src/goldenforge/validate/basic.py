from goldenforge.models import Trace


def validate_trace(trace: Trace) -> list[str]:
    """Return validation errors for a Trace."""

    errors: list[str] = []

    if not trace.id.strip():
        errors.append("Trace id must not be empty.")

    if not trace.input.strip():
        errors.append("Trace input must not be empty.")

    if not trace.output.strip():
        errors.append("Trace output must not be empty.")

    return errors
