from goldenforge.models import Trace
from goldenforge.select.basic import select_traces


def test_select_traces_returns_negative_feedback():
    trace = Trace(
        id="trace_001",
        input="Hello",
        output="Wrong answer",
        feedback="negative",
    )

    selected = select_traces([trace])

    assert selected == [trace]


def test_select_traces_ignores_positive_feedback():
    trace = Trace(
        id="trace_002",
        input="Hello",
        output="Correct answer",
        feedback="positive",
    )

    selected = select_traces([trace])

    assert selected == []


def test_select_traces_handles_multiple_traces():
    negative = Trace(
        id="trace_003",
        input="Question 1",
        output="Bad answer",
        feedback="negative",
    )

    positive = Trace(
        id="trace_004",
        input="Question 2",
        output="Good answer",
        feedback="positive",
    )

    selected = select_traces([negative, positive])

    assert selected == [negative]


def test_select_traces_handles_empty_input():
    selected = select_traces([])

    assert selected == []
