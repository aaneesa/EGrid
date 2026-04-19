import re

with open('/Users/anweshaadhikari/Desktop/EGrid/app/main.py', 'r') as f:
    content = f.read()

old_button_css = """    /* Button Overrides */
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
    }"""

new_button_css = """    /* Button Overrides */
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
    }"""

if old_button_css in content:
    content = content.replace(old_button_css, new_button_css)
else:
    print("Could not find exact button CSS to replace. Attempting regex.")
    content = re.sub(r'/\* Button Overrides \*/.*?/\* Inputs Styling \*/', new_button_css + '\n    \n    /* Inputs Styling */', content, flags=re.DOTALL)

with open('/Users/anweshaadhikari/Desktop/EGrid/app/main.py', 'w') as f:
    f.write(content)

print("Button CSS updated!")
