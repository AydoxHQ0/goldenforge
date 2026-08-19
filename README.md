```markdown
# GoldenForge

> Transform production AI traces into high-quality Golden Datasets for evaluation.

GoldenForge is an open-source Python toolkit for turning production AI application traces into curated datasets that can be reused for AI evaluation workflows.

Production AI applications generate large amounts of interaction data, but raw traces are often noisy, duplicated, incomplete, or difficult to reuse directly for evaluation.

GoldenForge provides a deterministic data-preparation layer between production traces and downstream evaluation systems.

## How it works

```text
Production AI Traces
        |
        v
      Ingest
        |
        v
     Normalize
        |
        v
     Validate
        |
        v
   Deduplicate
        |
        v
    Discovery
        |
        +--> Failure
        +--> Rarity
        +--> Novelty
        +--> Clustering
        +--> Diversity
        |
        v
     Curation
        |
        v
 Build Golden Dataset
        |
        v
      Export
```

The current pipeline is deterministic and does not require an LLM or external AI API.

## Current Features

- JSONL trace ingestion
- Trace normalization and validation
- Trace deduplication
- Production trace discovery
- Failure, rarity, novelty, and diversity signals
- Deterministic lexical clustering
- Candidate curation and ranking
- Configurable curation limits
- Golden Dataset construction
- JSON export
- Python API
- Command-line interface
- Automated test suite

## Installation

### From source

```bash
git clone https://github.com/AydoxHQ/goldenforge.git
cd goldenforge

python -m venv .venv
```

On Windows:

```powershell
.venv\Scripts\activate
```

Install in editable mode:

```bash
python -m pip install -e .
```

## Quick Start

GoldenForge accepts JSONL traces.

Example:

```json
{"id":"trace_001","input":"How do I reset my password?","output":"Go to Settings > Security > Reset Password.","feedback":"positive"}
{"id":"trace_002","input":"How do I reset my password?","output":"I don't know.","feedback":"negative"}
```

Save the traces as `traces.jsonl`, then run:

```bash
goldenforge build traces.jsonl golden_dataset.json
```

By default, the pipeline produces at most two curated examples.

You can change the limit:

```bash
goldenforge build traces.jsonl golden_dataset.json --max-items 10
```

## CLI

Check the version:

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

Limit the number of examples:

```bash
goldenforge build input.jsonl output.json --max-items 10
```

View help:

```bash
goldenforge --help
goldenforge build --help
```

## Python API

Build from JSONL:

```python
from goldenforge.pipeline.basic import build_pipeline_from_jsonl

dataset = build_pipeline_from_jsonl(
    "traces.jsonl",
    max_items=10,
)
```

Or use the pipeline directly:

```python
from goldenforge.pipeline.basic import build_pipeline

dataset = build_pipeline(
    traces,
    max_items=10,
)
```

Use `max_items=None` when no curation limit is desired.

## Pipeline

The current pipeline performs:

1. **Ingest** — Load production traces from JSONL.
2. **Normalize** — Convert traces into a consistent representation.
3. **Validate** — Remove invalid or incomplete traces.
4. **Deduplicate** — Remove duplicate traces.
5. **Discover** — Identify valuable production traces.
6. **Cluster** — Group traces using deterministic lexical similarity.
7. **Score** — Calculate discovery signals such as failure, rarity, novelty, and diversity.
8. **Curate** — Rank candidates and optionally limit the final candidate set.
9. **Build** — Construct Golden Dataset examples.
10. **Export** — Write the resulting dataset to JSON.

## Discovery

GoldenForge currently uses deterministic signals.

### Failure

Negative user feedback is treated as a strong signal that a trace may represent a useful evaluation case.

### Rarity

Rarity measures how frequently the same normalized input appears in the trace set.

### Novelty

Novelty estimates how different an input is from other inputs using deterministic lexical similarity.

### Clustering

Traces can be grouped using Jaccard similarity over input tokens.

### Diversity

Diversity is derived from cluster representation. Traces belonging to smaller clusters receive a higher diversity signal, helping preserve less-represented behaviors.

The discovery system is intentionally deterministic and transparent.

## Curation

Curation converts discovered candidates into a bounded Golden Case set.

The current curation layer:

- filters candidates by minimum score,
- ranks candidates by score,
- optionally limits the number of candidates,
- preserves candidate metadata, signals, and explanations.

The default pipeline limit is two examples and can be changed through the Python API or CLI.

## Architecture

The project is organized into focused modules:

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

Each stage has a focused responsibility, making the system easier to test, extend, and integrate.

## Testing

GoldenForge uses `pytest`.

Run the complete test suite:

```bash
python -m pytest
```

Current development status:

```text
62 tests passed
```

The tests cover ingestion, normalization, validation, scoring, selection, deduplication, discovery, clustering, diversity, curation, pipeline execution, export, and CLI behavior.

## Roadmap

### Current

- [x] JSONL ingestion
- [x] Trace normalization
- [x] Trace validation
- [x] Trace scoring
- [x] Trace selection
- [x] Trace deduplication
- [x] Production trace discovery
- [x] Deterministic clustering
- [x] Diversity scoring
- [x] Candidate curation
- [x] Configurable curation limit
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
- [ ] Configurable discovery strategies
- [ ] Dataset inspection and review workflows
- [ ] Web interface

## Open Source

GoldenForge is released under the MIT License.

Contributions are welcome.

Before submitting a pull request:

1. Create a focused change.
2. Add or update tests.
3. Run the test suite.
4. Update documentation when necessary.
5. Submit a pull request describing the change.

## Project Status

GoldenForge is an early-stage open-source project.

The current implementation provides a deterministic pipeline for transforming production AI traces into curated Golden Datasets.

The project is being developed toward becoming a practical data-preparation layer for production AI evaluation workflows.
```