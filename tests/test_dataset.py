from goldenforge.dataset.golden import build_golden_dataset
from goldenforge.models import Trace


def test_build_golden_dataset():
    traces = [
        Trace(
            id="trace_001",
            input="How do I cancel my subscription?",
            output="Go to Settings > Billing.",
            feedback="positive",
        ),
        Trace(
            id="trace_002",
            input="How do I reset my password?",
            output="Use the password reset page.",
            feedback="positive",
        ),
    ]

    dataset = build_golden_dataset(traces)

    assert len(dataset) == 2
    assert dataset[0]["id"] == "trace_001"
    assert dataset[0]["input"] == "How do I cancel my subscription?"
    assert dataset[0]["output"] == "Go to Settings > Billing."
    assert dataset[0]["metadata"] == {}
