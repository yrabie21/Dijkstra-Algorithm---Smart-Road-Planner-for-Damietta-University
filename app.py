"""
Smart Road Planner — Damietta University
=========================================
An interactive educational tool that visualises Dijkstra's algorithm
on a real-world campus map.  Built with Streamlit, NetworkX, and PyVis.

Modules
-------
config          – graph data, icons, positions
dijkstra        – custom Dijkstra implementation with trace
graph_builder   – NetworkX / PyVis graph construction
styles          – application CSS
"""

import base64
import os

import pandas as pd
import streamlit as st
import streamlit.components.v1 as components

from config import DEFAULT_EDGES, LOCATIONS, NODE_ICONS
from dijkstra import dijkstra_with_trace
from graph_builder import build_graph, build_pyvis
from styles import APP_CSS

# ─────────────────────────────────────────────
# PAGE CONFIG
# ─────────────────────────────────────────────
st.set_page_config(
    page_title="Smart Road Planner – Damietta University",
    page_icon="🗺️",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ─────────────────────────────────────────────
# INJECT CSS
# ─────────────────────────────────────────────
st.markdown(APP_CSS, unsafe_allow_html=True)

# ─────────────────────────────────────────────
# SESSION STATE DEFAULTS
# ─────────────────────────────────────────────
if "edge_weights" not in st.session_state:
    st.session_state.edge_weights = dict(DEFAULT_EDGES)
if "path_result" not in st.session_state:
    st.session_state.path_result = None
if "distance_result" not in st.session_state:
    st.session_state.distance_result = None
if "all_distances" not in st.session_state:
    st.session_state.all_distances = None
if "trace_steps" not in st.session_state:
    st.session_state.trace_steps = None
if "op_counts" not in st.session_state:
    st.session_state.op_counts = None
if "searched" not in st.session_state:
    st.session_state.searched = False

# Build graph from current weights
G = build_graph(st.session_state.edge_weights)


# ╔═══════════════════════════════════════════╗
# ║               HERO HEADER                 ║
# ╚═══════════════════════════════════════════╝
st.markdown(
    """
    <div class="hero">
        <h1>🗺️ Smart Road Planner</h1>
        <p>
            Navigate <strong>Damietta University Campus</strong> efficiently.<br>
            Select your start and destination, and let the <em>Dijkstra algorithm</em>
            instantly compute the <strong>shortest walking route</strong> between any two
            buildings or gates.
        </p>
    </div>
    """,
    unsafe_allow_html=True,
)


# ╔═══════════════════════════════════════════╗
# ║                SIDEBAR                    ║
# ╚═══════════════════════════════════════════╝
with st.sidebar:
    # ── University Logo ──
    logo_path = os.path.join(
        os.path.dirname(os.path.abspath(__file__)), "university-logo.png"
    )
    if os.path.exists(logo_path):
        with open(logo_path, "rb") as img_file:
            logo_b64 = base64.b64encode(img_file.read()).decode()
        logo_html = (
            f'<img src="data:image/png;base64,{logo_b64}" '
            f'style="width:110px; border-radius:50%; margin-bottom:0.3rem;">'
        )
    else:
        logo_html = '<span style="font-size:3rem;">🎓</span>'

    st.markdown(
        f"""
        <div style="text-align:center; padding:1rem 0 0.5rem;">
            {logo_html}
            <h2 style="font-weight:900; font-size:1.3rem;
                       margin:0.3rem 0 0.2rem; color:#312e81;">
                Route Planner
            </h2>
            <p style="font-size:0.85rem; color:#64748b; margin:0;">
                Damietta University
            </p>
        </div>
        <hr style="margin:0.8rem 0;">
        """,
        unsafe_allow_html=True,
    )

    # ── Source / Destination selectors ──
    start_point = st.selectbox(
        "📍 Start Point", LOCATIONS, index=0,
        help="Choose where your journey begins.",
    )
    destination = st.selectbox(
        "🏁 Destination", LOCATIONS, index=2,
        help="Choose your destination building.",
    )

    st.markdown("<br>", unsafe_allow_html=True)
    find_btn = st.button(
        "🔍 Find Shortest Path", type="primary", use_container_width=True
    )

    st.markdown("<hr>", unsafe_allow_html=True)

    # ── Custom Edge Weights ──
    with st.expander("⚙️ Customize Road Distances"):
        st.caption(
            "Adjust road distances (metres) and re-run to see "
            "how the path changes."
        )
        new_weights: dict = {}
        weights_changed = False
        for (u, v), default_w in DEFAULT_EDGES.items():
            icon_u = NODE_ICONS.get(u, "📍")
            icon_v = NODE_ICONS.get(v, "📍")
            cur = st.session_state.edge_weights.get((u, v), default_w)
            nw = st.slider(
                f"{icon_u} {u} ↔ {icon_v} {v}",
                50, 1000, cur, 10,
                key=f"w_{u}_{v}",
            )
            new_weights[(u, v)] = nw
            if nw != cur:
                weights_changed = True
        if weights_changed:
            st.session_state.edge_weights = new_weights
            st.session_state.searched = False
            st.rerun()
        if st.button("🔄 Reset to Default", use_container_width=True):
            st.session_state.edge_weights = dict(DEFAULT_EDGES)
            st.session_state.searched = False
            st.rerun()

    st.markdown("<hr>", unsafe_allow_html=True)
    st.markdown(
        f"""
        <div style="font-size:0.85rem; color:#475569; line-height:1.6;">
            <strong>Algorithm:</strong> Dijkstra's Shortest Path<br>
            <strong>Library:</strong> NetworkX + PyVis<br>
            <strong>Nodes:</strong> {len(LOCATIONS)} buildings / gates<br>
            <strong>Edges:</strong> {len(DEFAULT_EDGES)} campus roads<br>
        </div>
        """,
        unsafe_allow_html=True,
    )


# ╔═══════════════════════════════════════════╗
# ║            PATHFINDING LOGIC              ║
# ╚═══════════════════════════════════════════╝
if find_btn:
    if start_point == destination:
        st.warning(
            "⚠️  Start and destination are the same location. "
            "Please choose different points."
        )
        st.session_state.searched = False
    else:
        path, distance, all_distances, steps, op_counts = dijkstra_with_trace(
            G, start_point, destination
        )
        st.session_state.path_result = path
        st.session_state.distance_result = distance
        st.session_state.all_distances = all_distances
        st.session_state.trace_steps = steps
        st.session_state.op_counts = op_counts
        st.session_state.searched = True


# ╔═══════════════════════════════════════════╗
# ║          INTERACTIVE CAMPUS MAP           ║
# ╚═══════════════════════════════════════════╝
col_map, col_info = st.columns([2.5, 1.5], gap="large")

with col_map:
    st.markdown(
        '<div class="card-title">🗺️ Interactive Campus Map</div>',
        unsafe_allow_html=True,
    )
    graph_html = build_pyvis(
        G,
        path=st.session_state.path_result if st.session_state.searched else None,
    )
    components.html(graph_html, height=580, scrolling=False)
    st.caption(
        "💡 **Controls:** Scroll to zoom · Drag to pan · "
        "Use the on-screen buttons or arrow keys to navigate"
    )

with col_info:
    # ── Legend ──
    st.markdown(
        """
        <div class="card">
            <div class="card-title">Legend</div>
            <p style="font-size:0.9rem; color:#475569; line-height:1.9; margin:0;">
                🔵 &nbsp;<strong>Blue node</strong> – Campus location<br>
                🔴 &nbsp;<strong>Red node</strong> – On shortest path<br>
                🟢 &nbsp;<strong>Green node</strong> – Visited (step view)<br>
                🟠 &nbsp;<strong>Orange node</strong> – Currently visiting<br>
                ─── &nbsp;<span style="color:#94a3b8;">Gray edge</span> – Campus road<br>
                ─── &nbsp;<span style="color:#ef4444; font-weight:bold;">Red edge</span> – Shortest route<br>
                ─── &nbsp;<span style="color:#f59e0b; font-weight:bold;">Orange edge</span> – Being relaxed<br>
                🏷️ &nbsp;Edge labels = distance (m)
            </p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    # ── How it Works ──
    st.markdown(
        """
        <div class="card">
            <div class="card-title">🧠 How it Works</div>
            <p style="font-size:0.9rem; color:#475569;">
            This tool uses <strong>Dijkstra's Algorithm</strong>, a famous graph
            search algorithm that finds the shortest path between a starting node
            and all other nodes in a weighted graph.
            </p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    with st.expander("Show Algorithm Steps"):
        st.markdown(
            """
            **Dijkstra's Algorithm Process:**
            1. **Initialize:** Set the distance to the start node to `0` and all
               other nodes to `infinity`.
            2. **Queue:** Place all nodes into an unvisited queue.
            3. **Explore:** Pick the unvisited node with the smallest known
               distance (initially the start node).
            4. **Update Neighbors:** For the current node, look at all its
               unvisited neighbors.  Calculate the distance to them through the
               current node.
            5. **Relax Edges:** If this new distance is smaller than their
               currently known distance, update it.
            6. **Mark Visited:** Once all neighbors of the current node are
               checked, mark it as visited.  A visited node's shortest path is
               finalized.
            7. **Repeat:** Continue until the destination node is marked as
               visited.
            """
        )


# ╔═══════════════════════════════════════════╗
# ║              RESULTS PANEL                ║
# ╚═══════════════════════════════════════════╝
if st.session_state.searched:
    path = st.session_state.path_result
    distance = st.session_state.distance_result
    all_distances = st.session_state.all_distances

    st.markdown("---")

    if path is None:
        st.error("❌ No path found between the selected locations.")
    else:
        r_col1, r_col2 = st.columns([1.5, 1])

        with r_col1:
            st.markdown(
                '<div class="card-title">📊 Route Analysis</div>',
                unsafe_allow_html=True,
            )

            m1, m2, m3 = st.columns(3)
            with m1:
                st.metric(
                    "📏 Total Distance", f"{distance} m",
                    help="Shortest walking distance in metres",
                )
            with m2:
                walk_min = round(distance / 80)
                st.metric(
                    "🚶 Est. Walking Time", f"~{walk_min} min",
                    help="Estimated at 80 m/min",
                )
            with m3:
                st.metric(
                    "🔢 Stops", len(path),
                    help="Number of locations on the route",
                )

            st.markdown("<br>", unsafe_allow_html=True)

            # Route badges
            route_html = (
                '<div style="margin-top:0.4rem; display:flex; '
                'flex-wrap:wrap; align-items:center; gap:0.25rem;">'
            )
            for i, stop in enumerate(path):
                icon = NODE_ICONS.get(stop, "📍")
                route_html += f'<span class="route-badge">{icon} {stop}</span>'
                if i < len(path) - 1:
                    route_html += '<span class="route-arrow">→</span>'
            route_html += "</div>"
            st.markdown(route_html, unsafe_allow_html=True)

            # Segment breakdown
            st.markdown("<br>", unsafe_allow_html=True)
            st.markdown(
                '<div class="card-title">🛣️ Segment Breakdown</div>',
                unsafe_allow_html=True,
            )
            seg_cols = st.columns(min(len(path) - 1, 3))
            for i in range(len(path) - 1):
                seg_dist = G[path[i]][path[i + 1]]["weight"]
                col = seg_cols[i % len(seg_cols)]
                with col:
                    st.markdown(
                        f"""
                        <div class="card" style="padding:0.9rem 1.1rem;
                             box-shadow:none; border:1px solid #e2e8f0;
                             background:#f8fafc;">
                            <div style="font-size:0.8rem; color:#6366f1;
                                 font-weight:700; text-transform:uppercase;
                                 letter-spacing:0.06em;">
                                Leg {i + 1}
                            </div>
                            <div style="font-size:0.95rem; color:#334155;
                                 margin:0.3rem 0; font-weight:600;">
                                {NODE_ICONS.get(path[i], '📍')} {path[i]}
                                <span style="color:#f59e0b; font-weight:900;">
                                    →
                                </span>
                                {NODE_ICONS.get(path[i + 1], '📍')} {path[i + 1]}
                            </div>
                            <div style="font-size:1.05rem; font-weight:800;
                                 color:#10b981;">
                                {seg_dist} m
                            </div>
                        </div>
                        """,
                        unsafe_allow_html=True,
                    )

            st.success(
                f"✅ Optimal route found! Travel **{distance} metres** "
                f"via **{' → '.join(path)}**."
            )

        with r_col2:
            st.markdown(
                f'<div class="card-title">📍 Shortest Distances from '
                f'{start_point}</div>',
                unsafe_allow_html=True,
            )
            st.markdown(
                """
                <p style="font-size:0.9rem; color:#64748b; margin-bottom:1rem;">
                Dijkstra's algorithm automatically computes the shortest
                distance to <b>all connected nodes</b> from the starting point.
                Here are the calculated minimum distances:
                </p>
                """,
                unsafe_allow_html=True,
            )

            dist_data = []
            for node in LOCATIONS:
                if node in all_distances:
                    dist_data.append({
                        "Location": f"{NODE_ICONS.get(node, '📍')} {node}",
                        "Distance (m)": all_distances[node],
                    })
                else:
                    dist_data.append({
                        "Location": f"{NODE_ICONS.get(node, '📍')} {node}",
                        "Distance (m)": "Unreachable",
                    })

            df_distances = pd.DataFrame(dist_data).sort_values("Distance (m)")
            st.dataframe(df_distances, use_container_width=True, hide_index=True)

elif not find_btn:
    st.markdown("---")
    st.info(
        "👈  Use the sidebar to select a **Start Point** and "
        "**Destination**, then click **Find Shortest Path**."
    )


# ╔═══════════════════════════════════════════╗
# ║           ALGORITHM DEEP DIVE             ║
# ╚═══════════════════════════════════════════╝
if (
    st.session_state.searched
    and st.session_state.trace_steps
    and st.session_state.path_result
):
    st.markdown("---")
    st.markdown(
        '<div class="card-title">🔬 Algorithm Deep Dive</div>',
        unsafe_allow_html=True,
    )

    tab_steps, tab_complexity = st.tabs(
        ["📖 Step-by-Step Walkthrough", "📐 Complexity Analysis"]
    )

    steps = st.session_state.trace_steps
    op_counts = st.session_state.op_counts

    # ── TAB 1 · Step-by-Step ──────────────────
    with tab_steps:
        st.markdown(
            """
            Walk through each iteration of Dijkstra's algorithm.  Use the
            buttons to step forward and backward, see which node is visited,
            which edges are relaxed, and the state of the **priority queue**
            at every step.
            """
        )

        # Step navigation buttons
        if "step_idx" not in st.session_state:
            st.session_state.step_idx = 1
        max_step = len(steps)
        if st.session_state.step_idx > max_step:
            st.session_state.step_idx = max_step

        nav1, nav2, nav3 = st.columns([1, 2, 1])
        with nav1:
            if st.button(
                "⬅️ Previous Step",
                use_container_width=True,
                disabled=(st.session_state.step_idx <= 1),
            ):
                st.session_state.step_idx -= 1
                st.rerun()
        with nav2:
            st.markdown(
                f"""
                <div class="step-counter">
                    <div class="step-label">Algorithm Iteration</div>
                    Step {st.session_state.step_idx} of {max_step}
                </div>
                """,
                unsafe_allow_html=True,
            )
        with nav3:
            if st.button(
                "Next Step ➡️",
                use_container_width=True,
                disabled=(st.session_state.step_idx >= max_step),
            ):
                st.session_state.step_idx += 1
                st.rerun()

        step = steps[st.session_state.step_idx - 1]

        # Map + details columns
        sc1, sc2 = st.columns([1.6, 1], gap="large")

        with sc1:
            st.markdown("**🗺️ Step Map**")
            step_html = build_pyvis(G, step_data=step)
            components.html(step_html, height=580, scrolling=False)
            st.caption(
                "💡 **Controls:** Scroll to zoom · Drag to pan · "
                "Use the on-screen buttons or arrow keys to navigate"
            )

        with sc2:
            cur = step["current_node"]
            icon = NODE_ICONS.get(cur, "📍")
            st.markdown(
                f"""
                <div class="step-current">
                    <div style="font-size:0.8rem; color:#92400e;
                         font-weight:700; text-transform:uppercase;">
                        Step {step["iteration"]}
                    </div>
                    <div style="font-size:1.1rem; font-weight:700;
                         color:#78350f; margin:0.3rem 0;">
                        Visiting {icon} {cur}
                    </div>
                    <div style="font-size:0.9rem; color:#a16207;">
                        Distance from source:
                        <strong>{step["current_dist"]} m</strong>
                    </div>
                </div>
                """,
                unsafe_allow_html=True,
            )

            # Relaxed edges
            if step["relaxed"]:
                st.markdown("**🔄 Edges Relaxed:**")
                for u, v, w, new_d in step["relaxed"]:
                    st.markdown(
                        f"&nbsp;&nbsp; {NODE_ICONS.get(u, '')} {u} → "
                        f"{NODE_ICONS.get(v, '')} {v}  (+{w}m = **{new_d}m**)"
                    )
            else:
                st.caption("No edges relaxed in this step.")

            # Priority Queue — visual pipe
            st.markdown("**📋 Priority Queue (Min-Heap):**")
            if step["queue"]:
                pq_visual = (
                    '<div style="display:flex; align-items:center; gap:0;">'
                    '<div class="pq-arrow-out">⇨ OUT</div>'
                    '<div class="pq-visual">'
                )
                for i, (d, n) in enumerate(step["queue"]):
                    cls = (
                        "pq-visual-item pq-front"
                        if i == 0
                        else "pq-visual-item"
                    )
                    pq_visual += (
                        f'<div class="{cls}">{NODE_ICONS.get(n, "")} {n}'
                        f'<span class="pq-dist">{d}m</span></div>'
                    )
                pq_visual += (
                    "</div>"
                    '<div style="padding:0 0.5rem; font-size:0.8rem; '
                    'color:#6366f1; font-weight:600;">IN ⇨</div>'
                    "</div>"
                )
                st.markdown(pq_visual, unsafe_allow_html=True)
                st.caption(
                    "🟡 The leftmost item (lowest distance) will be "
                    "extracted next — this is how a min-heap works."
                )

                # Badge summary
                pq_html = (
                    '<div style="display:flex; flex-wrap:wrap; '
                    'gap:4px; margin-top:0.5rem;">'
                )
                for i, (d, n) in enumerate(step["queue"]):
                    cls = "pq-entry popped" if i == 0 else "pq-entry"
                    pq_html += (
                        f'<span class="{cls}">'
                        f'{NODE_ICONS.get(n, "")} {n}: {d}m</span>'
                    )
                pq_html += "</div>"
                st.markdown(pq_html, unsafe_allow_html=True)
            else:
                st.caption("Queue is empty — algorithm complete.")

            # Visited set
            visited_str = ", ".join(
                f"{NODE_ICONS.get(n, '')}{n}" for n in step["visited"]
            )
            st.markdown(f"**✅ Visited:** {visited_str}")

    # ── TAB 2 · Complexity Analysis ───────────
    with tab_complexity:
        st.markdown(
            """
            Dijkstra's algorithm with a **binary heap** (min-priority queue)
            has the following theoretical complexities, where **V** = number
            of vertices and **E** = number of edges.
            """
        )

        tc1, tc2 = st.columns(2)
        with tc1:
            st.markdown(
                """
                <div style="background:#f0fdf4; border:1px solid #86efac;
                     border-radius:12px; padding:1.2rem; text-align:center;
                     margin-bottom:1rem;">
                    <div style="font-size:0.75rem; color:#15803d;
                         font-weight:700; text-transform:uppercase;">
                        Time Complexity
                    </div>
                    <div style="font-size:1.6rem; font-weight:800;
                         color:#166534; margin:0.4rem 0;">
                        O((V + E) log V)
                    </div>
                    <div style="font-size:0.8rem; color:#4ade80;">
                        Each vertex extracted once · each edge relaxed at
                        most once
                    </div>
                </div>
                """,
                unsafe_allow_html=True,
            )
        with tc2:
            st.markdown(
                """
                <div style="background:#eff6ff; border:1px solid #93c5fd;
                     border-radius:12px; padding:1.2rem; text-align:center;
                     margin-bottom:1rem;">
                    <div style="font-size:0.75rem; color:#1d4ed8;
                         font-weight:700; text-transform:uppercase;">
                        Space Complexity
                    </div>
                    <div style="font-size:1.6rem; font-weight:800;
                         color:#1e40af; margin:0.4rem 0;">
                        O(V)
                    </div>
                    <div style="font-size:0.8rem; color:#60a5fa;">
                        Distance array + predecessor array + priority queue
                    </div>
                </div>
                """,
                unsafe_allow_html=True,
            )

        st.markdown("#### 📊 Actual Operation Counts (This Run)")
        V = len(LOCATIONS)
        E = len(DEFAULT_EDGES)
        oc1, oc2, oc3, oc4 = st.columns(4)
        with oc1:
            st.metric(
                "🔁 Iterations", op_counts["iterations"],
                help=f"Nodes visited (max V={V})",
            )
        with oc2:
            st.metric(
                "🔀 Edge Relaxations", op_counts["relaxations"],
                help=f"Edges relaxed (max E={E})",
            )
        with oc3:
            st.metric(
                "📋 Queue Operations", op_counts["queue_ops"],
                help="Push + Pop operations on the min-heap",
            )
        with oc4:
            st.metric(
                "⚖️ Comparisons", op_counts["comparisons"],
                help="Distance comparisons + visited checks",
            )

        log_v = round(3.3219 * len(bin(V)[2:]), 1)
        st.markdown(
            f"""
            <div class="card" style="margin-top:1rem;">
                <div class="card-title">📝 Analysis for This Graph</div>
                <p style="font-size:0.9rem; color:#475569; line-height:1.7;">
                    With <strong>V = {V}</strong> vertices and
                    <strong>E = {E}</strong> edges:<br>
                    • Theoretical upper bound:
                      <strong>O(({V} + {E}) × log {V})</strong>
                      ≈ <strong>O({V + E} × {log_v:.1f})</strong>
                      ≈ <strong>{int((V + E) * log_v)}</strong>
                      operations<br>
                    • Actual operations in this run:
                      <strong>{sum(op_counts.values())}</strong><br>
                    • The algorithm terminated after visiting
                      <strong>{op_counts["iterations"]}</strong> out of {V}
                      nodes (early exit when destination is reached).
                </p>
            </div>
            """,
            unsafe_allow_html=True,
        )
