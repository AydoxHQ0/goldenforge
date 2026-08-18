from goldenforge.cluster.basic import cluster_traces
from goldenforge.models import Trace


def test_cluster_traces_groups_similar_inputs():
    password_1 = Trace(
        id="trace_001",
        input="How do I reset my password?",
        output="Use the reset link.",
    )

    password_2 = Trace(
        id="trace_002",
        input="How can I reset my password?",
        output="Use the reset link.",
    )

    payment = Trace(
        id="trace_003",
        input="Why was my international payment declined?",
        output="Contact your bank.",
    )

    clusters = cluster_traces(
        [password_1, password_2, payment]
    )

    assert len(clusters) == 2

    cluster_ids = [
        {trace.id for trace in cluster}
        for cluster in clusters
    ]

    assert {"trace_001", "trace_002"} in cluster_ids
    assert {"trace_003"} in cluster_ids
def test_cluster_traces_respects_similarity_threshold():
    first = Trace(
        id="trace_004",
        input="How do I reset my password?",
        output="Answer",
    )

    second = Trace(
        id="trace_005",
        input="How can I reset my password?",
        output="Another answer",
    )

    strict_clusters = cluster_traces(
        [first, second],
        threshold=0.8,
    )

    loose_clusters = cluster_traces(
        [first, second],
        threshold=0.5,
    )

    assert len(strict_clusters) == 2
    assert len(loose_clusters) == 1

def test_cluster_traces_keeps_unique_trace_as_single_cluster():
    trace = Trace(
        id="trace_006",
        input="Why was my international payment declined?",
        output="Contact your bank.",
    )

    clusters = cluster_traces([trace])

    assert clusters == [[trace]]

def test_cluster_traces_preserves_all_traces():
    traces = [
        Trace(
            id="trace_007",
            input="How do I reset my password?",
            output="Answer",
        ),
        Trace(
            id="trace_008",
            input="How can I reset my password?",
            output="Answer",
        ),
        Trace(
            id="trace_009",
            input="Why was my payment declined?",
            output="Answer",
        ),
    ]

    clusters = cluster_traces(traces)

    clustered_ids = [
        trace.id
        for cluster in clusters
        for trace in cluster
    ]

    assert sorted(clustered_ids) == sorted(
        trace.id for trace in traces
    )