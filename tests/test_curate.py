from goldenforge.models import Candidate, Trace
from goldenforge.curate.basic import curate_candidates


def test_curate_candidates_returns_candidates_above_minimum_score():
    low = Candidate(
        trace=Trace(
            id="trace_001",
            input="Question 1",
            output="Wrong answer",
            feedback="negative",
        ),
        score=4.0,
    )

    high = Candidate(
        trace=Trace(
            id="trace_002",
            input="Question 2",
            output="Wrong answer",
            feedback="negative",
        ),
        score=8.0,
    )

    curated = curate_candidates(
        [low, high],
        min_score=5.0,
    )

    assert curated == [high]


def test_curate_candidates_respects_maximum_size():
    candidates = [
        Candidate(
            trace=Trace(
                id=f"trace_{index}",
                input=f"Question {index}",
                output="Wrong answer",
                feedback="negative",
            ),
            score=float(index),
        )
        for index in range(1, 6)
    ]

    curated = curate_candidates(
        candidates,
        min_score=0.0,
        max_items=2,
    )

    assert [candidate.trace.id for candidate in curated] == [
        "trace_5",
        "trace_4",
    ]


def test_curate_candidates_preserves_score_order():
    first = Candidate(
        trace=Trace(
            id="trace_006",
            input="Question 1",
            output="Wrong answer",
            feedback="negative",
        ),
        score=7.0,
    )

    second = Candidate(
        trace=Trace(
            id="trace_007",
            input="Question 2",
            output="Wrong answer",
            feedback="negative",
        ),
        score=9.0,
    )

    curated = curate_candidates(
        [first, second],
        min_score=0.0,
    )

    assert [candidate.trace.id for candidate in curated] == [
        "trace_007",
        "trace_006",
    ]

def test_curate_candidates_preserves_candidate_data():
    candidate = Candidate(
        trace=Trace(
            id="trace_008",
            input="Question",
            output="Wrong answer",
            feedback="negative",
            metadata={"source": "production"},
        ),
        score=9.0,
        signals={
            "failure": 1.0,
            "rarity": 0.5,
            "novelty": 0.8,
        },
        reason="Negative feedback and high novelty.",
    )

    curated = curate_candidates([candidate])

    assert curated == [candidate]
    assert curated[0].signals["novelty"] == 0.8
    assert curated[0].reason == "Negative feedback and high novelty."
    assert curated[0].trace.metadata == {"source": "production"}