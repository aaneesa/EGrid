import re

with open('/Users/anweshaadhikari/Desktop/EGrid/app/main.py', 'r') as f:
    content = f.read()

new_css = '''st.markdown("""
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

    html, body, [class*="st-"] {
        font-family: 'Inter', sans-serif;
        background-color: var(--bg-color);
        color: var(--text-main);
    }
    
    /* Background effects */
    .stApp {
        background: radial-gradient(circle at top right, rgba(123, 44, 191, 0.15), transparent 40%),
                    radial-gradient(circle at bottom left, rgba(0, 255, 204, 0.1), transparent 40%),
                    var(--bg-color);
    }

    /* Typography */
    h1, h2, h3, .sb-name, .wc-title {
        font-family: 'Outfit', sans-serif !important;
    }

    .block-container { padding-top: 2rem; padding-bottom: 3rem; max-width: 1200px; }

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
        background: linear-gradient(135deg, var(--primary) 0%, #00b38f 100%) !important;
        color: #000 !important; font-weight: 800 !important; font-family: 'Outfit', sans-serif !important;
        letter-spacing: 1.5px !important; border: none !important;
        border-radius: 12px !important; transition: all 0.3s ease !important;
        padding: 24px 20px !important;
        text-transform: uppercase;
        box-shadow: 0 4px 15px var(--primary-glow) !important;
    }
    .stButton > button[kind="primary"]:hover {
        box-shadow: 0 8px 25px rgba(0, 255, 204, 0.6) !important;
        transform: translateY(-2px) !important;
    }
    .stDownloadButton > button {
        background: linear-gradient(135deg, var(--primary) 0%, #00b38f 100%) !important;
        color: #000 !important; font-weight: 700 !important; font-family: 'Outfit', sans-serif !important;
        border: none !important; border-radius: 12px !important;
        padding: 16px 20px !important; text-transform: uppercase; letter-spacing: 1px !important;
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
""", unsafe_allow_html=True)'''

content = re.sub(r'st\.markdown\("""\s*<style>.*?</style>\s*""", unsafe_allow_html=True\)', new_css, content, flags=re.DOTALL)

sidebar_old = '''        st.markdown("""
            <div class="sidebar-brand">
                <div style="font-size: 2rem;">⚡</div>
                <div class="sb-name">EGrid</div>
                <div class="sb-version">AI Supervisor · v2.0</div>
                <div class="sb-line"></div>
            </div>
        """, unsafe_allow_html=True)'''
sidebar_new = '''        st.markdown("""
            <div class="sidebar-brand">
                <div class="sb-icon">⚡</div>
                <div class="sb-name">EGrid</div>
                <div class="sb-version">AI Supervisor · v3.0</div>
            </div>
        """, unsafe_allow_html=True)'''
content = content.replace(sidebar_old, sidebar_new)

header_old = '''    # ───── HEADER ─────
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
    """, unsafe_allow_html=True)'''

header_new = '''    # ───── HEADER ─────
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
    """, unsafe_allow_html=True)'''
content = content.replace(header_old, header_new)

metrics_old = '''    sim_status = "⚠️ STRESS TEST" if run_simulation else "● STABLE"
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
    """, unsafe_allow_html=True)'''

metrics_new = '''    sim_status = "STRESS TEST" if run_simulation else "SYSTEM STABLE"
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
    """, unsafe_allow_html=True)'''
content = content.replace(metrics_old, metrics_new)


welcome_old = '''    else:
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
        """, unsafe_allow_html=True)'''

welcome_new = '''    else:
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
        """, unsafe_allow_html=True)'''
content = content.replace(welcome_old, welcome_new)


with open('/Users/anweshaadhikari/Desktop/EGrid/app/main.py', 'w') as f:
    f.write(content)

print("UI updated successfully")
