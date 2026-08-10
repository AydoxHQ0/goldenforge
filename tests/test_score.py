from goldenforge.models import Trace
from goldenforge.score.basic import score_trace


def test_score_positive_feedback():
    trace = Trace(
        id="trace_001",
        input="How do I cancel my subscription?",
        output="You can cancel your subscription from Settings > Billing.",
        feedback="positive",
    )

    assert score_trace(trace) == 1.0


def test_score_negative_feedback():
    trace = Trace(
        id="trace_002",
        input="How do I cancel my subscription?",
        output="I don't know.",
        feedback="negative",
    )

    assert score_trace(trace) == 0.0


def test_score_without_feedback():
    trace = Trace(
        id="trace_003",
        input="Hello",
        output="Hello!",
    )

    assert score_trace(trace) == 0.5
