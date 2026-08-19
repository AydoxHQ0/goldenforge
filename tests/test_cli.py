from typer.testing import CliRunner

from goldenforge.cli import app


runner = CliRunner()


def test_version_command():
    result = runner.invoke(app, ["version"])

    assert result.exit_code == 0
    assert "GoldenForge v0.1.0" in result.stdout


def test_hello_command():
    result = runner.invoke(app, ["hello"])

    assert result.exit_code == 0
    assert "GoldenForge is ready." in result.stdout


def test_build_command(monkeypatch, tmp_path):
    input_path = tmp_path / "traces.jsonl"
    output_path = tmp_path / "golden.json"

    input_path.write_text('{"id": "trace_001"}\n', encoding="utf-8")

    expected_dataset = [
        {
            "input": "Hello",
            "output": "World",
        }
    ]

    exported = {}

def fake_build_pipeline(path, max_items):
    assert path == input_path
    assert max_items == 2
    return expected_dataset

    def fake_export_json(dataset, path):
        exported["dataset"] = dataset
        exported["path"] = path

    monkeypatch.setattr(
        "goldenforge.cli.build_pipeline_from_jsonl",
        fake_build_pipeline,
    )

    monkeypatch.setattr(
        "goldenforge.cli.export_json",
        fake_export_json,
    )

    result = runner.invoke(
        app,
        ["build", str(input_path), str(output_path)],
    )

    assert result.exit_code == 0
    assert "Golden Dataset created successfully." in result.stdout
    assert exported["dataset"] == expected_dataset
    assert exported["path"] == output_path

def test_build_command_accepts_max_items(monkeypatch, tmp_path):
    input_path = tmp_path / "traces.jsonl"
    output_path = tmp_path / "golden.json"

    input_path.write_text('{"id": "trace_001"}\n', encoding="utf-8")

    captured = {}

    def fake_build_pipeline(path, max_items):
        captured["path"] = path
        captured["max_items"] = max_items
        return [{"input": "Hello", "output": "World"}]

    def fake_export_json(dataset, path):
        captured["dataset"] = dataset
        captured["output_path"] = path

    monkeypatch.setattr(
        "goldenforge.cli.build_pipeline_from_jsonl",
        fake_build_pipeline,
    )

    monkeypatch.setattr(
        "goldenforge.cli.export_json",
        fake_export_json,
    )

    result = runner.invoke(
        app,
        [
            "build",
            str(input_path),
            str(output_path),
            "--max-items",
            "1",
        ],
    )

    assert result.exit_code == 0
    assert captured["path"] == input_path
    assert captured["max_items"] == 1
    assert captured["dataset"] == [
        {"input": "Hello", "output": "World"}
    ]
    assert captured["output_path"] == output_path

def test_build_help_includes_max_items():
    result = runner.invoke(app, ["build", "--help"])

    assert result.exit_code == 0
    assert "--max-items" in result.stdout
    assert "Maximum number of Golden Dataset examples" in result.stdout
