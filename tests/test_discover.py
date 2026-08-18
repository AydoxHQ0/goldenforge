from goldenforge.discover.basic import discover_candidates
from goldenforge.models import Trace


def test_discover_candidates_selects_negative_feedback():
    trace = Trace(
        id="trace_001",
        input="Question",
        output="Wrong answer",
        feedback="negative",
    )

    candidates = discover_candidates([trace])

    assert len(candidates) == 1
    assert candidates[0].trace == trace
    assert candidates[0].score == 5.0


def test_discover_candidates_ignores_positive_feedback():
    trace = Trace(
        id="trace_002",
        input="Question",
        output="Good answer",
        feedback="positive",
    )

    candidates = discover_candidates([trace])

    assert candidates == []


def test_discover_candidates_contains_signals_and_reason():
    trace = Trace(
        id="trace_003",
        input="Question",
        output="Wrong answer",
        feedback="negative",
        evaluation={"correct": False},
        context={"documents": ["doc1"]},
        tools=[{"name": "search"}],
        metadata={"source": "production"},
    )

    candidates = discover_candidates([trace])

    candidate = candidates[0]

    assert candidate.score == 10.0
    assert candidate.signals["failure"] == 1.0
    assert candidate.signals["evaluation"] == 1.0
    assert candidate.signals["context"] == 1.0
    assert candidate.signals["tools"] == 1.0
    assert candidate.signals["metadata"] == 1.0
    assert "negative user feedback" in candidate.reason


def test_discover_candidates_ranks_by_score():
    low_value = Trace(
        id="trace_004",
        input="Question",
        output="Wrong answer",
        feedback="negative",
    )

    high_value = Trace(
        id="trace_005",
        input="Complex question",
        output="Wrong answer",
        feedback="negative",
        evaluation={"correct": False},
        context={"documents": ["doc1"]},
        tools=[{"name": "search"}],
        metadata={"source": "production"},
    )

    candidates = discover_candidates([low_value, high_value])

    assert [candidate.trace.id for candidate in candidates] == [
        "trace_005",
        "trace_004",
    ]


def test_discover_candidates_calculates_rarity():
    rare = Trace(
        id="trace_006",
        input="Rare question",
        output="Wrong answer",
        feedback="negative",
    )

    common_1 = Trace(
        id="trace_007",
        input="Common question",
        output="Wrong answer",
        feedback="negative",
    )

    common_2 = Trace(
        id="trace_008",
        input="Common question",
        output="Another wrong answer",
        feedback="negative",
    )

    candidates = discover_candidates([rare, common_1, common_2])

    by_id = {candidate.trace.id: candidate for candidate in candidates}

    assert by_id["trace_006"].signals["rarity"] == 1.0
    assert by_id["trace_007"].signals["rarity"] == 0.5
    assert by_id["trace_008"].signals["rarity"] == 0.5


def test_discover_candidates_rarity_considers_all_traces():
    negative = Trace(
        id="trace_009",
        input="Repeated question",
        output="Wrong answer",
        feedback="negative",
    )

    positive = Trace(
        id="trace_010",
        input="Repeated question",
        output="Good answer",
        feedback="positive",
    )

    candidates = discover_candidates([negative, positive])

    assert len(candidates) == 1
    assert candidates[0].trace.id == "trace_009"
    assert candidates[0].signals["rarity"] == 0.5
def test_discover_candidates_uses_rarity_as_tiebreaker():
    common_1 = Trace(
        id="trace_011",
        input="Common question",
        output="Wrong answer",
        feedback="negative",
    )

    common_2 = Trace(
        id="trace_012",
        input="Common question",
        output="Another wrong answer",
        feedback="negative",
    )

    rare = Trace(
        id="trace_013",
        input="Rare question",
        output="Wrong answer",
        feedback="negative",
    )

    candidates = discover_candidates([common_1, common_2, rare])

    assert [candidate.trace.id for candidate in candidates] == [
        "trace_013",
        "trace_011",
        "trace_012",
    ]

def test_discover_candidates_calculates_novelty():
    common = Trace(
        id="trace_014",
        input="How do I reset my password?",
        output="Wrong answer",
        feedback="negative",
    )

    similar = Trace(
        id="trace_015",
        input="How can I reset my password?",
        output="Another wrong answer",
        feedback="negative",
    )

    novel = Trace(
        id="trace_016",
        input="Why was my international payment declined?",
        output="Wrong answer",
        feedback="negative",
    )

    candidates = discover_candidates([common, similar, novel])

    by_id = {candidate.trace.id: candidate for candidate in candidates}

    assert "novelty" in by_id["trace_014"].signals
    assert "novelty" in by_id["trace_015"].signals
    assert "novelty" in by_id["trace_016"].signals

    assert by_id["trace_016"].signals["novelty"] > by_id["trace_014"].signals["novelty"]
    assert by_id["trace_016"].signals["novelty"] > by_id["trace_015"].signals["novelty"]