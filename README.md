# GoldenForge

> Transform production AI traces into curated Golden Datasets for evaluation.

GoldenForge is an open-source Python toolkit for transforming production AI traces into curated Golden Dataset examples.

GoldenForge v0.1 provides a deterministic, local-first data-preparation pipeline for turning JSONL production traces into evaluation-ready Golden Dataset data.

The current release is intentionally small and framework-agnostic. It does not require an LLM, external AI API, cloud account, or persistent database for its core pipeline.

## How it works

```text
JSONL Production Traces
        |
        v
     Validate
        |
        v
    Normalize
        |
        v
Exact Deduplication
        |
        v
Lexical/Jaccard Clustering
        |
        v
Candidate Discovery
        |
        v
 Candidate Scoring
        |
        v
Deterministic Curation
        |
        v
 Golden Dataset
        |
        v
    JSON Export
```

The current v0.1 pipeline is deterministic and local-first.

Human review workflows, semantic similarity, near-duplicate detection, dataset versioning, external integrations, and SaaS capabilities are future scope.

## Current Features

GoldenForge v0.1 includes:

- JSONL trace ingestion
- Trace validation and normalization
- Exact trace deduplication
- Deterministic lexical/Jaccard clustering
- Deterministic candidate discovery
- Explainable discovery signals:
  - Failure
  - Rarity
  - Novelty
  - Diversity
  - Evaluation
  - Context
  - Tools
  - Metadata
- Deterministic candidate scoring
- Deterministic candidate curation
- Configurable `max_items` curation limit
- Golden Dataset construction
- JSON export
- Python pipeline APIs
- Command-line interface
- Automated test suite

## Installation

GoldenForge v0.1 runs locally with Python.

### From source

```bash
git clone https://github.com/AydoxHQ/goldenforge.git
cd goldenforge

python -m venv .venv
```

On Windows:

.venv\Scripts\activate

On macOS or Linux:

source .venv/bin/activate

Install GoldenForge in editable mode:

python -m pip install -e .

No cloud account, external AI API, or persistent database is required for the v0.1 core pipeline.

---

## Quick Start

GoldenForge v0.1 accepts JSONL production traces and builds a curated Golden Dataset locally.

Example:

```json
{"id":"trace_001","input":"How do I reset my password?","output":"Go to Settings > Security > Reset Password.","feedback":"positive"}
{"id":"trace_002","input":"How do I reset my password?","output":"I don't know.","feedback":"negative"}
```

Save the traces as `traces.jsonl`, then run:

```bash
goldenforge build traces.jsonl golden_dataset.json
```

The `build` command runs the complete deterministic v0.1 pipeline:

```text
JSONL
→ Validation
→ Normalization
→ Exact Deduplication
→ Lexical/Jaccard Clustering
→ Candidate Discovery and Scoring
→ Deterministic Curation
→ Golden Dataset Construction
→ JSON Export
```

By default, the pipeline produces at most two curated examples.

You can change the curation limit:

```bash
goldenforge build traces.jsonl golden_dataset.json --max-items 10
```

The entire pipeline runs locally and does not require an LLM or external AI API.

---

## CLI

GoldenForge v0.1 provides a small command-line interface.

Check the installed version:

```bash
goldenforge version
```

Verify the installation:

```bash
goldenforge hello
```

Build a Golden Dataset from JSONL:

```bash
goldenforge build input.jsonl output.json
```

Limit the number of curated examples:

```bash
goldenforge build input.jsonl output.json --max-items 10
```

View general help:

```bash
goldenforge --help
```

View build command help:

```bash
goldenforge build --help
```

The v0.1 CLI does not provide separate `import`, `analyze`, `review`, or `export` commands. Human review workflows are future scope.

---

## Python API

GoldenForge v0.1 exposes Python APIs for running the same core pipeline programmatically.

Build from JSONL:

```python
from goldenforge.pipeline.basic import build_pipeline_from_jsonl

dataset = build_pipeline_from_jsonl(
    "traces.jsonl",
    max_items=10,
)
```

Or use the pipeline directly with normalized traces:

```python
from goldenforge.pipeline.basic import build_pipeline

dataset = build_pipeline(
    traces,
    max_items=10,
)
```

Use `max_items=None` when no curation limit is desired.

The Python API and CLI use the same underlying deterministic pipeline.

---

## Pipeline

GoldenForge v0.1 runs the following deterministic local pipeline:

1. **Validate** — Validate incoming JSONL traces.
2. **Normalize** — Convert valid traces into the internal GoldenForge representation.
3. **Exact Deduplication** — Remove exact duplicate traces.
4. **Deterministic Lexical/Jaccard Clustering** — Group traces using the implemented lexical similarity logic.
5. **Candidate Discovery** — Identify candidate traces using deterministic discovery signals.
6. **Candidate Scoring** — Calculate the current deterministic `selection_score`.
7. **Deterministic Curation** — Select candidates according to the current selection logic and optional `max_items` limit.
8. **Golden Dataset Construction** — Convert selected candidates into Golden Dataset examples.
9. **JSON Export** — Write the resulting Golden Dataset to JSON.

The v0.1 pipeline does not require an LLM or external AI API.

Semantic similarity, near-duplicate detection, human review workflows, dataset versioning, regression management, and external integrations are future scope.

## Discovery

GoldenForge v0.1 uses deterministic and explainable discovery signals to identify production traces that may be valuable as Golden Dataset examples.

### Failure

Identifies evidence that an interaction may represent a failure or problematic behavior.

Examples include available failure-related signals such as negative feedback or evaluation evidence.

### Rarity

Measures how uncommon an interaction or behavior is within the processed trace set.

### Novelty

Measures how different an interaction is from other traces using the deterministic similarity logic available in v0.1.

### Diversity

Helps preserve behavioral coverage by favoring candidates that contribute representation from less-represented areas of the dataset.

### Evaluation

Uses available evaluation-related information as a candidate discovery signal.

### Context

Uses available contextual information associated with the trace.

### Tools

Uses available tool-related information associated with the trace.

### Metadata

Uses available metadata as additional candidate discovery information.

### Clustering

GoldenForge v0.1 uses deterministic lexical/Jaccard clustering over trace content to provide grouping and discovery signals.

The discovery system is intentionally deterministic, local-first, and explainable. The resulting signals are used by the current deterministic candidate scoring and curation logic.

## Curation

GoldenForge v0.1 performs deterministic candidate curation as the final selection step before Golden Dataset construction.

The current curation layer:

- uses the deterministic candidate selection logic,
- ranks candidates according to the current `selection_score`,
- applies the optional `max_items` limit,
- preserves candidate signals and metadata in the resulting dataset.

The default pipeline limit is two examples and can be changed through the Python API or CLI.

The v0.1 curation step does not provide human review, interactive accept/reject workflows, editing, merging, or collaborative approval.

Human curation workflows are future scope.

## Architecture

GoldenForge v0.1 is organized into focused Python modules around the deterministic processing pipeline:

```text
src/goldenforge/
├── cluster/
├── curate/
├── dataset/
├── dedupe/
├── discover/
├── ingest/
├── normalize/
├── pipeline/
├── score/
├── select/
├── validate/
├── cli.py
└── models.py
```

Each module has a focused responsibility within the v0.1 pipeline.

The core engine is independent from external model providers, Web UI, and SaaS functionality.

For the full architectural design and future direction, see `docs/ARCHITECTURE.md`.

## Testing

GoldenForge uses `pytest` for automated testing.

Run the complete test suite:

```bash
python -m pytest
```

The test suite covers:

- JSONL ingestion
- Normalization
- Validation
- Deduplication
- Discovery
- Clustering
- Scoring
- Selection
- Diversity
- Curation
- Pipeline execution
- JSON export
- CLI behavior

The current test suite passes successfully.

## Roadmap

### Implemented in v0.1

- [x] JSONL ingestion
- [x] Trace validation
- [x] Trace normalization
- [x] Exact trace deduplication
- [x] Deterministic lexical/Jaccard clustering
- [x] Deterministic candidate discovery
- [x] Explainable discovery signals
- [x] Deterministic candidate scoring
- [x] Deterministic candidate curation
- [x] Configurable `max_items` limit
- [x] Golden Dataset construction
- [x] JSON export
- [x] End-to-end local pipeline
- [x] CLI
- [x] Python API
- [x] Automated tests

### Future

- [ ] Additional input formats
- [ ] Additional export formats
- [ ] Semantic similarity
- [ ] Near-duplicate detection
- [ ] Human review workflows
- [ ] Dataset inspection and management
- [ ] Dataset versioning
- [ ] Regression workflows
- [ ] External provider and observability integrations
- [ ] Web interface
- [ ] Open-Core SaaS capabilities

## Open Source

GoldenForge v0.1 is released under the MIT License.

The OSS project is designed to provide a useful local production-to-evaluation data pipeline without requiring a cloud account or paid service.

Contributions are welcome.

Before submitting a pull request:

1. Create a focused change.
2. Add or update tests.
3. Run the complete test suite.
4. Update documentation when necessary.
5. Keep changes aligned with the project's architecture and scope.
6. Submit a pull request describing the change.

## Project Status

GoldenForge v0.1 is an early-stage open-source release.

The current release provides a deterministic, local-first pipeline for transforming production AI traces from JSONL into curated Golden Datasets.

The v0.1 core pipeline is implemented, tested, and usable through the CLI and Python API.

Future development will extend GoldenForge toward a broader production-to-evaluation data layer while keeping the core engine local-first and framework-agnostic.