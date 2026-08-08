# GoldenForge — Product Requirements Document

**Status:** Draft v0.1  
**Project:** GoldenForge  
**License:** Apache-2.0  
**Document:** Product Requirements Document

---

## 1. Product Summary

GoldenForge is an open-source developer tool that transforms real production AI interactions into high-quality, versioned Golden Datasets and regression test suites.

Instead of requiring developers to manually design evaluation datasets, GoldenForge analyzes real-world AI application traces and helps identify which interactions are valuable enough to become permanent test cases.

The long-term vision is:

Production Traffic
→ Trace Collection
→ Normalization
→ Deduplication
→ Clustering
→ Failure / Edge-Case Detection
→ Candidate Cases
→ Human Curation
→ Golden Dataset
→ Versioning
→ Regression Suite
→ CI/CD

GoldenForge is not another general-purpose LLM evaluation framework.

Its primary responsibility is the lifecycle of turning real application behavior into reliable evaluation data.

---

# 2. Problem

AI applications continuously generate enormous amounts of real-world interaction data.

A production AI application may receive millions of conversations, requests, tool calls, or agent traces.

However, most teams cannot efficiently determine:

- Which interactions are important?
- Which failures should become regression tests?
- Which rare edge cases are being missed?
- Which cases are duplicates?
- Which topics are overrepresented?
- Which important scenarios are absent from the current test set?
- When should a production trace be promoted into the Golden Dataset?
- How should the dataset evolve when new failures appear?

A naive approach is random sampling.

Random sampling is insufficient because it can:

- Overrepresent frequent topics.
- Miss rare but critical cases.
- Produce thousands of near-duplicates.
- Waste human review capacity.
- Fail to provide coverage across the true behavioral distribution of the application.

The core problem is therefore not simply:

> "How do we run evaluations?"

It is:

> **"How do we continuously discover, curate, and maintain the right evaluation cases from real production behavior?"**

---

# 3. Core Insight

The most valuable evaluation dataset is not necessarily the largest dataset.

A useful Golden Dataset should maximize meaningful behavioral coverage.

GoldenForge therefore prioritizes cases based on signals such as:

- Importance
- Rarity
- Failure likelihood
- Novelty
- Diversity
- User feedback
- Business impact
- Semantic coverage
- Regression history

The system should reduce redundant cases while protecting rare and important scenarios.

Conceptually:

```text
2,000,000 production interactions

        ↓

Normalization

        ↓

Deduplication

        ↓

Semantic grouping

        ↓

Frequency analysis
+ rarity detection
+ failure detection
+ novelty detection
+ importance signals

        ↓

Candidate selection

        ↓

Human review

        ↓

Golden Dataset

        ↓

Regression Suite


---

4. Target Users

Primary Users

AI Application Developers

Developers building:

AI SaaS products

AI assistants

RAG applications

Customer-support AI

Agentic applications

AI APIs

Internal AI systems


AI / ML Engineers

Teams responsible for:

Evaluation

Quality

Regression testing

Model selection

Prompt engineering

Production monitoring


Small AI Teams

Teams that cannot afford to build a complete internal evaluation infrastructure.


---

5. Supported Application Types

GoldenForge should eventually support:

Chat applications

RAG applications

AI assistants

Tool-using agents

Multi-step agents

AI APIs

Classification systems

Structured-output applications


The architecture should avoid being tied to a single framework.


---

6. Core Product Concept

GoldenForge has five fundamental responsibilities.

6.1 Ingest

Accept production interaction data from multiple sources.

Initial MVP sources:

JSON

JSONL

CSV


Future sources:

Langfuse

LangSmith

OpenTelemetry

Webhooks

Application databases

Other observability platforms



---

6.2 Normalize

Convert different input formats into a common internal representation.

Example:

Trace
├── input
├── output
├── metadata
├── timestamp
├── model
├── feedback
├── latency
├── tools
└── context

The internal schema must remain framework-agnostic.


---

6.3 Discover

GoldenForge analyzes interactions to identify valuable candidates.

Important signals include:

Frequency

How often does a behavior occur?

Rarity

How unusual is this interaction compared with the rest of the dataset?

Similarity

Is this interaction nearly identical to existing cases?

Novelty

Does it represent a behavior not already covered?

Failure

Was the interaction associated with:

negative feedback

errors

failed evaluations

retries

escalations

human corrections


Importance

Does the interaction represent an important business or technical scenario?


---

6.4 Curate

GoldenForge should not blindly convert every interesting trace into a Golden Dataset.

Instead, it creates a candidate queue.

Example:

Candidate #1842

Reason:
- Rare behavior
- No existing similar case
- Negative user feedback
- High semantic novelty

Recommendation:
HIGH PRIORITY

A developer can then:

Accept

Reject

Edit

Merge

Ignore

Mark as important



---

6.5 Export

GoldenForge should not attempt to replace every existing evaluation framework.

Instead, it should integrate with them.

Initial export targets:

JSON

JSONL


Future integrations:

Promptfoo

DeepEval

Langfuse

LangSmith

pytest

CI systems


GoldenForge should become the layer that prepares high-quality evaluation data for the rest of the ecosystem.


---

7. Golden Dataset Lifecycle

The central product loop is:

Production
   ↓
Ingestion
   ↓
Normalization
   ↓
Deduplication
   ↓
Clustering
   ↓
Candidate Detection
   ↓
Prioritization
   ↓
Human Curation
   ↓
Golden Dataset
   ↓
Version
   ↓
Regression Tests
   ↓
CI
   ↓
New Production Failures
   ↓
Back to GoldenForge

This lifecycle is the heart of the project.


---

8. MVP

The MVP must remain small enough for one developer to build within approximately 8–12 weeks.

MVP Goal

Given a production dataset containing AI interactions, GoldenForge should be able to identify valuable, diverse, non-redundant candidate cases and export them as a Golden Dataset.


---

MVP Input

Support:

JSON
JSONL
CSV

Example:

{
  "input": "How do I cancel my subscription?",
  "output": "You can cancel...",
  "feedback": "negative"
}


---

9. MVP Processing Pipeline

The first implementation should provide:

Step 1 — Import

Load production interactions.

Step 2 — Normalize

Convert them to the GoldenForge internal schema.

Step 3 — Deduplicate

Remove exact and near-duplicate interactions.

Step 4 — Cluster

Group semantically similar interactions.

Step 5 — Analyze

Calculate signals such as:

frequency

rarity

similarity

novelty

feedback

potential importance


Step 6 — Rank

Produce a prioritized candidate list.

Step 7 — Curate

Allow the user to accept or reject candidates.

Step 8 — Export

Generate a Golden Dataset.


---

10. MVP User Experience

The simplest useful workflow should be:

goldenforge import conversations.jsonl

Then:

goldenforge analyze

Then:

goldenforge review

Finally:

goldenforge export golden-dataset.jsonl

The goal is to make the first successful result possible within minutes.


---

11. What GoldenForge Must NOT Become

GoldenForge should NOT initially attempt to become:

A general LLM framework

A chatbot

A general observability platform

A replacement for Langfuse

A replacement for LangSmith

A replacement for Promptfoo

A complete evaluation framework

A model provider

A general-purpose RAG framework

A generic analytics platform


Its core identity must remain:

> Production traces → high-quality Golden Datasets




---

12. Open-Source Strategy

The core lifecycle should remain open source.

The OSS project should provide developers with a genuinely useful local tool without requiring a cloud account.

Initial open-source capabilities:

CLI

Data ingestion

Normalization

Deduplication

Clustering

Candidate ranking

Basic review workflow

Golden Dataset export

Configuration

Provider-independent schema


The project should be useful even if the user never pays for anything.


---

13. Future Open-Core SaaS

The commercial product should not simply put a paywall around the OSS CLI.

The SaaS should solve collaboration, scale, governance, and continuous operation.

Potential paid capabilities:

Hosted Dataset Registry

Central datasets

Dataset versions

Dataset lineage

Dataset history


Team Curation

Assign cases to reviewers

Comments

Approvals

Review workflows


Continuous Production Sync

Automatically ingest new production traces.

Automatic Dataset Evolution

Detect new failure patterns and propose additions.

Regression Management

Track:

Test results

Dataset versions

Model versions

Prompt versions

Application versions


CI/CD

Automatically run regression suites on:

Pull requests

Deployments

Model changes

Prompt changes


Analytics

Show:

Dataset coverage

Failure clusters

Newly discovered edge cases

Regression trends

Most important cases



---

14. Long-Term Product Vision

GoldenForge should evolve from:

> A dataset generation CLI



into:

> The continuous data layer for AI evaluation.



Long-term architecture:

GoldenForge

Production ───────┐
                   │
Langfuse ──────────┤
                   │
LangSmith ─────────┤
                   │
OpenTelemetry ─────┤
                   ↓
             Ingestion Layer
                   ↓
             Normalization
                   ↓
        Discovery & Intelligence
                   ↓
             Curation Layer
                   ↓
          Golden Dataset Registry
                   ↓
           Evaluation / CI Layer
                   ↓
       Production Feedback Loop


---

15. Long-Term Moat

Potential defensibility comes from:

15.1 Dataset Intelligence

Learning which production interactions are most valuable as tests.

15.2 Behavioral Coverage

Understanding which parts of an application's behavior are covered or missing.

15.3 Dataset Lineage

Connecting:

Production Trace
→ Candidate
→ Golden Case
→ Dataset Version
→ Evaluation
→ Regression
→ Production Outcome

15.4 Ecosystem Integrations

Deep integrations with:

Observability platforms

Evaluation frameworks

CI/CD

GitHub

AI application frameworks


15.5 Community Standards

The long-term goal is for GoldenForge's normalized trace and dataset formats to become useful beyond GoldenForge itself.


---

16. Success Metrics

The project should measure both OSS adoption and product value.

Open Source

Initial milestones:

100 GitHub stars

500 GitHub stars

1,000 GitHub stars

5,000 GitHub stars

10,000 GitHub stars


Other metrics:

Contributors

Forks

Downloads

Dependent projects

Issues

Pull requests

Community integrations


Product Metrics

Important SaaS metrics:

Active projects

Traces processed

Golden cases created

Dataset versions created

Regression tests executed

CI integrations

Paying teams

Retention



---

17. Design Principles

Principle 1 — Real production data first

GoldenForge should prioritize real user behavior over purely synthetic benchmarks.

Principle 2 — Reduce human effort

Humans should curate important cases, not manually discover millions of them.

Principle 3 — Framework agnostic

GoldenForge should integrate with the ecosystem instead of competing with every tool.

Principle 4 — Local-first OSS

Developers should be able to run the core locally.

Principle 5 — Composable

GoldenForge should work alongside existing tools.

Principle 6 — Evidence over assumptions

Candidate selection should be explainable.

For every candidate, the system should ideally explain:

> "Why was this selected?"




---

18. Security & Privacy

Production AI traces can contain sensitive information.

The architecture must therefore prioritize:

Local processing

Explicit persistence

Configurable redaction

Secret removal

PII-aware processing

No telemetry by default

Clear documentation about data handling


The SaaS version should eventually provide:

Encryption

Access controls

RBAC

Audit logs

Data retention policies



---

19. Technical Direction

Initial architecture:

CLI
 ↓
Core Processing Engine
 ↓
Internal Trace Schema
 ↓
Deduplication
 ↓
Clustering
 ↓
Candidate Ranking
 ↓
Dataset Builder
 ↓
Exporters

Potential implementation:

Core

Python

CLI

Python CLI framework

Web UI

TypeScript + Next.js

Storage

SQLite for local MVP

Future SaaS

PostgreSQL + object storage

The architecture should keep the core engine independent from the web application.


---

20. Initial Repository Structure

Expected structure:

goldenforge/
│
├── docs/
│   └── PRD.md
│
├── src/
│   └── goldenforge/
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

This structure is directional and may evolve during implementation.


---

21. Initial Roadmap

Phase 1 — Foundation

Internal trace schema

JSON/JSONL ingestion

CLI

Basic normalization


Phase 2 — Discovery

Exact deduplication

Semantic similarity

Clustering

Rarity detection

Candidate ranking


Phase 3 — Curation

Candidate review

Accept/reject

Golden Dataset generation


Phase 4 — Export

JSON/JSONL

Promptfoo-compatible export

Additional integrations


Phase 5 — Regression

Dataset versioning

Baselines

CI integration



---

22. Strategic Positioning

GoldenForge should be positioned as:

> The open-source production-to-evals pipeline.



Or more specifically:

> Turn real AI production traffic into living Golden Datasets.



The project should avoid positioning itself as another:

> "AI evaluation platform."



The distinction is critical.


---

23. Initial Definition of Done

The MVP is successful when a developer can:

1. Take a large production interaction file.


2. Import it into GoldenForge.


3. Automatically remove redundant cases.


4. Discover meaningful behavioral clusters.


5. Identify rare, novel, or failed interactions.


6. Receive a ranked candidate list.


7. Review candidates.


8. Approve a subset.


9. Export a Golden Dataset.


10. Use that dataset as a regression suite.



If this workflow works reliably and is dramatically easier than manually building the same pipeline, GoldenForge has achieved its core MVP objective.


---

24. Strategic Objective

GoldenForge has two long-term objectives:

Objective 1 — Open Source Impact

Become a widely adopted piece of infrastructure for building evaluation datasets from real AI application behavior.

Objective 2 — Sustainable Business

Build an Open-Core SaaS around:

continuous ingestion

dataset governance

collaborative curation

dataset versioning

regression management

CI/CD

analytics

enterprise controls


The commercial product must grow naturally from the operational problems created by successful OSS adoption.


---

25. Final Product Definition

GoldenForge is:

> An open-source system for discovering, curating, versioning, and continuously evolving Golden Datasets from real-world AI application traces.



Its fundamental loop is:

REAL PRODUCTION BEHAVIOR
        ↓
DISCOVER IMPORTANT CASES
        ↓
CURATE
        ↓
GOLDEN DATASET
        ↓
REGRESSION TESTS
        ↓
CI/CD
        ↓
NEW PRODUCTION BEHAVIOR
        ↺

That loop is the product.

### بعد اللصق

اضغط **Commit changes...**

واجعل رسالة الـ commit:

```text
docs: add initial product requirements

