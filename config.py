"""
Configuration constants for the Smart Road Planner.

Contains graph topology (default edge weights), location names,
node icons / emoji, and node positions for the PyVis layout.
"""

# ─────────────────────────────────────────────
# DEFAULT EDGE WEIGHTS  (u, v) → distance in metres
# ─────────────────────────────────────────────
DEFAULT_EDGES = {
    ("Main Gate", "Engineering"):       250,
    ("Main Gate", "Commerce"):          300,
    ("Main Gate", "Arts"):              400,
    ("Engineering", "Computers & AI"):  100,
    ("Engineering", "Administration"):  150,
    ("Computers & AI", "Law"):          120,
    ("Commerce", "Arts"):               150,
    ("Commerce", "Administration"):     200,
    ("Arts", "Law"):                    200,
    ("Law", "Administration"):          250,
}

# ─────────────────────────────────────────────
# CAMPUS LOCATIONS (ordered list)
# ─────────────────────────────────────────────
LOCATIONS = [
    "Main Gate",
    "Engineering",
    "Computers & AI",
    "Commerce",
    "Arts",
    "Law",
    "Administration",
]

# ─────────────────────────────────────────────
# NODE ICONS  (emoji used in labels / badges)
# ─────────────────────────────────────────────
NODE_ICONS = {
    "Main Gate":      "🚪",
    "Engineering":    "⚙️",
    "Computers & AI": "💻",
    "Commerce":       "📊",
    "Arts":           "🎨",
    "Law":            "⚖️",
    "Administration": "🏛️",
}

# ─────────────────────────────────────────────
# NODE POSITIONS  (x, y) for fixed PyVis layout
# ─────────────────────────────────────────────
NODE_POS = {
    "Main Gate":      (0,    200),
    "Engineering":    (300,  100),
    "Commerce":       (-300, 100),
    "Administration": (0,    0),
    "Computers & AI": (450, -150),
    "Arts":           (-450,-150),
    "Law":            (0,   -300),
}
