# ⚡ EGrid — Agentic EV Infrastructure Optimization System

🌐 **Live Demo: [egrid1.streamlit.app](https://egrid1.streamlit.app/)**

> An autonomous AI framework that synthesizes machine learning load predictions with RAG-based policy retrieval to generate actionable EV charger placement mandates and investor-grade infrastructure reports.

---

## 📋 Table of Contents

- [Overview](#overview)
- [System Architecture](#system-architecture)
- [Project Structure](#project-structure)
- [Tech Stack](#tech-stack)
- [Installation](#installation)
- [Configuration](#configuration)
- [Running the Application](#running-the-application)
- [Agent Workflow](#agent-workflow)
- [Tools & Components](#tools--components)
- [Team](#team)

---

## Overview

The rapid proliferation of Electric Vehicles presents a dual challenge: increasing demand for accessible charging infrastructure and the subsequent strain on aging electrical grids. **EGrid** addresses this through two cooperating AI agents:

- **EGrid Technical Supervisor** — The core autonomous agent acting as an expert in EV infrastructure and grid stability. It synthesizes real-time telemetry and ML predictions into structured, four-section engineering mandates.
- **EV Infrastructure Investment Analyst** — A high-level financial consultant agent that translates technical output into an investor-grade **Investment Memorandum** covering CAPEX/OPEX, risk analysis, and ROI projections.

---

## System Architecture

```
User Query
    │
    ▼
LangGraph Technical Supervisor (llama-3.3-70b-versatile via Groq)
    │
    ├──► station_load_analyst    →  Load Score (0–100) via XGBoost
    │
    ├──► policy_researcher       →  Protocol IDs & Mandates via ChromaDB RAG
    │
    └──► scenario_simulator      →  Risk Level & Failure Hours (24-hr stress test)
                │
                ▼
    Data & Knowledge Layer
    ┌──────────────┬─────────────────────┬─────────────────────┐
    │  XGBoost /   │   Chroma Vector     │  Load/Temp          │
    │  demand_     │   Store             │  Multiplier Logic   │
    │  predictor   │                     │                     │
    └──────────────┴─────────────────────┴─────────────────────┘
                │
                ▼
    Structured 4-Section Mandate
    +
    Investment Memorandum (PDF Export)
```

---

## Project Structure

```
EGrid/
│
├── app/
│   └── main.py                  # Streamlit web application
│
├── data/
│   ├── raw/
│   │   └── ev_charging_patterns.csv   # Raw EV telemetry dataset
│   └── processed/
│       └── processed_data.csv         # Cleaned, feature-engineered data
│
├── src/
│   ├── __init__.py
│   │
│   ├── agent/
│   │   ├── __init__.py
│   │   └── graph.py             # LangGraph stateful agent definition
│   │
│   ├── models/
│   │   ├── demand_predictor.pkl # Trained XGBoost model
│   │   └── scaler.pkl           # Feature scaler
│   │
│   └── tools/
│       ├── __init__.py
│       ├── demand_analyzer.py   # Data preprocessing & Load Score computation
│       ├── predictor_model.py   # XGBoost training & inference
│       └── agent_tools.py       # LangChain tool definitions (load analyst, RAG, simulator)
│
├── knowledge_base/              # Policy documents for RAG
│   ├── capacity_expansion_policy.md
│   └── grid_utilization_standards.md
│
├── .env                         # API keys (not committed)
├── .gitignore
├── requirements.txt
└── README.md
```

---

## Tech Stack

| Layer | Technology |
|---|---|
| Agent Framework | LangGraph + LangChain |
| LLM | `llama-3.3-70b-versatile` via Groq |
| ML Model | XGBoost (XGBRegressor) |
| Vector Database | ChromaDB + HuggingFace Embeddings |
| Frontend | Streamlit |
| PDF Export | ReportLab |
| Data Processing | Pandas, NumPy, Scikit-learn |
| Environment | Python 3.10+ |

---

## Installation

### 1. Clone the repository

```bash
git clone https://github.com/aaneesa/EGrid.git
cd EGrid
```

### 2. Create and activate a virtual environment

```bash
python -m venv venv

# On macOS/Linux:
source venv/bin/activate

# On Windows:
venv\Scripts\activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

Additional dependencies not yet in `requirements.txt`:

```bash
pip install langgraph langchain-core langchain-community xgboost joblib \
            sentence-transformers reportlab
```

---

## Configuration

Create a `.env` file in the project root:

```env
GROQ_API_KEY=your_groq_api_key_here
```

Get a free Groq API key at [console.groq.com](https://console.groq.com).

---

## Running the Application

### Option A — Streamlit Web App (Recommended)

```bash
streamlit run app/main.py
```

Then open `http://localhost:8501` in your browser. From the UI you can:
- Select a city (Chicago, Houston, New York) with its environmental archetype
- Run the multi-agent pipeline on a custom query (e.g., *"Should we expand Level 3 chargers in downtown Houston?"*)
- View the structured mandate and Investment Memorandum
- Export results as a formatted PDF

### Option B — Run the Agent Directly (for testing)

```bash
python -m src.agent.graph
```

---

## Agent Workflow

The Technical Supervisor follows a strict four-step reasoning protocol:

### Step 1 — Environmental Classification
Identifies the thermal archetype of the selected city:
- `ARCH-HEAT` — temperature > 30°C (e.g., Houston)
- `ARCH-COLD` — temperature < 10°C (e.g., Chicago)

### Step 2 — Load Diagnosis (`station_load_analyst`)
Calls the XGBoost model with station, hour, and temperature features to compute a **Load Score (0–100)**. Peak-hour flags (08:00–10:00 and 17:00–20:00) are applied to refine accuracy.

### Step 3 — Regulatory Lookup (`policy_researcher`)
Queries the ChromaDB vector store using HuggingFace embeddings to retrieve relevant Protocol IDs and engineering mandates from indexed policy documents. The agent is **restricted from inventing Protocol IDs** — all citations must come from the RAG retriever.

### Step 4 — Mandate Generation
Produces a structured **4-section output**:
1. Environmental & Context Classification
2. Infrastructure Diagnosis (Load Scores, failure hours)
3. Regulatory Constraints (RAG-retrieved protocols)
4. Final Expansion Mandates (charger type, quantity, placement zones)

The Investment Analyst agent then converts this into an **Investment Memorandum** with CAPEX/OPEX breakdowns and ROI projections.

---

## Tools & Components

### `demand_analyzer.py`
Preprocessing pipeline for raw EV charging data:
- Parses `Charging Start Time` → extracts `Hour`, `Day_of_Week`, `Is_Weekend`
- Aggregates by station and hour for energy consumption and vehicle counts
- Computes a normalized **Load Score**: `0.5 × (Energy/Max_Energy) + 0.5 × (Vehicles/Max_Vehicles)` × 100

### `predictor_model.py`
XGBoost training and inference:
- **Features**: `Hour`, `Day_Numeric`, `Temperature`, `Is_Peak`, `Location_Numeric`, `Forecasted_Energy`
- **Target**: `Load_Score`
- **Evaluation**: MAE and R² Score
- Saves trained model to `src/models/demand_predictor.pkl`

### `agent_tools.py` (LangChain Tool Definitions)
Three tools exposed to the LangGraph agent:

| Tool | Description |
|---|---|
| `station_load_analyst` | Runs XGBoost inference for a given station, hour, and temperature |
| `policy_researcher` | Retrieves engineering protocols from ChromaDB using semantic search |
| `scenario_simulator` | Runs a 24-hour recursive stress test with configurable load multipliers |

### Scenario Simulator
- Applies a user-defined load multiplier (e.g., `2.0x`) to base predictions over 24 hours
- Identifies **failure hours** where simulated load exceeds 90%
- Assigns `CRITICAL` risk level if failures exceed 3 hours → triggers mandatory Level 3 charger recommendation

---

## Team

| Member | Role | Primary Deliverables |
|---|---|---|
| **Anwesha Adhikari** | Team Lead | Agent Logic & RAG Integration — `graph.py`, `rag_retriever.py` |
| **Anusha Prathapani** | ML Engineer | Data Pipeline & Agent Tools — `ml_tool.py`, `agent_tools.py` |
| **Kartikey Gupta** | Data Analyst | Dataset Prep & UI Logic — `demand_analyzer.py`, `main.py` |
| **Agnik Misra** | RAG Specialist | Knowledge Base & Deployment — `rag_builder.py`, Chroma DB |

---

*EGrid — April 2026*
