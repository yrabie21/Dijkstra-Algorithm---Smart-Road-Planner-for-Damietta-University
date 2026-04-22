"""
Graph construction and PyVis visualisation helpers.

* `build_graph()`  — create a NetworkX weighted graph from an edge dict.
* `build_pyvis()`  — render the graph as an interactive PyVis HTML string
  with optional path / step-by-step highlighting.
"""

from __future__ import annotations

import os
import tempfile

import networkx as nx
from pyvis.network import Network

from config import NODE_ICONS, NODE_POS


# ─────────────────────────────────────────────
# GRAPH CONSTRUCTION
# ─────────────────────────────────────────────
def build_graph(edge_weights: dict[tuple[str, str], int]) -> nx.Graph:
    """Return a NetworkX undirected graph from an edge-weight dictionary."""
    G = nx.Graph()
    for (u, v), w in edge_weights.items():
        G.add_edge(u, v, weight=w)
    return G


# ─────────────────────────────────────────────
# PYVIS VISUALISATION
# ─────────────────────────────────────────────
_NAV_CSS = """\
<style>
div.vis-network div.vis-navigation div.vis-button {
    width: 34px !important; height: 34px !important;
    background-image: none !important;
    background-color: #ffffff !important;
    border: 1px solid #cbd5e1 !important;
    border-radius: 8px !important;
    cursor: pointer !important;
    box-shadow: 0 1px 3px rgba(0,0,0,0.08) !important;
    display: flex !important; align-items: center !important;
    justify-content: center !important;
    transition: all 0.15s ease !important;
    font-size: 0 !important;
}
div.vis-network div.vis-navigation div.vis-button:hover {
    background-color: #e0e7ff !important;
    border-color: #6366f1 !important;
}
div.vis-button.vis-up:after    { content: '↑'; font-size: 16px; color: #475569; }
div.vis-button.vis-down:after  { content: '↓'; font-size: 16px; color: #475569; }
div.vis-button.vis-left:after  { content: '←'; font-size: 16px; color: #475569; }
div.vis-button.vis-right:after { content: '→'; font-size: 16px; color: #475569; }
div.vis-button.vis-zoomIn:after     { content: '+'; font-size: 18px; font-weight: bold; color: #475569; }
div.vis-button.vis-zoomOut:after    { content: '−'; font-size: 18px; font-weight: bold; color: #475569; }
div.vis-button.vis-zoomExtends:after { content: '⊡'; font-size: 16px; color: #475569; }
</style>
"""


def build_pyvis(
    G: nx.Graph,
    path: list[str] | None = None,
    step_data: dict | None = None,
) -> str:
    """
    Build a PyVis interactive graph and return the HTML string.

    Parameters
    ----------
    G : nx.Graph
        The campus graph.
    path : list[str] | None
        If given, highlight this path in red (final shortest path mode).
    step_data : dict | None
        If given, colour nodes/edges by algorithm-step state (step mode).
    """
    path_edges: set[frozenset] = set()
    path_nodes: set[str] = set()
    visited_nodes: set[str] = set()
    current_node: str | None = None
    relaxed_edge_set: set[frozenset] = set()

    if path and not step_data:
        path_nodes = set(path)
        for i in range(len(path) - 1):
            path_edges.add(frozenset({path[i], path[i + 1]}))

    if step_data:
        visited_nodes = step_data.get("visited", set())
        current_node = step_data.get("current_node")
        for edge_info in step_data.get("relaxed", []):
            relaxed_edge_set.add(frozenset({edge_info[0], edge_info[1]}))

    # ── Network setup ──
    net = Network(
        height="560px",
        width="100%",
        bgcolor="#ffffff",
        font_color="#1e293b",
        directed=False,
        notebook=False,
    )
    net.toggle_physics(True)
    net.set_options(
        """
        {
          "physics": { "enabled": false },
          "interaction": {
            "hover": true, "tooltipDelay": 150,
            "navigationButtons": true,
            "keyboard": {
              "enabled": true,
              "speed": { "x": 10, "y": 10, "zoom": 0.02 },
              "bindToWindow": false
            },
            "zoomView": true, "dragView": true
          },
          "edges": { "smooth": { "type": "curvedCW", "roundness": 0.1 } }
        }
        """
    )

    # ── Nodes ──
    for node in G.nodes():
        is_in_path = node in path_nodes
        is_current = node == current_node
        is_visited = node in visited_nodes and not is_current
        label = f"{NODE_ICONS.get(node, '📍')} {node}"

        if is_current:
            bg, brd, fc, sz = "#f59e0b", "#d97706", "#ffffff", 38
        elif is_in_path:
            bg, brd, fc, sz = "#ef4444", "#b91c1c", "#ffffff", 35
        elif is_visited:
            bg, brd, fc, sz = "#10b981", "#059669", "#ffffff", 30
        else:
            bg, brd, fc, sz = "#e0e7ff", "#6366f1", "#1e293b", 25

        net.add_node(
            node,
            label=label,
            x=NODE_POS[node][0],
            y=NODE_POS[node][1],
            color={
                "background": bg,
                "border": brd,
                "highlight": {"background": "#f97316", "border": "#ea580c"},
                "hover": {"background": "#f97316", "border": "#ea580c"},
            },
            size=sz,
            font={"size": 15 if sz > 25 else 13, "color": fc, "bold": sz > 25},
            shadow=True,
            borderWidth=3 if sz > 25 else 2,
            physics=False,
        )

    # ── Edges ──
    for u, v, data in G.edges(data=True):
        w = data["weight"]
        ek = frozenset({u, v})
        is_path_edge = ek in path_edges
        is_relaxed = ek in relaxed_edge_set

        if is_path_edge:
            ec, ew = "#ef4444", 5
        elif is_relaxed:
            ec, ew = "#f59e0b", 4
        else:
            ec, ew = "#cbd5e1", 2

        net.add_edge(
            u,
            v,
            label=f"{w} m",
            width=ew,
            color={"color": ec, "highlight": "#f97316", "hover": "#f97316"},
            font={
                "size": 13,
                "color": (
                    "#b91c1c"
                    if is_path_edge
                    else ("#d97706" if is_relaxed else "#475569")
                ),
                "strokeWidth": 3,
                "strokeColor": "#ffffff",
                "bold": is_path_edge or is_relaxed,
            },
            smooth={"type": "curvedCW", "roundness": 0.1},
            shadow=is_path_edge or is_relaxed,
        )

    # ── Render to HTML string ──
    with tempfile.NamedTemporaryFile(
        suffix=".html", delete=False, mode="w", encoding="utf-8"
    ) as tmp:
        tmp_path = tmp.name
    net.save_graph(tmp_path)
    with open(tmp_path, "r", encoding="utf-8") as f:
        html_content = f.read()
    os.unlink(tmp_path)

    # Inject custom button CSS (vis.js icons are missing in this env)
    html_content = html_content.replace("</head>", _NAV_CSS + "</head>")
    return html_content
