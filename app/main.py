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
    @import url('https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;500;600;700;800&family=Inter:wght@300;400;500;600;700&display=swap');

    :root {
        --primary: #00ffcc;
        --primary-glow: rgba(0, 255, 204, 0.4);
        --secondary: #7b2cbf;
        --bg-color: #050508;
        --card-bg: rgba(15, 15, 25, 0.6);
        --card-border: rgba(255, 255, 255, 0.08);
        --text-main: #f0f0f5;
        --text-muted: #9aa0a6;
    }

    html, body, .stApp {
        font-family: 'Inter', sans-serif;
        background-color: var(--bg-color);
        color: var(--text-main);
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
        background: rgba(10, 10, 15, 0.8) !important;
        backdrop-filter: blur(20px);
        -webkit-backdrop-filter: blur(20px);
        border-right: 1px solid var(--card-border);
    }
    section[data-testid="stSidebar"] .stMarkdown {
        color: var(--text-main);
    }

    /* Metric Cards - Glassmorphism */
    .metric-row { display: flex; gap: 20px; margin-bottom: 24px; flex-wrap: wrap; }
    .metric-card {
        flex: 1;
        min-width: 150px;
        background: var(--card-bg);
        backdrop-filter: blur(12px);
        -webkit-backdrop-filter: blur(12px);
        border: 1px solid var(--card-border);
        border-radius: 16px;
        padding: 24px 16px;
        text-align: center;
        transition: all 0.4s cubic-bezier(0.175, 0.885, 0.32, 1.275);
        position: relative;
        overflow: hidden;
        box-shadow: 0 4px 30px rgba(0, 0, 0, 0.1);
    }
    .metric-card::before {
        content: '';
        position: absolute;
        top: 0; left: 0; width: 100%; height: 100%;
        background: linear-gradient(135deg, rgba(255,255,255,0.05) 0%, transparent 100%);
        pointer-events: none;
    }
    .metric-card:hover {
        transform: translateY(-5px);
        border-color: var(--primary);
        box-shadow: 0 8px 30px var(--primary-glow);
    }
    .metric-card .mc-icon { 
        font-size: 1.8rem; margin-bottom: 8px; 
        display: inline-block;
        filter: drop-shadow(0 0 8px rgba(255,255,255,0.2));
    }
    .metric-card .mc-value { 
        color: var(--text-main); font-size: 1.6rem; font-weight: 800; font-family: 'Outfit', sans-serif; 
        text-shadow: 0 0 10px rgba(255,255,255,0.1);
    }
    .metric-card .mc-label {
        color: var(--primary); font-size: 0.75rem; font-weight: 600;
        text-transform: uppercase; letter-spacing: 1.5px; margin-top: 6px;
    }

    /* Neon Divider */
    .green-divider {
        height: 1px;
        background: linear-gradient(90deg, transparent, var(--primary), transparent);
        margin: 24px 0 32px 0; border: none;
        opacity: 0.5;
        box-shadow: 0 0 10px var(--primary);
    }

    /* Section Header */
    .section-header {
        font-family: 'Outfit', sans-serif;
        font-size: 1.3rem; font-weight: 700; color: #fff;
        letter-spacing: 0.5px; margin-bottom: 20px;
        display: flex; align-items: center; gap: 12px;
    }
    .section-header .sh-dot {
        width: 10px; height: 10px; border-radius: 50%;
        background: var(--primary); display: inline-block;
        box-shadow: 0 0 12px var(--primary);
        animation: pulse 2s infinite;
    }
    
    @keyframes pulse {
        0% { box-shadow: 0 0 0 0 var(--primary-glow); }
        70% { box-shadow: 0 0 0 10px rgba(0, 255, 204, 0); }
        100% { box-shadow: 0 0 0 0 rgba(0, 255, 204, 0); }
    }

    /* Sidebar Branding */
    .sidebar-brand { text-align: center; padding: 20px 0 10px 0; }
    .sidebar-brand .sb-icon { font-size: 2.5rem; filter: drop-shadow(0 0 15px var(--primary)); margin-bottom: 5px; }
    .sidebar-brand .sb-name {
        font-size: 1.8rem; font-weight: 900; color: #fff;
        letter-spacing: 3px; text-transform: uppercase;
        background: linear-gradient(135deg, #fff, var(--primary));
        -webkit-background-clip: text; -webkit-text-fill-color: transparent;
    }
    .sidebar-brand .sb-version { font-size: 0.75rem; color: var(--text-muted); letter-spacing: 2px; margin-top: 4px; }

    /* Sidebar Section Labels */
    .sidebar-section {
        font-size: 0.75rem; font-weight: 700; color: var(--primary);
        text-transform: uppercase; letter-spacing: 2px;
        margin-top: 24px; margin-bottom: 12px;
        display: flex; align-items: center; gap: 8px;
    }
    .sidebar-section::after {
        content: ''; flex-grow: 1; height: 1px;
        background: linear-gradient(90deg, var(--card-border), transparent);
    }

    /* Welcome Card */
    .welcome-card {
        background: var(--card-bg);
        backdrop-filter: blur(16px);
        -webkit-backdrop-filter: blur(16px);
        border: 1px solid var(--card-border);
        border-radius: 20px; padding: 40px 30px; text-align: center; margin-top: 20px;
        box-shadow: 0 10px 40px rgba(0,0,0,0.2);
        animation: float 6s ease-in-out infinite;
    }
    @keyframes float {
        0% { transform: translateY(0px); }
        50% { transform: translateY(-10px); }
        100% { transform: translateY(0px); }
    }
    .welcome-card .wc-icon { font-size: 3.5rem; margin-bottom: 16px; filter: drop-shadow(0 0 20px rgba(255,255,255,0.2)); }
    .welcome-card .wc-title { font-size: 1.4rem; font-weight: 800; color: #fff; margin-bottom: 12px; letter-spacing: 1px; }
    .welcome-card .wc-text { font-size: 0.95rem; color: var(--text-muted); line-height: 1.7; }
    .welcome-card .wc-hint { 
        display: inline-block;
        padding: 6px 12px; background: rgba(0, 255, 204, 0.1); border-radius: 20px;
        border: 1px solid rgba(0, 255, 204, 0.2);
        font-size: 0.8rem; color: var(--primary); margin-top: 20px; font-weight: 600; 
    }

    /* Button Overrides */
    .stButton > button[kind="primary"] {
        background: rgba(0, 255, 204, 0.05) !important;
        color: var(--primary) !important;
        font-weight: 800 !important; font-family: 'Outfit', sans-serif !important;
        letter-spacing: 2px !important;
        border: 1px solid var(--primary) !important;
        border-radius: 8px !important;
        transition: all 0.3s ease !important;
        text-transform: uppercase;
        box-shadow: 0 0 15px rgba(0, 255, 204, 0.1), inset 0 0 10px rgba(0, 255, 204, 0.05) !important;
        min-height: 54px !important;
    }
    .stButton > button[kind="primary"] p {
        color: inherit !important;
    }
    .stButton > button[kind="primary"]:hover {
        background: var(--primary) !important;
        color: #050508 !important;
        box-shadow: 0 0 25px rgba(0, 255, 204, 0.5), inset 0 0 15px rgba(255, 255, 255, 0.5) !important;
        transform: translateY(-2px) !important;
    }
    .stDownloadButton > button {
        background: rgba(0, 255, 204, 0.05) !important;
        color: var(--primary) !important;
        font-weight: 700 !important; font-family: 'Outfit', sans-serif !important;
        border: 1px solid var(--primary) !important;
        border-radius: 8px !important;
        text-transform: uppercase; letter-spacing: 1.5px !important;
        transition: all 0.3s ease !important;
        min-height: 50px !important;
    }
    .stDownloadButton > button p {
        color: inherit !important;
    }
    .stDownloadButton > button:hover {
        background: var(--primary) !important;
        color: #050508 !important;
        box-shadow: 0 0 20px rgba(0, 255, 204, 0.4) !important;
    }
    
    /* Inputs Styling */
    .stTextInput > div > div > input, .stTextArea > div > div > textarea, .stSelectbox > div > div > div {
        background-color: rgba(0,0,0,0.2) !important;
        border: 1px solid var(--card-border) !important;
        border-radius: 8px !important;
        color: #fff !important;
    }
    .stTextInput > div > div > input:focus, .stTextArea > div > div > textarea:focus {
        border-color: var(--primary) !important;
        box-shadow: 0 0 0 1px var(--primary) !important;
    }
    
    /* Expander Styling */
    .streamlit-expanderHeader {
        background-color: var(--card-bg) !important;
        border-radius: 8px !important;
        border: 1px solid var(--card-border) !important;
        font-weight: 600 !important;
        color: #fff !important;
    }
    
    /* Status Box */
    [data-testid="stStatusWidget"] {
        background-color: var(--card-bg) !important;
        border: 1px solid var(--card-border) !important;
        border-radius: 12px !important;
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
                <div class="sb-icon">⚡</div>
                <div class="sb-name">EGrid</div>
                <div class="sb-version">AI Supervisor · v3.0</div>
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
        <div style="display:flex; align-items:center; gap:16px; margin-bottom:10px;">
            <div style="font-size:2.8rem; filter: drop-shadow(0 0 10px rgba(0,255,204,0.5));">⚡</div>
            <div>
                <div style="font-size:2.4rem; font-weight:900; font-family:'Outfit', sans-serif; letter-spacing:2px;
                    background: linear-gradient(135deg, #ffffff, var(--primary));
                    -webkit-background-clip: text; -webkit-text-fill-color: transparent;
                    text-transform: uppercase; line-height: 1.2;">EGrid Supervisor</div>
                <div style="color:var(--text-muted); font-size:1rem; font-weight:500;">
                    Autonomous EV Infrastructure & Grid Stability Intelligence
                </div>
            </div>
        </div>
    """, unsafe_allow_html=True)

    # ───── METRIC CARDS ─────
    sim_status = "STRESS TEST" if run_simulation else "SYSTEM STABLE"
    sim_color = "#ff3366" if run_simulation else "var(--primary)"
    sim_icon = "⚠️" if run_simulation else "🟢"
    card_border_style = f"border-color: {sim_color}; box-shadow: inset 0 0 20px rgba(255, 51, 102, 0.1);" if run_simulation else ""

    st.markdown(f"""
        <div class="metric-row">
            <div class="metric-card">
                <div class="mc-icon">📍</div>
                <div class="mc-value">{city}</div>
                <div class="mc-label">Active Node</div>
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
            <div class="metric-card" style="{card_border_style}">
                <div class="mc-icon">{sim_icon}</div>
                <div class="mc-value" style="color:{sim_color}; font-size:1.2rem;">{sim_status}</div>
                <div class="mc-label">System State</div>
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
                <div class="wc-icon">🌐</div>
                <div class="wc-title">System Standby</div>
                <div class="wc-text">
                    Configure telemetry parameters and specify your infrastructure objective in the
                    control panel. Initialize analysis to deploy the AI Supervisor network.
                </div>
                <div class="wc-hint">✨ Powered by LangGraph • XGBoost • RAG</div>
            </div>
        """, unsafe_allow_html=True)


if __name__ == "__main__":
    main()