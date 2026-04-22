"""
Custom Dijkstra's algorithm with full execution trace.

Provides `dijkstra_with_trace()` — a hand-written implementation using a
binary min-heap (heapq) that records every iteration so the Streamlit UI
can replay the algorithm step-by-step.
"""

from __future__ import annotations

import heapq

import networkx as nx


def dijkstra_with_trace(
    G: nx.Graph, source: str, target: str
) -> tuple[list[str] | None, int | None, dict, list[dict], dict]:
    """
    Run Dijkstra's algorithm from *source* to *target* on graph *G*.

    Returns
    -------
    path : list[str] | None
        Ordered node list from source → target, or None if unreachable.
    distance : int | None
        Total shortest distance in metres, or None.
    all_distances : dict[str, int | float]
        Shortest distance from *source* to every reachable node.
    steps : list[dict]
        One entry per iteration with keys:
        ``iteration, current_node, current_dist, distances, visited,
        queue, relaxed``.
    op_counts : dict[str, int]
        Operation counters: iterations, relaxations, queue_ops, comparisons.
    """
    dist = {node: float("inf") for node in G.nodes()}
    dist[source] = 0
    prev: dict[str, str | None] = {node: None for node in G.nodes()}
    visited: set[str] = set()
    pq: list[tuple[int, str]] = [(0, source)]

    steps: list[dict] = []
    op: dict[str, int] = {
        "iterations": 0,
        "relaxations": 0,
        "queue_ops": 1,       # initial push
        "comparisons": 0,
    }

    while pq:
        d, u = heapq.heappop(pq)
        op["queue_ops"] += 1

        if u in visited:
            op["comparisons"] += 1
            continue
        visited.add(u)
        op["iterations"] += 1

        relaxed: list[tuple[str, str, int, int]] = []
        for v in G.neighbors(u):
            op["comparisons"] += 1
            if v not in visited:
                new_dist = d + G[u][v]["weight"]
                op["comparisons"] += 1
                if new_dist < dist[v]:
                    dist[v] = new_dist
                    prev[v] = u
                    heapq.heappush(pq, (new_dist, v))
                    op["relaxations"] += 1
                    op["queue_ops"] += 1
                    relaxed.append((u, v, G[u][v]["weight"], new_dist))

        steps.append(
            {
                "iteration": len(steps) + 1,
                "current_node": u,
                "current_dist": d,
                "distances": dict(dist),
                "visited": set(visited),
                "queue": sorted(
                    [(dd, nn) for dd, nn in pq if nn not in visited]
                ),
                "relaxed": relaxed,
            }
        )

        if u == target:
            break

    # Reconstruct path
    path: list[str] = []
    node: str | None = target
    while node is not None:
        path.append(node)
        node = prev[node]
    path.reverse()

    if dist[target] == float("inf"):
        return None, None, dict(dist), steps, op
    return path, dist[target], dict(dist), steps, op
