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

def test_select_traces_ranks_by_selection_score():
    low_value = Trace(
        id="trace_005",
        input="Question",
        output="Wrong answer",
        feedback="negative",
    )

    high_value = Trace(
        id="trace_006",
        input="Complex question",
        output="Wrong answer",
        feedback="negative",
        evaluation={"correct": False},
        context={"documents": ["doc1"]},
        tools=[{"name": "search"}],
        metadata={"source": "production"},
    )

    selected = select_traces([low_value, high_value])

    assert selected == [high_value, low_value]
