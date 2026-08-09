from goldenforge.models import Trace
from goldenforge.validate.basic import validate_trace


def test_validate_trace_accepts_valid_trace():
    trace = Trace(
        id="trace_001",
        input="Hello",
        output="World",
    )

    assert validate_trace(trace) == []


def test_validate_trace_detects_empty_id():
    trace = Trace(
        id="   ",
        input="Hello",
        output="World",
    )

    errors = validate_trace(trace)

    assert "Trace id must not be empty." in errors


def test_validate_trace_detects_empty_input():
    trace = Trace(
        id="trace_001",
        input="   ",
        output="World",
    )

    errors = validate_trace(trace)

    assert "Trace input must not be empty." in errors


def test_validate_trace_detects_empty_output():
    trace = Trace(
        id="trace_001",
        input="Hello",
        output="   ",
    )

    errors = validate_trace(trace)

    assert "Trace output must not be empty." in errors


def test_validate_trace_detects_multiple_errors():
    trace = Trace(
        id="   ",
        input="   ",
        output="   ",
    )

    errors = validate_trace(trace)

    assert len(errors) == 3
    assert "Trace id must not be empty." in errors
    assert "Trace input must not be empty." in errors
    assert "Trace output must not be empty." in errors
