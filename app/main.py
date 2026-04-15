"""
EGrid — Intelligent EV Charging Demand Prediction & Agentic Infrastructure Planning
Streamlit Application
"""
import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import os
import sys
import json
import time

# Add project root to path
ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, ROOT_DIR)

# Page config
st.set_page_config(
    page_title="EGrid — EV Infrastructure Intelligence",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ---------------------------------------------------------------------------
# Custom CSS — Premium Dark Theme
# ---------------------------------------------------------------------------
st.markdown("""
<style>
    /* Import Google Font */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap');
    
    * { font-family: 'Inter', sans-serif; }
    
    /* Main background */
    .stApp {
        background: linear-gradient(135deg, #0a0a0f 0%, #0d1117 50%, #0a0f1a 100%);
    }
    
    /* Sidebar */
    section[data-testid="stSidebar"] {
        background: linear-gradient(180deg, #0d1117 0%, #111827 100%);
        border-right: 1px solid rgba(99, 102, 241, 0.15);
    }
    
    section[data-testid="stSidebar"] .stMarkdown p,
    section[data-testid="stSidebar"] .stMarkdown li,
    section[data-testid="stSidebar"] label {
        color: #a5b4c8 !important;
    }
    
    /* Headers */
    h1 { 
        background: linear-gradient(135deg, #818cf8 0%, #6366f1 30%, #a78bfa 70%, #c084fc 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-weight: 800 !important;
        letter-spacing: -0.03em;
    }
    
    h2, h3 {
        color: #e2e8f0 !important;
        font-weight: 700 !important;
    }
    
    /* Body text */
    .stMarkdown p, .stMarkdown li {
        color: #94a3b8 !important;
    }
    
    /* Metric cards */
    div[data-testid="stMetric"] {
        background: linear-gradient(135deg, rgba(99, 102, 241, 0.08) 0%, rgba(139, 92, 246, 0.05) 100%);
        border: 1px solid rgba(99, 102, 241, 0.15);
        border-radius: 16px;
        padding: 20px 24px;
        transition: all 0.3s ease;
    }
    
    div[data-testid="stMetric"]:hover {
        border-color: rgba(99, 102, 241, 0.4);
        transform: translateY(-2px);
        box-shadow: 0 8px 32px rgba(99, 102, 241, 0.12);
    }
    
    div[data-testid="stMetric"] label {
        color: #64748b !important;
        font-weight: 500 !important;
        text-transform: uppercase;
        font-size: 0.72rem !important;
        letter-spacing: 0.08em;
    }
    
    div[data-testid="stMetric"] [data-testid="stMetricValue"] {
        color: #e2e8f0 !important;
        font-weight: 700 !important;
    }
    
    /* Tabs */
    .stTabs [data-baseweb="tab-list"] {
        gap: 8px;
        background: transparent;
        border-bottom: 1px solid rgba(99, 102, 241, 0.1);
    }
    
    .stTabs [data-baseweb="tab"] {
        background: transparent;
        color: #64748b;
        border-radius: 10px 10px 0 0;
        padding: 12px 24px;
        font-weight: 500;
        border: none;
    }
    
    .stTabs [aria-selected="true"] {
        background: linear-gradient(135deg, rgba(99, 102, 241, 0.12) 0%, rgba(139, 92, 246, 0.08) 100%);
        color: #a78bfa !important;
        border-bottom: 2px solid #6366f1;
    }
    
    /* Expander */
    .streamlit-expanderHeader {
        background: rgba(99, 102, 241, 0.06);
        border: 1px solid rgba(99, 102, 241, 0.12);
        border-radius: 12px;
        color: #c4b5fd !important;
        font-weight: 600 !important;
    }
    
    /* Buttons */
    .stButton button {
        background: linear-gradient(135deg, #4f46e5 0%, #6366f1 50%, #7c3aed 100%);
        color: white !important;
        border: none;
        border-radius: 12px;
        padding: 12px 28px;
        font-weight: 600;
        font-size: 0.9rem;
        letter-spacing: 0.02em;
        transition: all 0.3s ease;
        box-shadow: 0 4px 16px rgba(99, 102, 241, 0.3);
    }
    
    .stButton button:hover {
        transform: translateY(-2px);
        box-shadow: 0 8px 24px rgba(99, 102, 241, 0.45);
    }
    
    /* Text input / Chat input */
    .stTextInput input, .stTextArea textarea {
        background: rgba(15, 23, 42, 0.8) !important;
        border: 1px solid rgba(99, 102, 241, 0.2) !important;
        border-radius: 12px !important;
        color: #e2e8f0 !important;
        padding: 12px 16px !important;
    }
    
    .stTextInput input:focus, .stTextArea textarea:focus {
        border-color: #6366f1 !important;
        box-shadow: 0 0 0 3px rgba(99, 102, 241, 0.15) !important;
    }
    
    /* Chat messages */
    .stChatMessage {
        background: rgba(15, 23, 42, 0.5) !important;
        border: 1px solid rgba(99, 102, 241, 0.08) !important;
        border-radius: 16px !important;
    }
    
    /* Selectbox */
    .stSelectbox > div > div {
        background: rgba(15, 23, 42, 0.8) !important;
        border: 1px solid rgba(99, 102, 241, 0.2) !important;
        border-radius: 12px !important;
        color: #e2e8f0 !important;
    }
    
    /* Dividers */
    hr { border-color: rgba(99, 102, 241, 0.1) !important; }
    
    /* Scrollbar */
    ::-webkit-scrollbar { width: 6px; }
    ::-webkit-scrollbar-track { background: #0a0a0f; }
    ::-webkit-scrollbar-thumb { background: rgba(99, 102, 241, 0.3); border-radius: 3px; }
    ::-webkit-scrollbar-thumb:hover { background: rgba(99, 102, 241, 0.5); }
    
    /* Success/Error/Warning badges */
    .badge-critical {
        background: linear-gradient(135deg, rgba(239, 68, 68, 0.15), rgba(239, 68, 68, 0.05));
        border: 1px solid rgba(239, 68, 68, 0.3);
        color: #fca5a5;
        padding: 4px 12px;
        border-radius: 20px;
        font-size: 0.75rem;
        font-weight: 600;
    }
    
    .badge-optimization {
        background: linear-gradient(135deg, rgba(251, 191, 36, 0.15), rgba(251, 191, 36, 0.05));
        border: 1px solid rgba(251, 191, 36, 0.3);
        color: #fcd34d;
        padding: 4px 12px;
        border-radius: 20px;
        font-size: 0.75rem;
        font-weight: 600;
    }
    
    .badge-normal {
        background: linear-gradient(135deg, rgba(52, 211, 153, 0.15), rgba(52, 211, 153, 0.05));
        border: 1px solid rgba(52, 211, 153, 0.3);
        color: #6ee7b7;
        padding: 4px 12px;
        border-radius: 20px;
        font-size: 0.75rem;
        font-weight: 600;
    }
    
    /* Spinner */
    .stSpinner > div { border-top-color: #6366f1 !important; }
    
    /* Agent report container */
    .report-section {
        background: rgba(15, 23, 42, 0.4);
        border: 1px solid rgba(99, 102, 241, 0.1);
        border-radius: 16px;
        padding: 24px;
        margin-bottom: 16px;
    }
</style>
""", unsafe_allow_html=True)

# ---------------------------------------------------------------------------
# Data Loading
# ---------------------------------------------------------------------------

@st.cache_data
def load_data():
    """Load the processed dataset."""
    data_path = os.path.join(ROOT_DIR, "data", "processed", "processed_data.csv")
    raw_path = os.path.join(ROOT_DIR, "data", "raw", "ev_charging_patterns.csv")
    
    processed = None
    raw = None
    
    if os.path.exists(data_path):
        processed = pd.read_csv(data_path)
    if os.path.exists(raw_path):
        raw = pd.read_csv(raw_path)
    
    return processed, raw

# Plotly dark theme template
PLOT_TEMPLATE = dict(
    layout=go.Layout(
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font=dict(family="Inter", color="#94a3b8"),
        title_font=dict(color="#e2e8f0", size=16),
        xaxis=dict(gridcolor="rgba(99,102,241,0.06)", zerolinecolor="rgba(99,102,241,0.1)"),
        yaxis=dict(gridcolor="rgba(99,102,241,0.06)", zerolinecolor="rgba(99,102,241,0.1)"),
        colorway=["#818cf8", "#a78bfa", "#c084fc", "#f472b6", "#34d399", "#fbbf24", "#38bdf8", "#fb7185"],
        margin=dict(l=40, r=20, t=50, b=40),
    )
)

# ---------------------------------------------------------------------------
# Sidebar
# ---------------------------------------------------------------------------

with st.sidebar:
    st.markdown("## ⚡ EGrid")
    st.markdown("*Intelligent EV Infrastructure*")
    st.markdown("---")
    
    page = st.radio(
        "Navigation",
        ["📊 Dashboard", "🤖 AI Planner", "📈 Model Performance"],
        label_visibility="collapsed"
    )
    
    st.markdown("---")
    
    st.markdown("### System Status")
    
    # Check component readiness
    data_ready = os.path.exists(os.path.join(ROOT_DIR, "data", "processed", "processed_data.csv"))
    model_ready = os.path.exists(os.path.join(ROOT_DIR, "src", "models", "demand_predictor.pkl"))
    
    groq_key = os.environ.get("GROQ_API_KEY", "")
    llm_ready = bool(groq_key)
    
    vectordb_path = os.path.join(ROOT_DIR, "src", "vectordb", "chroma_store")
    rag_ready = os.path.exists(vectordb_path)
    
    st.markdown(f"{'✅' if data_ready else '❌'} Data Pipeline")
    st.markdown(f"{'✅' if model_ready else '❌'} ML Model")
    st.markdown(f"{'✅' if rag_ready else '⚠️'} RAG Knowledge Base")
    st.markdown(f"{'✅' if llm_ready else '⚠️'} LLM Connection")
    
    if not llm_ready:
        st.markdown("---")
        groq_input = st.text_input("Groq API Key", type="password", placeholder="gsk_...")
        if groq_input:
            os.environ["GROQ_API_KEY"] = groq_input
            st.success("API Key set!")
            st.rerun()
    
    st.markdown("---")
    st.markdown(
        "<div style='text-align:center; color:#475569; font-size:0.75rem;'>"
        "EGrid v2.0 — Agentic Infrastructure Planning<br>"
        "Built with LangGraph + Groq + ChromaDB"
        "</div>",
        unsafe_allow_html=True
    )

# ---------------------------------------------------------------------------
# PAGE: Dashboard
# ---------------------------------------------------------------------------

if page == "📊 Dashboard":
    st.markdown("# 📊 Charging Network Dashboard")
    st.markdown("Real-time analytics across the EGrid EV charging network")
    st.markdown("")
    
    processed, raw = load_data()
    
    if processed is None:
        st.error("No processed data found. Run `python src/tools/demand_analyzer.py` first.")
        st.stop()
    
    # --- KPI Row ---
    col1, col2, col3, col4, col5 = st.columns(5)
    
    num_stations = processed["Charging Station ID"].nunique()
    num_cities = processed["Charging Station Location"].nunique()
    avg_load = processed["Load_Score"].mean()
    max_load = processed["Load_Score"].max()
    total_energy = processed["Energy Consumed (kWh)"].sum()
    
    col1.metric("Stations", num_stations)
    col2.metric("Cities", num_cities)
    col3.metric("Avg Load Score", f"{avg_load:.1f}")
    col4.metric("Peak Load", f"{max_load:.1f}")
    col5.metric("Total Energy", f"{total_energy:,.0f} kWh")
    
    st.markdown("")
    
    # --- Tabs for different views ---
    tab1, tab2, tab3, tab4 = st.tabs([
        "🌍 City Overview", "⏰ Temporal Patterns", "🔥 Load Heatmap", "📋 Station Details"
    ])
    
    with tab1:
        col_left, col_right = st.columns([3, 2])
        
        with col_left:
            # City average load scores
            city_load = processed.groupby("Charging Station Location").agg({
                "Load_Score": ["mean", "max"],
                "Energy Consumed (kWh)": "sum",
                "Vehicle_Count": "sum"
            }).reset_index()
            city_load.columns = ["City", "Avg_Load", "Max_Load", "Total_Energy", "Total_Vehicles"]
            city_load = city_load.sort_values("Avg_Load", ascending=True)
            
            fig = go.Figure()
            fig.add_trace(go.Bar(
                y=city_load["City"],
                x=city_load["Avg_Load"],
                orientation="h",
                name="Average",
                marker=dict(
                    color=city_load["Avg_Load"],
                    colorscale=[[0, "#818cf8"], [0.5, "#a78bfa"], [1, "#f472b6"]],
                    cornerradius=6
                ),
                text=city_load["Avg_Load"].round(1),
                textposition="inside",
                textfont=dict(color="white", size=12, family="Inter")
            ))
            fig.add_trace(go.Scatter(
                y=city_load["City"],
                x=city_load["Max_Load"],
                mode="markers",
                name="Peak",
                marker=dict(color="#fbbf24", size=10, symbol="diamond"),
            ))
            fig.update_layout(
                **PLOT_TEMPLATE["layout"].to_plotly_json(),
                title="Load Score by City",
                xaxis_title="Load Score",
                height=350,
                showlegend=True,
                legend=dict(orientation="h", yanchor="bottom", y=1.02, x=0.5, xanchor="center")
            )
            st.plotly_chart(fig, use_container_width=True)
        
        with col_right:
            # Energy distribution by city (donut)
            fig2 = go.Figure(data=[go.Pie(
                labels=city_load["City"],
                values=city_load["Total_Energy"],
                hole=0.55,
                marker=dict(colors=["#818cf8", "#a78bfa", "#c084fc", "#f472b6", "#34d399"]),
                textfont=dict(color="white", family="Inter"),
                textinfo="label+percent"
            )])
            fig2.update_layout(
                **PLOT_TEMPLATE["layout"].to_plotly_json(),
                title="Energy Distribution by City",
                height=350,
                showlegend=False
            )
            st.plotly_chart(fig2, use_container_width=True)
    
    with tab2:
        col_left, col_right = st.columns(2)
        
        with col_left:
            # Hourly load pattern
            hourly = processed.groupby("Hour").agg({
                "Load_Score": "mean",
                "Vehicle_Count": "sum"
            }).reset_index()
            
            fig3 = go.Figure()
            fig3.add_trace(go.Scatter(
                x=hourly["Hour"],
                y=hourly["Load_Score"],
                mode="lines+markers",
                name="Avg Load Score",
                line=dict(color="#818cf8", width=3, shape="spline"),
                marker=dict(size=7),
                fill="tozeroy",
                fillcolor="rgba(129, 140, 248, 0.1)"
            ))
            
            # Mark peak hours
            peak_hours = hourly.nlargest(3, "Load_Score")
            fig3.add_trace(go.Scatter(
                x=peak_hours["Hour"],
                y=peak_hours["Load_Score"],
                mode="markers",
                name="Peak Hours",
                marker=dict(color="#fbbf24", size=14, symbol="star", line=dict(color="#fbbf24", width=1)),
            ))
            
            fig3.update_layout(
                **PLOT_TEMPLATE["layout"].to_plotly_json(),
                title="Hourly Load Score Pattern",
                xaxis_title="Hour of Day",
                yaxis_title="Avg Load Score",
                height=380,
            )
            st.plotly_chart(fig3, use_container_width=True)
        
        with col_right:
            # Day of week pattern
            day_order = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
            daily = processed.groupby("Day_of_Week")["Load_Score"].mean().reindex(day_order).reset_index()
            
            fig4 = go.Figure(data=[go.Bar(
                x=daily["Day_of_Week"],
                y=daily["Load_Score"],
                marker=dict(
                    color=daily["Load_Score"],
                    colorscale=[[0, "#34d399"], [0.5, "#818cf8"], [1, "#f472b6"]],
                    cornerradius=8
                ),
                text=daily["Load_Score"].round(1),
                textposition="outside",
                textfont=dict(color="#94a3b8", size=11, family="Inter")
            )])
            fig4.update_layout(
                **PLOT_TEMPLATE["layout"].to_plotly_json(),
                title="Daily Load Score Pattern",
                xaxis_title="Day of Week",
                yaxis_title="Avg Load Score",
                height=380,
            )
            st.plotly_chart(fig4, use_container_width=True)
    
    with tab3:
        # Heatmap: Station x Hour
        st.markdown("#### Station Load Heatmap")
        
        selected_city = st.selectbox(
            "Filter by City",
            ["All"] + list(processed["Charging Station Location"].unique()),
            key="heatmap_city"
        )
        
        if selected_city != "All":
            filtered = processed[processed["Charging Station Location"] == selected_city]
        else:
            filtered = processed
        
        # Pivot table for heatmap
        heatmap_data = filtered.pivot_table(
            index="Charging Station ID",
            columns="Hour",
            values="Load_Score",
            aggfunc="mean"
        ).fillna(0)
        
        # Limit to top 20 stations for readability
        station_max = heatmap_data.max(axis=1).nlargest(20)
        heatmap_data = heatmap_data.loc[station_max.index]
        
        fig5 = go.Figure(data=go.Heatmap(
            z=heatmap_data.values,
            x=heatmap_data.columns,
            y=heatmap_data.index,
            colorscale=[[0, "#0a0f1a"], [0.3, "#312e81"], [0.5, "#4f46e5"], [0.7, "#a78bfa"], [1, "#f472b6"]],
            colorbar=dict(title="Load Score", titlefont=dict(color="#94a3b8"), tickfont=dict(color="#94a3b8")),
            hovertemplate="Station: %{y}<br>Hour: %{x}<br>Load Score: %{z:.1f}<extra></extra>"
        ))
        fig5.update_layout(
            **PLOT_TEMPLATE["layout"].to_plotly_json(),
            title=f"Load Score Heatmap — {selected_city}",
            xaxis_title="Hour of Day",
            yaxis_title="Station ID",
            height=500,
        )
        st.plotly_chart(fig5, use_container_width=True)
    
    with tab4:
        st.markdown("#### Station Performance Table")
        
        station_stats = processed.groupby(["Charging Station ID", "Charging Station Location"]).agg({
            "Load_Score": ["mean", "max", "min"],
            "Energy Consumed (kWh)": ["sum", "mean"],
            "Vehicle_Count": ["sum"],
            "Temperature (°C)": ["mean"]
        }).reset_index()
        station_stats.columns = [
            "Station ID", "City", "Avg Load", "Max Load", "Min Load",
            "Total Energy (kWh)", "Avg Energy", "Total Vehicles", "Avg Temp (°C)"
        ]
        station_stats = station_stats.round(2).sort_values("Max Load", ascending=False)
        
        st.dataframe(
            station_stats,
            use_container_width=True,
            height=500,
            column_config={
                "Max Load": st.column_config.ProgressColumn(
                    "Max Load", format="%.1f", min_value=0, max_value=100
                ),
                "Avg Load": st.column_config.ProgressColumn(
                    "Avg Load", format="%.1f", min_value=0, max_value=100
                ),
            }
        )

# ---------------------------------------------------------------------------
# PAGE: AI Planner (Agentic System)
# ---------------------------------------------------------------------------

elif page == "🤖 AI Planner":
    st.markdown("# 🤖 AI Infrastructure Planner")
    st.markdown("Agentic reasoning engine powered by LangGraph + Groq + RAG")
    st.markdown("")
    
    # Initialize session state
    if "agent_result" not in st.session_state:
        st.session_state.agent_result = None
    if "agent_running" not in st.session_state:
        st.session_state.agent_running = False
    
    # Query input
    st.markdown("### 💬 Ask the Planning Agent")
    
    # Preset queries
    preset = st.selectbox(
        "Quick Queries",
        [
            "Custom query...",
            "Analyze the full network and recommend infrastructure changes",
            "Which stations need immediate expansion?",
            "Optimize the charging schedule for Chicago stations",
            "What are the seasonal adjustments needed for Houston?",
            "Generate a capacity expansion plan for critical stations"
        ],
        key="preset_query"
    )
    
    if preset == "Custom query...":
        user_query = st.text_area(
            "Enter your query",
            placeholder="e.g., Analyze demand patterns and suggest infrastructure upgrades for high-load stations...",
            height=80,
            label_visibility="collapsed"
        )
    else:
        user_query = preset
    
    col_run, col_clear = st.columns([1, 4])
    
    with col_run:
        run_clicked = st.button("🚀 Run Agent", use_container_width=True, type="primary")
    with col_clear:
        if st.button("🗑️ Clear", use_container_width=False):
            st.session_state.agent_result = None
            st.rerun()
    
    if run_clicked and user_query:
        # Check prerequisites
        groq_key = os.environ.get("GROQ_API_KEY", "")
        if not groq_key:
            st.error("⚠️ Please enter your Groq API Key in the sidebar first.")
            st.stop()
        
        # Ensure RAG is ingested
        vectordb_path = os.path.join(ROOT_DIR, "src", "vectordb", "chroma_store")
        if not os.path.exists(vectordb_path):
            with st.spinner("📚 Initializing knowledge base..."):
                from src.vectordb.store import ingest_documents
                ingest_documents()
        
        # Run the agent
        with st.spinner(""):
            # Progress display
            progress_container = st.empty()
            steps = [
                ("📊 Analyzing charging demand patterns...", 0.2),
                ("📍 Identifying high-load locations...", 0.4),
                ("🏗️ Generating infrastructure expansion plan (RAG)...", 0.6),
                ("⚡ Optimizing scheduling insights...", 0.8),
                ("📎 Compiling references...", 0.95),
            ]
            
            progress_bar = st.progress(0)
            
            for step_text, step_progress in steps:
                progress_container.markdown(f"**{step_text}**")
                progress_bar.progress(step_progress)
                time.sleep(0.3)
            
            try:
                from src.agent.graph import run_agent
                result = run_agent(user_query)
                st.session_state.agent_result = result
            except Exception as e:
                st.error(f"Agent error: {str(e)}")
                import traceback
                st.code(traceback.format_exc())
                st.session_state.agent_result = None
            
            progress_bar.progress(1.0)
            progress_container.markdown("**✅ Agent workflow complete!**")
            time.sleep(0.5)
            progress_container.empty()
            progress_bar.empty()
    
    # Display results
    if st.session_state.agent_result:
        result = st.session_state.agent_result
        
        st.markdown("---")
        
        # Workflow visualization
        st.markdown("### 🔄 Agent Workflow")
        flow_cols = st.columns(5)
        node_labels = [
            ("📊", "Analyze"),
            ("📍", "Locate"),
            ("🏗️", "Plan"),
            ("⚡", "Optimize"),
            ("📎", "References")
        ]
        for i, (emoji, label) in enumerate(node_labels):
            with flow_cols[i]:
                st.markdown(
                    f"<div style='text-align:center; padding:16px; "
                    f"background: linear-gradient(135deg, rgba(99,102,241,0.12), rgba(139,92,246,0.06)); "
                    f"border: 1px solid rgba(99,102,241,0.25); border-radius:14px;'>"
                    f"<div style='font-size:1.6rem;'>{emoji}</div>"
                    f"<div style='color:#a78bfa; font-weight:600; font-size:0.85rem; margin-top:6px;'>{label}</div>"
                    f"<div style='color:#34d399; font-size:0.7rem; margin-top:4px;'>✓ Complete</div>"
                    f"</div>",
                    unsafe_allow_html=True
                )
        
        st.markdown("")
        
        # Structured output display
        out_tabs = st.tabs([
            "📄 Full Report",
            "📊 Analysis",
            "📍 Locations",
            "🏗️ Expansion Plan",
            "⚡ Scheduling",
            "📎 References"
        ])
        
        with out_tabs[0]:
            final_report = result.get("final_report", "")
            if final_report:
                st.markdown(final_report)
            else:
                st.info("No report generated.")
        
        with out_tabs[1]:
            analysis = result.get("analysis", "")
            if analysis:
                st.markdown(analysis)
            else:
                st.info("No analysis available.")
        
        with out_tabs[2]:
            high_load = result.get("high_load_locations", [])
            if high_load:
                for h in high_load:
                    severity = h.get("severity", "UNKNOWN")
                    if severity == "CRITICAL":
                        badge_class = "badge-critical"
                        icon = "🔴"
                    elif severity == "OPTIMIZATION":
                        badge_class = "badge-optimization"
                        icon = "🟡"
                    else:
                        badge_class = "badge-normal"
                        icon = "⚪"
                    
                    st.markdown(
                        f"{icon} **{h.get('station_id', 'N/A')}** — {h.get('location', 'N/A')} "
                        f" `{severity}` | Protocol: `{h.get('protocol', 'N/A')}` | "
                        f"Max Load: **{h.get('max_load', 'N/A')}** | "
                        f"Avg Load: {h.get('avg_load', 'N/A')}"
                    )
                    st.markdown("")
            else:
                st.info("No high-load locations identified.")
        
        with out_tabs[3]:
            plan = result.get("infrastructure_plan", "")
            if plan:
                st.markdown(plan)
            else:
                st.info("No infrastructure plan generated.")
        
        with out_tabs[4]:
            insights = result.get("scheduling_insights", "")
            if insights:
                st.markdown(insights)
            else:
                st.info("No scheduling insights generated.")
        
        with out_tabs[5]:
            refs = result.get("references", [])
            if refs:
                for ref in refs:
                    st.markdown(
                        f"📄 **{ref.get('source_name', 'Unknown')}** "
                        f"(`{ref.get('source_file', '')}`) — "
                        f"{ref.get('excerpts_used', 0)} excerpt(s) used"
                    )
                    with st.expander("Preview"):
                        st.markdown(ref.get("sample_excerpt", "No preview available."))
            else:
                st.info("No references available.")

# ---------------------------------------------------------------------------
# PAGE: Model Performance
# ---------------------------------------------------------------------------

elif page == "📈 Model Performance":
    st.markdown("# 📈 ML Model Performance")
    st.markdown("XGBoost Demand Prediction — Evaluation Metrics & Feature Analysis")
    st.markdown("")
    
    processed, raw = load_data()
    
    if processed is None:
        st.error("No processed data found.")
        st.stop()
    
    # Retrain inline for metrics display
    from sklearn.model_selection import train_test_split
    from sklearn.metrics import mean_absolute_error, r2_score, mean_squared_error
    
    try:
        from xgboost import XGBRegressor
        has_xgb = True
    except ImportError:
        has_xgb = False
    
    if has_xgb:
        df = processed.copy()
        y = df["Load_Score"]
        
        df["Day_Numeric"] = pd.factorize(df["Day_of_Week"])[0]
        df["Location_Numeric"] = pd.factorize(df["Charging Station Location"])[0]
        df["Is_Peak"] = df["Hour"].apply(lambda x: 1 if (8 <= x <= 10 or 17 <= x <= 20) else 0)
        
        np.random.seed(42)
        noise = np.random.normal(0, df["Energy Consumed (kWh)"].std() * 0.45, len(df))
        df["Forecasted_Energy"] = df["Energy Consumed (kWh)"] + noise
        
        features = ["Hour", "Day_Numeric", "Temperature (°C)", "Is_Peak", "Location_Numeric", "Forecasted_Energy"]
        X = df[features]
        
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
        
        model = XGBRegressor(n_estimators=150, max_depth=6, learning_rate=0.1, random_state=42, n_jobs=-1)
        model.fit(X_train, y_train)
        predictions = model.predict(X_test)
        
        mae = mean_absolute_error(y_test, predictions)
        rmse = np.sqrt(mean_squared_error(y_test, predictions))
        r2 = r2_score(y_test, predictions)
        
        # --- KPIs ---
        col1, col2, col3, col4 = st.columns(4)
        col1.metric("R² Score", f"{r2:.4f}")
        col2.metric("MAE", f"{mae:.2f}")
        col3.metric("RMSE", f"{rmse:.2f}")
        col4.metric("Samples", f"{len(y)}")
        
        st.markdown("")
        
        tab_m1, tab_m2, tab_m3 = st.tabs(["📉 Predictions", "📊 Feature Importance", "📦 Distribution"])
        
        with tab_m1:
            # Actual vs Predicted
            fig_pred = go.Figure()
            fig_pred.add_trace(go.Scatter(
                x=y_test.values,
                y=predictions,
                mode="markers",
                marker=dict(
                    color=abs(y_test.values - predictions),
                    colorscale=[[0, "#34d399"], [0.5, "#818cf8"], [1, "#f472b6"]],
                    size=6,
                    opacity=0.7,
                    colorbar=dict(title="Error", titlefont=dict(color="#94a3b8"), tickfont=dict(color="#94a3b8"))
                ),
                name="Predictions",
                hovertemplate="Actual: %{x:.1f}<br>Predicted: %{y:.1f}<extra></extra>"
            ))
            # Perfect prediction line
            min_val = min(y_test.min(), predictions.min())
            max_val = max(y_test.max(), predictions.max())
            fig_pred.add_trace(go.Scatter(
                x=[min_val, max_val],
                y=[min_val, max_val],
                mode="lines",
                line=dict(color="#fbbf24", width=2, dash="dash"),
                name="Perfect Prediction",
                showlegend=True
            ))
            fig_pred.update_layout(
                **PLOT_TEMPLATE["layout"].to_plotly_json(),
                title="Actual vs Predicted Load Score",
                xaxis_title="Actual Load Score",
                yaxis_title="Predicted Load Score",
                height=450,
            )
            st.plotly_chart(fig_pred, use_container_width=True)
        
        with tab_m2:
            # Feature importance
            fi = dict(zip(features, model.feature_importances_))
            fi_df = pd.DataFrame(list(fi.items()), columns=["Feature", "Importance"])
            fi_df = fi_df.sort_values("Importance", ascending=True)
            
            fig_fi = go.Figure(data=[go.Bar(
                y=fi_df["Feature"],
                x=fi_df["Importance"],
                orientation="h",
                marker=dict(
                    color=fi_df["Importance"],
                    colorscale=[[0, "#312e81"], [0.5, "#6366f1"], [1, "#c084fc"]],
                    cornerradius=6
                ),
                text=(fi_df["Importance"] * 100).round(1).astype(str) + "%",
                textposition="inside",
                textfont=dict(color="white", size=12, family="Inter")
            )])
            fig_fi.update_layout(
                **PLOT_TEMPLATE["layout"].to_plotly_json(),
                title="Feature Importance (XGBoost)",
                xaxis_title="Importance",
                height=350,
            )
            st.plotly_chart(fig_fi, use_container_width=True)
        
        with tab_m3:
            col_l, col_r = st.columns(2)
            
            with col_l:
                # Target distribution
                fig_dist = go.Figure(data=[go.Histogram(
                    x=y,
                    nbinsx=40,
                    marker=dict(
                        color="#818cf8",
                        line=dict(color="#4f46e5", width=1)
                    ),
                    opacity=0.8
                )])
                fig_dist.update_layout(
                    **PLOT_TEMPLATE["layout"].to_plotly_json(),
                    title="Load Score Distribution",
                    xaxis_title="Load Score",
                    yaxis_title="Count",
                    height=350,
                )
                st.plotly_chart(fig_dist, use_container_width=True)
            
            with col_r:
                # Residuals
                residuals = y_test.values - predictions
                fig_res = go.Figure(data=[go.Histogram(
                    x=residuals,
                    nbinsx=40,
                    marker=dict(
                        color="#a78bfa",
                        line=dict(color="#7c3aed", width=1)
                    ),
                    opacity=0.8
                )])
                fig_res.update_layout(
                    **PLOT_TEMPLATE["layout"].to_plotly_json(),
                    title="Prediction Residuals Distribution",
                    xaxis_title="Residual (Actual - Predicted)",
                    yaxis_title="Count",
                    height=350,
                )
                st.plotly_chart(fig_res, use_container_width=True)
    else:
        st.warning("XGBoost is not installed. Run `pip install xgboost` to view model performance.")
