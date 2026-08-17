```markdown
# GoldenForge

> Transform production AI traces into high-quality Golden Datasets for evaluation.

GoldenForge is an open-source Python toolkit for turning production AI application traces into curated datasets that can be reused for AI evaluation workflows.

Production AI applications generate large amounts of interaction data, but raw traces are often noisy, inconsistent, duplicated, incomplete, or difficult to reuse directly for evaluation.

GoldenForge provides a deterministic data-preparation layer between production traces and downstream evaluation systems.

## How it works

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

The current pipeline is deterministic and does not require an LLM or external AI API.

## Why GoldenForge?

AI evaluation is only as useful as the data used to evaluate an application.

A production AI application may generate thousands or millions of traces, but only a subset may be useful as evaluation examples.

GoldenForge helps developers turn those raw traces into a smaller, cleaner, reusable Golden Dataset.

Typical workflow:

```text
Production logs
      ↓
Raw traces
      ↓
GoldenForge
      ↓
Curated Golden Dataset
      ↓
AI evaluation
```

## Current Features

- JSONL trace ingestion
- Trace normalization
- Trace validation
- Quality-based trace scoring
- Trace selection
- Selection scoring
- Trace deduplication
- Golden Dataset construction
- JSON export
- Command-line interface
- Python API
- End-to-end pipeline
- Automated test suite

## Installation

### From TestPyPI

GoldenForge v0.1.0 is currently available through TestPyPI for testing.

```bash
python -m pip install --index-url https://test.pypi.org/simple/ goldenforge
```

### From source

Clone the repository:

```bash
git clone https://github.com/AydoxHQ/goldenforge.git
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

Install the project:

```bash
python -m pip install -e .
```

## Quick Start

GoldenForge accepts JSONL traces.

Example input:

```json
{"id":"trace_001","input":"How do I reset my password?","output":"Go to Settings > Security > Reset Password.","feedback":"positive"}
{"id":"trace_002","input":"How do I reset my password?","output":"I don't know.","feedback":"negative"}
```

Save the traces as:

```text
traces.jsonl
```

Run the pipeline:

```bash
goldenforge build traces.jsonl golden_dataset.json
```

GoldenForge processes the traces through the pipeline and writes the resulting Golden Dataset to the specified output file.

## Output

The resulting dataset contains curated examples suitable for downstream evaluation workflows.

Example:

```json
[
  {
    "id": "trace_002",
    "input": "How do I reset my password?",
    "output": "I don't know.",
    "metadata": {}
  }
]
```

The exact contents depend on the input traces and the current selection and deduplication rules.

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

Get command help:

```bash
goldenforge --help
```

## Python API

GoldenForge can also be used directly from Python:

```python
from goldenforge.pipeline.basic import build_pipeline_from_jsonl

dataset = build_pipeline_from_jsonl("traces.jsonl")

print(dataset)
```

This makes GoldenForge usable both as a command-line tool and as a component inside larger AI evaluation workflows.

## Architecture

GoldenForge is organized into small, focused modules:

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

Each stage has a focused responsibility, making the pipeline easier to test, extend, and integrate into larger AI evaluation systems.

## Pipeline

The current pipeline performs:

1. **Ingest** — Load production traces from JSONL.
2. **Normalize** — Convert traces into a consistent representation.
3. **Validate** — Remove invalid or incomplete traces.
4. **Select** — Identify traces that are useful for the Golden Dataset.
5. **Deduplicate** — Remove duplicate traces.
6. **Build** — Construct Golden Dataset examples.
7. **Export** — Write the resulting dataset to JSON.

## Testing

GoldenForge uses `pytest`.

Run the complete test suite:

```bash
python -m pytest
```

Current status:

```text
37 tests passed
```

The test suite covers:

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
- [x] v0.1.0 release
- [x] TestPyPI publishing
- [x] Clean-environment installation testing

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

The roadmap is intentionally focused on making GoldenForge a practical data-preparation layer for production AI evaluation workflows.

## Open Source

GoldenForge is an open-source project released under the MIT License.

Contributions are welcome.

Before submitting a pull request:

1. Create a focused change.
2. Add or update tests.
3. Run the test suite.
4. Update documentation when necessary.
5. Submit a pull request describing the change.

## Project Status

GoldenForge is currently an early-stage open-source project.

The current implementation provides a deterministic pipeline for transforming production AI traces into curated Golden Datasets.

The project is being developed toward becoming a practical data-preparation layer for production AI evaluation workflows.
```