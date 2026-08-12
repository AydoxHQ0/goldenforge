# GoldenForge

> Transform production AI traces into high-quality Golden Datasets for evaluation.

GoldenForge is an open-source Python toolkit for turning production AI application traces into curated Golden Datasets.

It provides a deterministic data preparation pipeline:

**Ingest → Normalize → Validate → Select → Deduplicate → Build → Export**

The goal is simple: help AI developers turn real-world application traces into useful evaluation data.

---

## Why GoldenForge?

AI evaluation workflows are only as useful as the data used to evaluate them.

Production AI applications generate large amounts of traces, but those traces are often:

- inconsistent
- noisy
- duplicated
- incomplete
- difficult to reuse for evaluation

GoldenForge provides the data preparation layer between production traces and downstream evaluation workflows.

```text
Production AI Traces
        │
        ▼
     Ingest
        │
        ▼
    Normalize
        │
        ▼
     Validate
        │
        ▼
      Select
        │
        ▼
    Deduplicate
        │
        ▼
 Build Golden Dataset
        │
        ▼
       Export
```

## Features

- JSONL trace ingestion
- Trace normalization
- Trace validation
- Quality-based trace selection
- Selection scoring
- Trace deduplication
- Golden Dataset construction
- JSON export
- Python API
- Command-line interface
- Automated tests for core functionality

## Installation

Clone the repository:

```bash
git clone https://github.com/AydoxHQ0/goldenforge.git
cd goldenforge
```

Create a virtual environment:

```bash
python -m venv .venv
```

Activate it on Windows:

```powershell
.venv\Scripts\activate
```

Install GoldenForge:

```bash
pip install -e .
```

## Quick Start

GoldenForge accepts JSONL traces.

Example input:

```json
{"id":"trace_001","input":"How do I reset my password?","output":"Go to Settings > Security > Reset Password.","feedback":"positive"}
{"id":"trace_002","input":"How do I reset my password?","output":"I don't know.","feedback":"negative"}
```

Run the pipeline:

```bash
goldenforge build traces.jsonl golden_dataset.json
```

GoldenForge processes the traces through the pipeline and exports the resulting Golden Dataset.

## CLI

Check the installed version:

```bash
goldenforge version
```

Verify the installation:

```bash
goldenforge hello
```

Build a Golden Dataset:

```bash
goldenforge build input.jsonl output.json
```

The `build` command runs the production trace pipeline and writes the resulting Golden Dataset to the specified output path.

## Python API

The core pipeline can also be used directly from Python:

```python
from goldenforge.pipeline.basic import build_pipeline_from_jsonl

dataset = build_pipeline_from_jsonl("traces.jsonl")

print(dataset)
```

## Architecture

GoldenForge is organized into small, focused, composable modules:

```text
src/goldenforge/
├── dataset/
│   ├── export.py
│   └── golden.py
├── dedupe/
│   └── basic.py
├── ingest/
│   └── jsonl.py
├── normalize/
│   └── basic.py
├── pipeline/
│   └── basic.py
├── score/
│   └── basic.py
├── select/
│   ├── basic.py
│   └── scoring.py
├── validate/
│   └── basic.py
├── cli.py
└── models.py
```

Each stage has a focused responsibility, making the pipeline easier to test, extend, and integrate into larger AI evaluation workflows.

## Pipeline

The current pipeline performs the following operations:

1. **Ingest** — Load production traces from JSONL.
2. **Normalize** — Convert traces into a consistent representation.
3. **Validate** — Remove invalid or incomplete traces.
4. **Select** — Identify useful traces for the Golden Dataset.
5. **Deduplicate** — Remove duplicate traces.
6. **Build** — Construct the Golden Dataset.
7. **Export** — Write the resulting dataset to JSON.

## Testing

GoldenForge uses `pytest`.

Run the complete test suite:

```bash
python -m pytest
```

The current test suite covers:

- JSONL ingestion
- normalization
- validation
- scoring
- selection
- selection scoring
- deduplication
- pipeline execution
- Golden Dataset construction
- JSON export
- CLI behavior

Current test status:

```text
37 tests passed
```

## Roadmap

### Current

- [x] JSONL ingestion
- [x] Trace normalization
- [x] Trace validation
- [x] Trace scoring
- [x] Trace selection
- [x] Selection scoring
- [x] Trace deduplication
- [x] Golden Dataset construction
- [x] JSON export
- [x] End-to-end pipeline
- [x] CLI
- [x] Automated tests

### Planned

- [ ] Additional trace formats
- [ ] Langfuse integration
- [ ] LangSmith integration
- [ ] Promptfoo integration
- [ ] Additional export formats
- [ ] More advanced quality scoring
- [ ] Configurable selection strategies
- [ ] Web interface
- [ ] Dataset inspection and review workflows

The roadmap is intentionally focused on improving GoldenForge as a practical data preparation layer for AI evaluation workflows.

## Contributing

Contributions are welcome.

Before submitting a pull request:

1. Create a focused change.
2. Add or update tests.
3. Run the test suite.
4. Update documentation when necessary.
5. Submit a pull request describing the change.

Run the tests with:

```bash
python -m pytest
```

## License

GoldenForge is released under the MIT License.

See [LICENSE](LICENSE) for details.

## Status

GoldenForge is an early-stage open-source project.

The current implementation provides a deterministic pipeline for transforming production AI traces into curated Golden Datasets.

The project is being developed toward becoming a practical data preparation layer for production AI evaluation workflows.
