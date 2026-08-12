from goldenforge.models import Trace
from goldenforge.pipeline.basic import build_pipeline


def test_pipeline_builds_golden_dataset():
    traces = [
        Trace(
            id="trace_001",
            input="Question 1",
            output="Bad answer",
            feedback="negative",
        ),
        Trace(
            id="trace_002",
            input="Question 2",
            output="Good answer",
            feedback="positive",
        ),
    ]

    result = build_pipeline(traces)

    assert len(result) == 1
    assert result[0]["id"] == "trace_001"
    assert result[0]["input"] == "Question 1"
    assert result[0]["output"] == "Bad answer"


def test_pipeline_normalizes_before_selection():
    traces = [
        Trace(
            id="trace_001",
            input="  Question  ",
            output="  Bad answer  ",
            feedback="negative",
        )
    ]

    result = build_pipeline(traces)

    assert result[0]["input"] == "Question"
    assert result[0]["output"] == "Bad answer"


def test_pipeline_removes_duplicates():
    traces = [
        Trace(
            id="trace_001",
            input="Question",
            output="Bad answer",
            feedback="negative",
        ),
        Trace(
            id="trace_002",
            input="Question",
            output="Bad answer",
            feedback="negative",
        ),
    ]

    result = build_pipeline(traces)

    assert len(result) == 1
    assert result[0]["id"] == "trace_001"


def test_pipeline_ignores_invalid_traces():
    traces = [
        Trace(
            id="",
            input="Question",
            output="Bad answer",
            feedback="negative",
        ),
        Trace(
            id="trace_002",
            input="Valid question",
            output="Valid answer",
            feedback="negative",
        ),
    ]

    result = build_pipeline(traces)

    assert len(result) == 1
    assert result[0]["id"] == "trace_002"


def test_pipeline_handles_empty_input():
    assert build_pipeline([]) == []
