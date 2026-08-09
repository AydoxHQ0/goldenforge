from goldenforge.models import Trace
from goldenforge.normalize.basic import normalize_trace


def test_normalize_trace_strips_text():
    trace = Trace(
        id="trace_001",
        input="  Hello world  ",
        output="  This is a response.  ",
    )

    normalized = normalize_trace(trace)

    assert normalized.input == "Hello world"
    assert normalized.output == "This is a response."


def test_normalize_trace_preserves_original():
    trace = Trace(
        id="trace_002",
        input="  Hello  ",
        output="  World  ",
    )

    normalized = normalize_trace(trace)

    assert trace.input == "  Hello  "
    assert trace.output == "  World  "

    assert normalized.input == "Hello"
    assert normalized.output == "World"


def test_normalize_trace_preserves_metadata():
    trace = Trace(
        id="trace_003",
        input="  Question  ",
        output="  Answer  ",
        model="example-model",
        feedback="positive",
        metadata={"source": "production"},
    )

    normalized = normalize_trace(trace)

    assert normalized.model == "example-model"
    assert normalized.feedback == "positive"
    assert normalized.metadata == {"source": "production"}
