
````
# GoldenForge — System Architecture

**Status:** Draft v0.1  
**Project:** GoldenForge  
**Document:** System Architecture

---

## 1. Architecture Goal

GoldenForge is designed as a local-first, framework-agnostic system that transforms production AI traces into curated Golden Datasets.

The architecture separates the core processing engine from the user interface and future SaaS layer.

The core pipeline is:

Production Data
    ↓
Ingestion
    ↓
Normalization
    ↓
Deduplication
    ↓
Clustering
    ↓
Signal Analysis
    ↓
Candidate Ranking
    ↓
Curation
    ↓
Golden Dataset
    ↓
Export

---

## 2. Core Architectural Principles

### 2.1 Local-first

The OSS version must work locally without requiring a cloud account.

### 2.2 Framework-agnostic

GoldenForge must not depend on LangChain, Langfuse, LangSmith, Promptfoo, or another specific framework.

### 2.3 Composable

GoldenForge should integrate with existing evaluation and observability tools rather than replace them.

### 2.4 Explainable

Candidate selection must provide understandable reasons.

Example:

```text
Candidate #1842

Priority: HIGH

Signals:
- Rare behavior
- Negative user feedback
- High semantic novelty
- No similar Golden Case

Reason:
This interaction represents an important behavior
that is currently underrepresented in the dataset.

````

### 2.5 Core engine independent from UI

The processing engine must be usable through:

- CLI
- Python API
- Future Web UI
- Future SaaS API

---

# 3. High-Level Architecture

```
                 ┌─────────────────────┐
                 │   Production Data   │
                 └──────────┬──────────┘
                            │
                            ▼
                 ┌─────────────────────┐
                 │      Ingestion      │
                 └──────────┬──────────┘
                            │
                            ▼
                 ┌─────────────────────┐
                 │    Normalization    │
                 └──────────┬──────────┘
                            │
                            ▼
                 ┌─────────────────────┐
                 │    Deduplication    │
                 └──────────┬──────────┘
                            │
                            ▼
                 ┌─────────────────────┐
                 │      Clustering     │
                 └──────────┬──────────┘
                            │
                            ▼
                 ┌─────────────────────┐
                 │   Signal Analysis   │
                 └──────────┬──────────┘
                            │
                            ▼
                 ┌─────────────────────┐
                 │ Candidate Ranking   │
                 └──────────┬──────────┘
                            │
                            ▼
                 ┌─────────────────────┐
                 │   Human Curation    │
                 └──────────┬──────────┘
                            │
                            ▼
                 ┌─────────────────────┐
                 │  Golden Dataset     │
                 └──────────┬──────────┘
                            │
                            ▼
                 ┌─────────────────────┐
                 │      Exporters      │
                 └─────────────────────┘

```

---

# 4. Main Components

GoldenForge consists of the following core components:

```
goldenforge/
│
├── ingest/
├── normalize/
├── dedupe/
├── cluster/
├── discover/
├── curate/
├── dataset/
├── export/
└── core/

```

Each component has a single primary responsibility.

---

# 5. Ingestion Layer

The ingestion layer converts external production data into an internal processing format.

## MVP Inputs

GoldenForge initially supports:

- JSON
- JSONL
- CSV

Example:

```
{
  "input": "How do I cancel my subscription?",
  "output": "You can cancel your subscription...",
  "feedback": "negative"
}

```

## Future Inputs

The architecture should allow adapters for:

- Langfuse
- LangSmith
- OpenTelemetry
- Application databases
- Webhooks
- Custom APIs

The ingestion layer must not contain discovery or ranking logic.

---

# 6. Internal Trace Model

All incoming data is converted into a normalized internal representation.

Conceptual model:

```
Trace
├── id
├── timestamp
├── input
├── output
├── metadata
├── model
├── feedback
├── tools
├── context
└── evaluation

```

The internal representation must remain independent from external providers.

Example:

```
Trace(
    id="trace_001",
    input="How do I cancel my subscription?",
    output="You can cancel...",
    feedback="negative",
    model="example-model",
    timestamp="..."
)

```

The exact implementation may evolve.

---

# 7. Normalization Layer

The normalization layer converts different input schemas into the internal Trace representation.

Responsibilities:

- Field mapping
- Missing field handling
- Type normalization
- Metadata normalization
- Timestamp normalization
- Basic validation

Example:

```
Provider Format A ──┐
Provider Format B ──┤
JSONL ──────────────┤
CSV ────────────────┤
                    ▼
              Normalization
                    │
                    ▼
              GoldenForge Trace

```

---

# 8. Deduplication Layer

The purpose of deduplication is to prevent redundant production interactions from consuming analysis and human review capacity.

GoldenForge should support multiple levels of duplication detection.

## Level 1 — Exact duplicates

Identical inputs or identical normalized traces.

## Level 2 — Near duplicates

Small textual variations representing essentially the same interaction.

## Level 3 — Semantic duplicates

Different wording representing the same underlying behavior.

Example:

```
"How can I cancel my subscription?"

"I want to terminate my subscription."

"Where do I cancel my plan?"

```

These may represent the same behavioral cluster.

The deduplication layer should preserve representative examples rather than simply deleting information.

---

# 9. Clustering Layer

The clustering system groups semantically related interactions.

Example:

```
Production Dataset

2,000,000 traces
        ↓
        ↓
     Clustering
        ↓

Cluster A: Subscription cancellation
Cluster B: Refund requests
Cluster C: Password problems
Cluster D: Account deletion
Cluster E: Unusual billing disputes
...

```

Clustering enables GoldenForge to understand the behavioral distribution of the production dataset.

The system should preserve cluster metadata such as:

- Cluster ID
- Size
- Representative examples
- Similarity statistics
- Frequency
- Candidate count

---

# 10. Signal Analysis

GoldenForge evaluates each trace and cluster using multiple signals.

Initial signals:

### Frequency

How often does this behavior occur?

### Rarity

How uncommon is this behavior?

### Novelty

How different is it from existing Golden Dataset cases?

### Similarity

How similar is it to already selected cases?

### Failure

Does the interaction have evidence of failure?

Examples:

- Negative feedback
- Error
- Retry
- Escalation
- Failed evaluation
- Human correction

### Importance

Does the interaction represent an important business or technical scenario?

### Diversity

Does selecting this case improve behavioral coverage?

---

# 11. Candidate Ranking

GoldenForge combines signals into a candidate priority score.

Conceptually:

```
Candidate Score

= Failure Signal
+ Rarity Signal
+ Novelty Signal
+ Importance Signal
+ Diversity Signal
- Redundancy Penalty

```

The exact scoring algorithm must remain configurable and evolve through experimentation.

The system must also expose the individual signals instead of returning only a single score.

Example:

```
Candidate #42

Score: 0.87

Failure:      0.95
Rarity:       0.82
Novelty:      0.91
Importance:   0.88
Diversity:    0.79
Redundancy:   0.08

```

---

# 12. Curation Layer

GoldenForge should separate automated discovery from human approval.

The system generates:

```
Candidate Cases

```

rather than automatically modifying the Golden Dataset.

Possible actions:

```
Accept
Reject
Edit
Merge
Ignore

```

This prevents the Golden Dataset from becoming polluted by low-quality or irrelevant cases.

Human judgment remains an important part of the lifecycle.

---

# 13. Golden Dataset

The Golden Dataset is the curated output of GoldenForge.

Each Golden Case should contain enough information to reproduce an evaluation scenario.

Conceptual structure:

```
Golden Case
├── id
├── input
├── expected_output
├── metadata
├── source_trace
├── reason
├── tags
├── created_at
└── version

```

The system should preserve lineage between:

```
Production Trace
        ↓
Candidate
        ↓
Golden Case
        ↓
Dataset Version

```

---

# 14. Dataset Versioning

Golden Datasets should be versioned.

Example:

```
golden-dataset
│
├── v0.1
├── v0.2
├── v0.3
└── v1.0

```

A version should be reproducible.

Future versions should support:

- Added cases
- Removed cases
- Modified cases
- Source lineage
- Change descriptions
- Dataset comparison

---

# 15. Export Layer

GoldenForge should export datasets in standard formats.

MVP:

```
JSON
JSONL

```

Future:

```
Promptfoo
DeepEval
Langfuse
LangSmith
pytest
Custom evaluation formats

```

GoldenForge should remain an upstream data layer.

It prepares high-quality evaluation data for other tools.

---

# 16. CLI Architecture

The CLI is the primary MVP interface.

Example:

```
goldenforge import conversations.jsonl

```

Then:

```
goldenforge analyze

```

Then:

```
goldenforge review

```

Finally:

```
goldenforge export golden-dataset.jsonl

```

The CLI should also support configuration files.

Example:

```
goldenforge.yaml

```

---

# 17. Storage Architecture

## MVP

Local SQLite storage.

Reasons:

- Zero infrastructure
- Easy installation
- Local-first
- Suitable for MVP datasets
- Easy backup
- Simple testing

Conceptually:

```
GoldenForge CLI
      ↓
SQLite
      ↓
Traces
Clusters
Candidates
Golden Cases
Dataset Versions

```

## Future SaaS

The storage layer can evolve to:

```
PostgreSQL
+
Object Storage

```

without changing the core processing model.

---

# 18. Web UI

The Web UI is not required for the first CLI prototype.

When introduced, it should provide:

- Dataset overview
- Candidate queue
- Candidate explanations
- Cluster visualization
- Golden Dataset management
- Dataset versions
- Search
- Filtering
- Review workflow

The UI should consume the same core engine/API rather than implement its own business logic.

---

# 19. API Boundary

The architecture should eventually expose a programmatic API.

Conceptually:

```
CLI ───────────┐
               │
Web UI ────────┤
               ▼
         Core Engine
               ▲
               │
Python API ────┘

```

This prevents the CLI from becoming the only way to use GoldenForge.

---

# 20. Future SaaS Architecture

The future hosted version may evolve into:

```
                    ┌─────────────────┐
                    │   Web Dashboard │
                    └────────┬────────┘
                             │
                    ┌────────▼────────┐
                    │    API Layer    │
                    └────────┬────────┘
                             │
          ┌──────────────────┼──────────────────┐
          │                  │                  │
          ▼                  ▼                  ▼
     Ingestion          Dataset Service    Review Service
          │                  │                  │
          └──────────────────┼──────────────────┘
                             ▼
                    GoldenForge Engine
                             │
              ┌──────────────┼──────────────┐
              ▼              ▼              ▼
         PostgreSQL     Object Storage   Job Queue

```

The SaaS layer should add:

- Authentication
- Organizations
- RBAC
- Team workflows
- Hosted ingestion
- Dataset registry
- Continuous synchronization
- CI/CD integrations
- Analytics

---

# 21. Privacy Architecture

Production AI traces may contain sensitive information.

The default OSS architecture should therefore favor local processing.

Important requirements:

- No telemetry by default
- Local processing
- Optional persistence
- Configurable redaction
- Secret detection
- PII-aware processing
- Explicit user consent for external services

The system must clearly document what data leaves the machine.

---

# 22. Provider Independence

GoldenForge must not assume a specific model provider.

The architecture should support:

```
Anthropic
OpenAI
Google
Open-source models
Other providers

```

The provider should be metadata, not a core architectural dependency.

---

# 23. Extension Architecture

GoldenForge should be designed around adapters.

Possible extension points:

```
Input Adapters
├── JSON
├── JSONL
├── CSV
├── Langfuse
├── LangSmith
└── OpenTelemetry

Export Adapters
├── JSON
├── JSONL
├── Promptfoo
├── DeepEval
├── Langfuse
└── LangSmith

```

This allows contributors to add integrations without modifying the core engine.

---

# 24. MVP Architecture Boundary

The first MVP must NOT implement the entire future architecture.

MVP:

```
JSON / JSONL / CSV
        ↓
Normalization
        ↓
Exact Deduplication
        ↓
Semantic Similarity
        ↓
Basic Clustering
        ↓
Signal Analysis
        ↓
Candidate Ranking
        ↓
Local Review
        ↓
Golden Dataset Export

```

Everything else is future scope.

---

# 25. Recommended MVP Stack

Core:

```
Python

```

CLI:

```
Typer

```

Data validation:

```
Pydantic

```

Storage:

```
SQLite

```

Data processing:

```
Python ecosystem

```

Embeddings / semantic similarity:

```
Pluggable embedding provider

```

Testing:

```
pytest

```

Future Web UI:

```
TypeScript
Next.js

```

The core engine must not depend on Next.js.

---

# 26. Repository Architecture

Target structure:

```
goldenforge/
│
├── docs/
│   ├── PRD.md
│   └── ARCHITECTURE.md
│
├── src/
│   └── goldenforge/
│       ├── core/
│       ├── ingest/
│       ├── normalize/
│       ├── dedupe/
│       ├── cluster/
│       ├── discover/
│       ├── curate/
│       ├── dataset/
│       └── export/
│
├── tests/
│
├── examples/
│
├── README.md
├── LICENSE
├── pyproject.toml
└── .gitignore

```

---

# 27. Architectural Success Criteria

The architecture is successful if:

1. A developer can run GoldenForge locally.
2. Production traces can be imported without a specific framework.
3. Different input formats can be normalized into one schema.
4. Redundant interactions can be detected.
5. Similar behaviors can be clustered.
6. Important and rare cases can be identified.
7. Candidate selection is explainable.
8. Humans can curate candidates.
9. Golden Datasets can be exported.
10. The core engine can later support a hosted SaaS without being rewritten.

---

# 28. Long-Term Architectural Goal

GoldenForge should eventually become an independent layer between production AI systems and evaluation systems.

```
                AI Applications
                       │
                       ▼
               Production Traces
                       │
                       ▼
                ┌─────────────┐
                │ GoldenForge │
                └──────┬──────┘
                       │
          ┌────────────┼────────────┐
          ▼            ▼            ▼
      Datasets      Regression   Coverage
                       │
                       ▼
                 Eval Systems
                       │
                       ▼
                     CI/CD
                       │
                       ▼
                 Production
                       │
                       └───────────↺

```

The strategic objective is not to become another evaluation framework.

The objective is to become the infrastructure layer responsible for answering:

> **Which real production behaviors should become tests?**
