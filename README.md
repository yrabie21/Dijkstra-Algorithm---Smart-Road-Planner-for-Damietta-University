<div align="center">

# 🗺️ Smart Road Planner

### Damietta University Campus — Shortest Path Finder

An interactive educational web application that visualises **Dijkstra's Algorithm**
on a real-world university campus map, built with Python, Streamlit, NetworkX, and PyVis.

[![Python](https://img.shields.io/badge/Python-3.10+-3776AB?logo=python&logoColor=white)](https://python.org)
[![Streamlit](https://img.shields.io/badge/Streamlit-1.30+-FF4B4B?logo=streamlit&logoColor=white)](https://streamlit.io)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)

</div>

---

## 📌 About

This project demonstrates how **Dijkstra's shortest-path algorithm** works in a practical, real-life context — navigating between buildings and gates on the Damietta University campus. It was developed as a course project for **Programming for Problem Solving**.

Rather than just computing results, the app provides a full **step-by-step walkthrough** of the algorithm, showing how it explores nodes, relaxes edges, and manages its priority queue — making it a powerful **educational tool** for understanding graph algorithms.

---

## ✨ Features

| Feature | Description |
|---|---|
| **Interactive Campus Map** | Drag, zoom, and explore a graph of 7 campus locations and 10 roads powered by PyVis |
| **Shortest Path Finder** | Computes the optimal route between any two campus locations using a custom Dijkstra implementation |
| **Step-by-Step Walkthrough** | Navigate through each algorithm iteration with Previous / Next buttons; see visited nodes, relaxed edges, and queue state |
| **Visual Priority Queue** | A horizontal pipe diagram that illustrates how the min-heap works — showing which node gets extracted next |
| **Custom Edge Weights** | Sidebar sliders to modify any road distance (50–1000 m) and instantly see how it affects the shortest path |
| **Complexity Analysis** | Displays theoretical O((V+E) log V) time complexity alongside actual operation counts from each run |
| **Route Analysis** | Metrics for total distance, estimated walking time, number of stops, and a per-segment breakdown |
| **Distance Table** | Shows shortest distances from the source to every campus node — demonstrating Dijkstra's "all-nodes" property |

---

## 🛠️ Tech Stack

| Technology | Role |
|---|---|
| **Python 3.10+** | Core language |
| **Streamlit** | Web application framework |
| **NetworkX** | Graph data structure & manipulation |
| **PyVis** | Interactive graph visualisation (vis.js wrapper) |
| **Pandas** | Distance table rendering |
| **heapq** | Binary min-heap for the priority queue |

---

## 📁 Project Structure

```
smart-road-planner/
├── app.py              # Main Streamlit application (UI orchestration)
├── config.py           # Graph data: edges, locations, icons, positions
├── dijkstra.py         # Custom Dijkstra algorithm with execution trace
├── graph_builder.py    # NetworkX graph construction + PyVis rendering
├── styles.py           # All CSS styles for the application
├── requirements.txt    # Python dependencies
├── university-logo.png # University logo displayed in sidebar
├── .gitignore          # Git ignore rules
├── lib/                # External JS libraries (vis.js, tom-select)
└── README.md           # This file
```

### Module Responsibilities

- **`config.py`** — Single source of truth for graph topology (edge weights, node names, emoji icons, fixed layout positions).
- **`dijkstra.py`** — Hand-written Dijkstra's algorithm using `heapq`. Records every iteration (visited set, priority queue state, relaxed edges, operation counts) for step-by-step playback.
- **`graph_builder.py`** — Constructs a `NetworkX` graph from edge weights and renders it as interactive HTML via `PyVis`, with support for path highlighting and step-by-step colouring.
- **`styles.py`** — All custom CSS in one place for easy maintenance.
- **`app.py`** — Thin orchestration layer that imports from the modules above, manages Streamlit session state, and assembles the UI.

---

## 🚀 Getting Started

### Prerequisites

- **Python 3.10** or higher
- **pip** (Python package manager)

### Installation

1. **Clone the repository:**
   ```bash
   git clone https://github.com/<your-username>/smart-road-planner.git
   cd smart-road-planner
   ```

2. **Create a virtual environment (recommended):**
   ```bash
   python -m venv venv
   source venv/bin/activate      # Linux / macOS
   # venv\Scripts\activate       # Windows
   ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Run the application:**
   ```bash
   streamlit run app.py
   ```

5. **Open in browser:**
   The app will launch at `http://localhost:8501`.

---

## 📖 How to Use

1. **Select locations** — Use the sidebar to choose a *Start Point* and *Destination*.
2. **Find path** — Click the **🔍 Find Shortest Path** button.
3. **Explore results** — View the highlighted path on the map, route analysis metrics, and per-segment breakdown.
4. **Step through the algorithm** — Scroll down to *Algorithm Deep Dive* and use the **⬅️ / ➡️** buttons to walk through each Dijkstra iteration.
5. **Modify weights** — Expand *⚙️ Customize Road Distances* in the sidebar, adjust any slider, and watch the path change.
6. **Analyse complexity** — Switch to the *📐 Complexity Analysis* tab to compare theoretical vs. actual operation counts.

---

## 🧠 Algorithm: Dijkstra's Shortest Path

Dijkstra's algorithm finds the shortest path from a single source node to all other nodes in a graph with non-negative edge weights.

### Steps

1. **Initialise** — Set distance to source = 0; all others = ∞.
2. **Push** source into a min-priority queue.
3. **Extract** the node with the smallest distance.
4. **Relax** all outgoing edges — if a shorter path is found, update the distance and push the neighbour.
5. **Repeat** until the destination is extracted or the queue is empty.

### Complexity (Binary Heap)

| Metric | Bound |
|---|---|
| Time | **O((V + E) log V)** |
| Space | **O(V)** |

Where **V** = vertices, **E** = edges.

---

## 🎨 Colour Legend

| Colour | Meaning |
|---|---|
| 🔵 Blue node | Default campus location |
| 🔴 Red node | On the shortest path |
| 🟢 Green node | Already visited (step view) |
| 🟠 Orange node | Currently being visited |
| Gray edge | Default campus road |
| Red edge | Part of shortest route |
| Orange edge | Being relaxed in current step |

---

## 👥 Authors

- **Youssef Mohamed Rabie** — Damietta University, Faculty of Computers and AI

---

## 📄 License

This project was developed as part of a Programming for Problem solving academic project.

---

<div align="center">
  <sub>Built with ❤️ for Programming for Problem Solving — Damietta University 2026</sub>
</div>
