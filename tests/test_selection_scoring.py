from goldenforge.models import Trace
from goldenforge.select.scoring import selection_score


def test_selection_score_negative_feedback():
    trace = Trace(
        id="trace_001",
        input="Hello",
        output="Wrong answer",
        feedback="negative",
    )

    assert selection_score(trace) == 5.0


def test_selection_score_rewards_evaluation():
    trace = Trace(
        id="trace_002",
        input="Question",
        output="Answer",
        feedback="negative",
        evaluation={"correct": False},
    )

    assert selection_score(trace) == 7.0


def test_selection_score_rewards_rich_context():
    trace = Trace(
        id="trace_003",
        input="Question",
        output="Answer",
        feedback="negative",
        evaluation={"correct": False},
        context={"documents": ["doc1"]},
        tools=[{"name": "search"}],
        metadata={"source": "production"},
    )

    assert selection_score(trace) == 10.0


def test_selection_score_without_feedback():
    trace = Trace(
        id="trace_004",
        input="Hello",
        output="World",
    )

    assert selection_score(trace) == 2.0
