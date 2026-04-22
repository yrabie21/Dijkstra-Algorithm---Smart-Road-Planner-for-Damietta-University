"""
Custom CSS stylesheet for the Streamlit application.

All styles are defined here as a single constant (`APP_CSS`) and injected
once at application startup via `st.markdown(unsafe_allow_html=True)`.
"""

APP_CSS = """\
<style>
/* ── Google Font ── */
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;600;700;900&display=swap');

html, body, [class*="css"] { font-family: 'Inter', sans-serif; }

/* ── Hero banner ── */
.hero {
    background: linear-gradient(120deg, #e0e7ff, #f3e8ff);
    border: 1px solid #c7d2fe;
    border-radius: 16px;
    padding: 2rem 2.5rem;
    margin-bottom: 1.5rem;
}
.hero h1 {
    font-size: 2.4rem;
    font-weight: 900;
    color: #312e81;
    margin-bottom: 0.3rem;
}
.hero p {
    font-size: 1.05rem;
    color: #475569;
    line-height: 1.7;
    max-width: 800px;
}

/* ── Section cards ── */
.card {
    background: #ffffff;
    border: 1px solid #e2e8f0;
    border-radius: 12px;
    padding: 1.2rem 1.5rem;
    margin-bottom: 1.2rem;
    box-shadow: 0 1px 3px rgba(0,0,0,0.05);
}
.card-title {
    font-size: 1.05rem;
    font-weight: 700;
    text-transform: uppercase;
    letter-spacing: 0.05em;
    color: #4f46e5;
    margin-bottom: 0.8rem;
}

/* ── Route badge ── */
.route-badge {
    display: inline-block;
    background: #4f46e5;
    border-radius: 999px;
    padding: 0.35rem 1rem;
    font-size: 0.95rem;
    font-weight: 600;
    color: #fff;
    margin: 0 0.3rem 0.6rem 0;
}
.route-arrow { color: #f59e0b; font-weight: 900; margin: 0 0.2rem; }

/* ── iframe border ── */
iframe { border-radius: 12px; border: 1px solid #cbd5e1; }

/* ── Dataframes ── */
.stDataFrame { border-radius: 8px; overflow: hidden; }

/* ── Step visualisation ── */
.step-current {
    background: #fef3c7; border: 1px solid #fbbf24;
    border-radius: 8px; padding: 0.8rem 1.2rem; margin: 0.5rem 0;
}
.pq-entry {
    display: inline-block; background: #ede9fe; border: 1px solid #c4b5fd;
    border-radius: 8px; padding: 0.3rem 0.8rem; margin: 0.2rem;
    font-size: 0.85rem; font-weight: 600; color: #5b21b6;
}
.pq-entry.popped {
    background: #fef3c7; border-color: #f59e0b; color: #92400e;
}

/* ── Priority Queue Visual ── */
.pq-visual {
    display: flex; align-items: stretch; margin: 0.8rem 0;
    border-radius: 12px; overflow: hidden;
    border: 2px solid #c4b5fd;
    background: #f5f3ff;
}
.pq-visual-item {
    flex: 1; text-align: center; padding: 0.6rem 0.4rem;
    border-right: 1px dashed #c4b5fd;
    font-size: 0.75rem; font-weight: 600; color: #5b21b6;
    position: relative; min-width: 70px;
    transition: all 0.2s ease;
}
.pq-visual-item:last-child { border-right: none; }
.pq-visual-item .pq-dist {
    font-size: 1rem; font-weight: 800; color: #7c3aed;
    display: block; margin-top: 2px;
}
.pq-visual-item.pq-front {
    background: linear-gradient(135deg, #fef3c7, #fde68a);
    border-right: 2px solid #f59e0b;
}
.pq-visual-item.pq-front .pq-dist { color: #d97706; }
.pq-arrow-out {
    display: flex; align-items: center; padding: 0 0.5rem;
    font-size: 1.2rem; color: #f59e0b; font-weight: 900;
}

/* ── Step Navigation ── */
.step-nav {
    display: flex; align-items: center; justify-content: center;
    gap: 1rem; margin: 0.8rem 0 1.2rem;
}
.step-counter {
    background: linear-gradient(135deg, #e0e7ff, #ede9fe);
    border: 2px solid #818cf8;
    border-radius: 12px; padding: 0.6rem 1.5rem;
    font-size: 1.1rem; font-weight: 800; color: #4338ca;
    text-align: center; min-width: 180px;
}
.step-counter .step-label {
    font-size: 0.7rem; font-weight: 600; color: #6366f1;
    text-transform: uppercase; letter-spacing: 0.08em;
}
</style>
"""
