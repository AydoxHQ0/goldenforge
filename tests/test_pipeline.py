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

def test_pipeline_curates_discovered_candidates():
    traces = [
        Trace(
            id="trace_020",
            input="Question 1",
            output="Wrong answer",
            feedback="negative",
        ),
        Trace(
            id="trace_021",
            input="Question 2",
            output="Wrong answer",
            feedback="positive",
        ),
    ]

    result = build_pipeline(traces)

    assert len(result) == 1
    assert result[0]["id"] == "trace_020"
def test_pipeline_applies_curation_limit():
    traces = [
        Trace(
            id="trace_022",
            input="Question 1",
            output="Wrong answer",
            feedback="negative",
        ),
        Trace(
            id="trace_023",
            input="Question 2",
            output="Wrong answer",
            feedback="negative",
        ),
        Trace(
            id="trace_024",
            input="Question 3",
            output="Wrong answer",
            feedback="negative",
        ),
    ]

    result = build_pipeline(traces)

    assert len(result) == 2

def test_pipeline_accepts_curation_limit():
    traces = [
        Trace(
            id="trace_025",
            input="Question 1",
            output="Wrong answer",
            feedback="negative",
        ),
        Trace(
            id="trace_026",
            input="Question 2",
            output="Wrong answer",
            feedback="negative",
        ),
        Trace(
            id="trace_027",
            input="Question 3",
            output="Wrong answer",
            feedback="negative",
        ),
    ]

    result = build_pipeline(traces, max_items=1)

    assert len(result) == 1

def test_pipeline_allows_unlimited_curation():
    traces = [
        Trace(
            id="trace_028",
            input="Question 1",
            output="Wrong answer",
            feedback="negative",
        ),
        Trace(
            id="trace_029",
            input="Question 2",
            output="Wrong answer",
            feedback="negative",
        ),
        Trace(
            id="trace_030",
            input="Question 3",
            output="Wrong answer",
            feedback="negative",
        ),
    ]

    result = build_pipeline(traces, max_items=None)

    assert len(result) == 3