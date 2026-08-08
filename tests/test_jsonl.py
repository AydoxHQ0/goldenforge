from pathlib import Path

import pytest

from goldenforge.ingest.jsonl import load_jsonl
from goldenforge.models import Trace


def test_load_jsonl():
    path = Path("examples/sample.jsonl")

    traces = list(load_jsonl(path))

    assert len(traces) == 3
    assert all(isinstance(trace, Trace) for trace in traces)

    assert traces[0].id == "trace_001"
    assert traces[0].input == "How do I cancel my subscription?"
    assert traces[0].feedback == "negative"


def test_load_jsonl_skips_blank_lines(tmp_path):
    path = tmp_path / "sample.jsonl"

    path.write_text(
        '{"id":"trace_001","input":"Hello","output":"Hi"}\n'
        "\n"
        '{"id":"trace_002","input":"Bye","output":"Goodbye"}\n',
        encoding="utf-8",
    )

    traces = list(load_jsonl(path))

    assert len(traces) == 2


def test_load_jsonl_rejects_invalid_json(tmp_path):
    path = tmp_path / "invalid.jsonl"

    path.write_text(
        '{"id":"trace_001","input":"Hello","output":"Hi"}\n'
        '{"invalid json\n',
        encoding="utf-8",
    )

    with pytest.raises(ValueError, match="Invalid JSONL record at line 2"):
        list(load_jsonl(path))
