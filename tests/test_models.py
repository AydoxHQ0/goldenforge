from goldenforge.models import Candidate, Trace


def test_candidate_defaults():
    trace = Trace(
        id="trace_001",
        input="Question",
        output="Answer",
    )

    candidate = Candidate(trace=trace)

    assert candidate.trace == trace
    assert candidate.score == 0.0
    assert candidate.signals == {}
    assert candidate.reason == ""


def test_candidate_stores_discovery_information():
    trace = Trace(
        id="trace_002",
        input="Question",
        output="Wrong answer",
        feedback="negative",
    )

    candidate = Candidate(
        trace=trace,
        score=0.87,
        signals={
            "failure": 0.95,
            "rarity": 0.82,
            "novelty": 0.91,
        },
        reason="Negative feedback and high semantic novelty.",
    )

    assert candidate.trace.id == "trace_002"
    assert candidate.score == 0.87
    assert candidate.signals["failure"] == 0.95
    assert candidate.signals["rarity"] == 0.82
    assert candidate.reason == "Negative feedback and high semantic novelty."