import os
import sys
import pandas as pd
import streamlit as st

# ─────────────────────────────────────────
# ENV FIX (macOS stability)
# ─────────────────────────────────────────
os.environ["TOKENIZERS_PARALLELISM"] = "false"
os.environ["OMP_NUM_THREADS"] = "1"
os.environ["PYTORCH_MPS_HIGH_WATERMARK_RATIO"] = "0.0"
os.environ["OBJC_DISABLE_INITIALIZE_FORK_SAFETY"] = "YES"

# Path fix
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# ─────────────────────────────────────────
# PAGE CONFIG
# ─────────────────────────────────────────
st.set_page_config(
    page_title="⚡ EGrid AI Supervisor",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ─────────────────────────────────────────
# CUSTOM CSS — Charcoal Black & Medium Green
# ─────────────────────────────────────────
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800;900&display=swap');

    html, body, .stApp {
        font-family: 'Inter', sans-serif;
    }

    /* Keep Streamlit icon glyphs from rendering as overlapping text labels */
    span.material-symbols-rounded,
    span.material-symbols-outlined,
    [data-testid="stSidebarCollapsedControl"] span,
    [data-testid="stExpanderToggleIcon"] span {
        font-family: "Material Symbols Rounded", "Material Symbols Outlined", sans-serif !important;
        font-style: normal;
        font-weight: 400;
        line-height: 1;
        letter-spacing: normal;
        text-transform: none;
        white-space: nowrap;
        display: inline-flex;
        align-items: center;
        justify-content: center;
        width: 1.25rem;
        overflow: hidden;
    }
    .block-container { padding-top: 2rem; padding-bottom: 2rem; }

    /* Sidebar */
    section[data-testid="stSidebar"] {
        background: linear-gradient(180deg, #0d0d14 0%, #141420 50%, #0d0d14 100%);
        border-right: 1px solid rgba(46, 204, 113, 0.15);
    }

    /* Metric Cards */
    .metric-row { display: flex; gap: 14px; margin-bottom: 20px; }
    .metric-card {
        flex: 1;
        background: linear-gradient(145deg, #1a1a2e 0%, #16162a 100%);
        border: 1px solid rgba(46, 204, 113, 0.12);
        border-radius: 12px;
        padding: 18px 14px;
        text-align: center;
        transition: all 0.3s ease;
        position: relative;
        overflow: hidden;
    }
    .metric-card::before {
        content: '';
        position: absolute;
        top: 0; left: 0; right: 0;
        height: 2px;
        background: linear-gradient(90deg, transparent, #2ecc71, transparent);
        opacity: 0.6;
    }
    .metric-card:hover {
        border-color: rgba(46, 204, 113, 0.35);
        transform: translateY(-2px);
        box-shadow: 0 8px 25px rgba(46, 204, 113, 0.08);
    }
    .metric-card .mc-icon { font-size: 1.3rem; margin-bottom: 4px; }
    .metric-card .mc-value { color: #2ecc71; font-size: 1.4rem; font-weight: 700; }
    .metric-card .mc-label {
        color: #666; font-size: 0.7rem; font-weight: 600;
        text-transform: uppercase; letter-spacing: 1px; margin-top: 4px;
    }

    /* Green Divider */
    .green-divider {
        height: 1px;
        background: linear-gradient(90deg, transparent, rgba(46, 204, 113, 0.3), transparent);
        margin: 8px 0 20px 0; border: none;
    }

    /* Section Header */
    .section-header {
        font-size: 1.1rem; font-weight: 700; color: #e0e0e0;
        letter-spacing: 0.5px; margin-bottom: 14px;
        display: flex; align-items: center; gap: 10px;
    }
    .section-header .sh-dot {
        width: 8px; height: 8px; border-radius: 50%;
        background: #2ecc71; display: inline-block;
        box-shadow: 0 0 8px rgba(46, 204, 113, 0.5);
    }

    /* Sidebar Branding */
    .sidebar-brand { text-align: center; padding: 12px 0 6px 0; }
    .sidebar-brand .sb-name {
        font-size: 1.3rem; font-weight: 800; color: #2ecc71;
        letter-spacing: 2px; text-transform: uppercase;
    }
    .sidebar-brand .sb-version { font-size: 0.7rem; color: #555; letter-spacing: 1px; margin-top: 2px; }
    .sidebar-brand .sb-line { width: 40px; height: 2px; background: #2ecc71; margin: 8px auto 0 auto; border-radius: 2px; }

    /* Sidebar Section Labels */
    .sidebar-section {
        font-size: 0.72rem; font-weight: 700; color: #2ecc71;
        text-transform: uppercase; letter-spacing: 2px;
        margin-top: 18px; margin-bottom: 8px;
        padding-bottom: 5px; border-bottom: 1px solid rgba(46, 204, 113, 0.15);
    }

    /* Welcome Card */
    .welcome-card {
        background: linear-gradient(145deg, #1a1a2e 0%, #16162a 100%);
        border: 1px solid rgba(46, 204, 113, 0.12);
        border-radius: 14px; padding: 32px 28px; text-align: center; margin-top: 12px;
    }
    .welcome-card .wc-icon { font-size: 2.8rem; margin-bottom: 10px; }
    .welcome-card .wc-title { font-size: 1.15rem; font-weight: 700; color: #e0e0e0; margin-bottom: 6px; }
    .welcome-card .wc-text { font-size: 0.88rem; color: #777; line-height: 1.6; }
    .welcome-card .wc-hint { font-size: 0.78rem; color: #2ecc71; margin-top: 14px; font-weight: 500; }

    /* Button Overrides */
    .stButton > button[kind="primary"] {
        background: linear-gradient(135deg, #2ecc71 0%, #27ae60 100%) !important;
        color: #000 !important; font-weight: 700 !important;
        letter-spacing: 1px !important; border: none !important;
        border-radius: 8px !important; transition: all 0.3s ease !important;
    }
    .stButton > button[kind="primary"]:hover {
        box-shadow: 0 4px 20px rgba(46, 204, 113, 0.3) !important;
        transform: translateY(-1px) !important;
    }
    .stDownloadButton > button {
        background: linear-gradient(135deg, #2ecc71 0%, #27ae60 100%) !important;
        color: #000 !important; font-weight: 700 !important;
        border: none !important; border-radius: 8px !important;
    }

    /* Hide Streamlit chrome */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
</style>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────
# LAZY LOADERS
# ─────────────────────────────────────────
@st.cache_resource
def load_technical_agent():
    from src.agent.graph import app
    return app

@st.cache_resource
def load_explainability_agent():
    from src.agent.explainability_agent import explainability_agent
    return explainability_agent

from src.tools.report_generator import generate_pdf

# ─────────────────────────────────────────
# HELPERS
# ─────────────────────────────────────────
CITY_COORDS = {
    "Chicago": (41.8781, -87.6298),
    "Houston": (29.7604, -95.3698),
    "New York": (40.7128, -74.0060),
    "San Francisco": (37.7749, -122.4194),
    "Los Angeles": (34.0522, -118.2437)
}

def stream_thoughts():
    st.caption(
        "AI pipeline: parsing grid conditions, running load analysis, checking policy constraints, and synthesizing recommendation."
    )

def parse_report_sections(report_text):
    """Split the explainability agent's report into sections by ## headers."""
    sections = {}
    current_key = "Overview"
    current_lines = []

    for line in report_text.split("\n"):
        if line.startswith("## "):
            if current_lines:
                sections[current_key] = "\n".join(current_lines).strip()
            current_key = line.replace("## ", "").strip()
            current_lines = []
        else:
            current_lines.append(line)

    if current_lines:
        sections[current_key] = "\n".join(current_lines).strip()

    return sections


# ─────────────────────────────────────────
# MAIN APP
# ─────────────────────────────────────────
def main():

    # ───── SIDEBAR ─────
    with st.sidebar:
        st.markdown("""
            <div class="sidebar-brand">
                <div style="font-size: 2rem;">⚡</div>
                <div class="sb-name">EGrid</div>
                <div class="sb-version">AI Supervisor · v2.0</div>
                <div class="sb-line"></div>
            </div>
        """, unsafe_allow_html=True)

        st.markdown('<div class="sidebar-section">📋 Analysis Query</div>', unsafe_allow_html=True)
        task = st.text_area(
            "Describe your task",
            placeholder="e.g., Should we expand Level 3 chargers in downtown Houston?",
            height=90,
            label_visibility="collapsed"
        )

        st.markdown('<div class="sidebar-section">📡 Grid Telemetry</div>', unsafe_allow_html=True)
        city = st.selectbox("Substation Location", list(CITY_COORDS.keys()))

        c1, c2 = st.columns(2)
        with c1:
            temp = st.slider("Temp (°C)", -20, 50, 25)
        with c2:
            hour = st.slider("Hour", 0, 23, 12)

        day = st.selectbox("Day of Week", ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"])

        st.markdown('<div class="sidebar-section">🧪 Simulation Engine</div>', unsafe_allow_html=True)
        run_simulation = st.checkbox("Enable 24-Hour Stress Test")

        load_multiplier = 1.0
        temp_increase = 0.0
        if run_simulation:
            load_multiplier = st.slider("Load Multiplier (x)", 1.0, 3.0, 1.5, 0.1)
            temp_increase = st.slider("Warming Spike (°C)", 0.0, 20.0, 5.0, 1.0)

        st.markdown("<br>", unsafe_allow_html=True)
        analyze_btn = st.button("🚀  INITIATE ANALYSIS", type="primary", use_container_width=True)


    # ───── HEADER ─────
    st.markdown("""
        <div style="display:flex; align-items:center; gap:12px; margin-bottom:2px;">
            <span style="font-size:2.2rem;">⚡</span>
            <span style="font-size:1.8rem; font-weight:800; letter-spacing:1.5px;
                background: linear-gradient(135deg, #2ecc71, #27ae60, #1abc9c);
                -webkit-background-clip: text; -webkit-text-fill-color: transparent;
                text-transform: uppercase;">EGrid Supervisor</span>
        </div>
        <div style="color:#666; font-size:0.9rem; margin-bottom:20px;">
            Autonomous EV Infrastructure & Grid Stability Intelligence
        </div>
    """, unsafe_allow_html=True)

    # ───── METRIC CARDS ─────
    sim_status = "⚠️ STRESS TEST" if run_simulation else "● STABLE"
    sim_color = "#ff9900" if run_simulation else "#2ecc71"

    st.markdown(f"""
        <div class="metric-row">
            <div class="metric-card">
                <div class="mc-icon">📍</div>
                <div class="mc-value">{city}</div>
                <div class="mc-label">Active Substation</div>
            </div>
            <div class="metric-card">
                <div class="mc-icon">🌡️</div>
                <div class="mc-value">{temp}°C</div>
                <div class="mc-label">Ambient Temp</div>
            </div>
            <div class="metric-card">
                <div class="mc-icon">🕐</div>
                <div class="mc-value">{hour:02d}:00</div>
                <div class="mc-label">Grid Time</div>
            </div>
            <div class="metric-card">
                <div class="mc-icon">📊</div>
                <div class="mc-value" style="color:{sim_color}; font-size:1rem;">{sim_status}</div>
                <div class="mc-label">Node Status</div>
            </div>
        </div>
    """, unsafe_allow_html=True)

    st.markdown('<div class="green-divider"></div>', unsafe_allow_html=True)

    # ───── LOCATION MAP ─────
    st.markdown('<div class="section-header"><span class="sh-dot"></span> Location Intelligence</div>', unsafe_allow_html=True)
    lat, lon = CITY_COORDS[city]
    st.map(pd.DataFrame({"lat": [lat], "lon": [lon]}), zoom=10)

    st.markdown('<div class="green-divider"></div>', unsafe_allow_html=True)

    # ───── ANALYSIS ─────
    if analyze_btn:
        if not task:
            st.warning("⚠️ Please describe your analysis task in the sidebar.")
            return

        st.markdown('<div class="section-header"><span class="sh-dot"></span> AI Processing</div>', unsafe_allow_html=True)
        stream_thoughts()

        # ── Phase 1: Technical Agent ──
        st.markdown("### 🧠 Technical Agent")

        tech_prompt = (
            f"Task: {task}\n"
            f"Context: Location: {city}, Temperature: {temp}°C, Time: {hour}:00, Day: {day}\n\n"
            f"You MUST address ALL of the following in your response:\n"
            f"1. INFRASTRUCTURE & LOAD DIAGNOSIS — use station_load_analyst tool\n"
            f"2. OPTIMAL CHARGER PLACEMENT & SITING — Level 2 vs Level 3, use policy_researcher tool\n"
            f"3. SCHEDULING & OPERATIONAL INSIGHTS — peak shifting recommendations\n"
            f"4. FINAL EXPANSION MANDATE — definitive recommendation with Protocol IDs"
        )

        if run_simulation:
            tech_prompt += (
                f"\n\n[USER COMMAND: You MUST run a scenario simulation using the "
                f"scenario_simulator tool with load_multiplier={load_multiplier} and "
                f"temp_increase={temp_increase}. Analyze the 24-hour grid stability.]"
            )

        st.info("Fetching RAG policies and ML predictions...")
        with st.spinner("Analyzing infrastructure & protocols..."):
            try:
                tech_response = load_technical_agent().invoke({"messages": [("user", tech_prompt)]})
                tech_output = tech_response["messages"][-1].content
            except Exception as e:
                st.error(f"Critical Node Failure: {e}")
                return
        st.success("Technical analysis completed.")

        st.markdown("<br>", unsafe_allow_html=True)

        # ── Technical Output (collapsible) ──
        with st.expander("🔍 View Raw Technical Supervisor Output", expanded=False):
            st.markdown(tech_output)

        st.markdown('<div class="green-divider"></div>', unsafe_allow_html=True)

        st.markdown("### 📊 Investment Memo Generator")

        explain_prompt = f"Convert the following technical analysis into a structured investor-grade report:\n\n{tech_output}"

        st.info("Structuring financial and risk profiles...")
        with st.spinner("Generating report..."):
            try:
                explain_response = load_explainability_agent().invoke({"messages": [("user", explain_prompt)]})
                final_report = explain_response["messages"][-1].content
            except Exception as e:
                st.error(f"Reporting Pipeline Failure: {e}")
                return
        st.success("Investment memo generated.")

        # ── Tabbed Report Display ──
        st.markdown('<div class="section-header"><span class="sh-dot"></span> Investment Memorandum</div>', unsafe_allow_html=True)

        sections = parse_report_sections(final_report)

        # Build tab names from the parsed sections
        tab_names = list(sections.keys())
        if tab_names:
            tabs = st.tabs(tab_names)
            for tab, key in zip(tabs, tab_names):
                with tab:
                    st.markdown(sections[key])
        else:
            # Fallback: show the full report if parsing found no sections
            with st.container():
                st.markdown(final_report)

        st.markdown('<div class="green-divider"></div>', unsafe_allow_html=True)

        # ── PDF Export ──
        pdf_filename = generate_pdf(final_report, filename="EGrid_Investment_Memo.pdf")
        with open(pdf_filename, "rb") as pdf_file:
            st.download_button(
                label="📥  EXPORT PDF MEMORANDUM",
                data=pdf_file,
                file_name=pdf_filename,
                mime="application/pdf",
                use_container_width=True
            )

        # ── AI Trace ──
        with st.expander("🧠 Full AI Trace"):
            st.code(tech_output, language="markdown")

    else:
        st.markdown("""
            <div class="welcome-card">
                <div class="wc-icon">🔋</div>
                <div class="wc-title">Ready to Analyze</div>
                <div class="wc-text">
                    Configure your grid parameters and describe your infrastructure task in the
                    sidebar, then click <strong>INITIATE ANALYSIS</strong> to deploy the AI Supervisor.
                </div>
                <div class="wc-hint">⚡ Powered by LangGraph + XGBoost + RAG</div>
            </div>
        """, unsafe_allow_html=True)


if __name__ == "__main__":
    main()