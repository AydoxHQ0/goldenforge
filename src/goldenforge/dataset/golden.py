from goldenforge.models import Trace


def build_golden_dataset(traces: list[Trace]) -> list[dict]:
    """Convert selected traces into Golden Dataset examples."""

    dataset = []

    for trace in traces:
        dataset.append(
            {
                "id": trace.id,
                "input": trace.input,
                "output": trace.output,
                "metadata": trace.metadata,
            }
        )

    return dataset
