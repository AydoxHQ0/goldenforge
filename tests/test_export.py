import json

from goldenforge.dataset.export import export_json


def test_export_json(tmp_path):
    dataset = [
        {
            "id": "trace_001",
            "input": "How do I cancel my subscription?",
            "output": "Go to Settings > Billing.",
            "metadata": {},
        }
    ]

    output_file = tmp_path / "golden_dataset.json"

    export_json(dataset, output_file)

    assert output_file.exists()

    with output_file.open("r", encoding="utf-8") as file:
        exported = json.load(file)

    assert exported == dataset
