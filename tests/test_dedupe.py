from goldenforge.models import Trace
from goldenforge.dedupe.basic import deduplicate_traces


def test_deduplicate_traces_removes_exact_duplicates():
    first = Trace(
        id="trace_001",
        input="Hello",
        output="World",
    )

    duplicate = Trace(
        id="trace_002",
        input="Hello",
        output="World",
    )

    unique = Trace(
        id="trace_003",
        input="Goodbye",
        output="World",
    )

    result = deduplicate_traces([first, duplicate, unique])

    assert result == [first, unique]


def test_deduplicate_traces_ignores_whitespace():
    first = Trace(
        id="trace_001",
        input="Hello",
        output="World",
    )

    duplicate = Trace(
        id="trace_002",
        input=" Hello ",
        output=" World ",
    )

    result = deduplicate_traces([first, duplicate])

    assert result == [first]


def test_deduplicate_traces_preserves_order():
    first = Trace(
        id="trace_001",
        input="Question 1",
        output="Answer 1",
    )

    second = Trace(
        id="trace_002",
        input="Question 2",
        output="Answer 2",
    )

    result = deduplicate_traces([first, second])

    assert result == [first, second]


def test_deduplicate_traces_handles_empty_input():
    assert deduplicate_traces([]) == []
