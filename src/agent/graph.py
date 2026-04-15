"""
EGrid Agentic Infrastructure Planning System
LangGraph workflow with 5 reasoning nodes:
  Analyze → Locate → Plan → Optimize → References
"""
import os
import json
import pandas as pd
import numpy as np
from typing import TypedDict, List, Optional, Annotated
from langgraph.graph import StateGraph, END

# ---------------------------------------------------------------------------
# State Schema
# ---------------------------------------------------------------------------

class EGridState(TypedDict):
    """Explicit state managed across all agent nodes."""
    # Input
    user_query: str
    
    # Data context (loaded once)
    data_summary: Optional[dict]
    station_data: Optional[list]
    
    # Node outputs (structured)
    analysis: Optional[str]          # Charging Demand Summary
    high_load_locations: Optional[list]  # High-load Location IDs
    infrastructure_plan: Optional[str]   # Infrastructure Expansion Recs
    scheduling_insights: Optional[str]   # Scheduling Insights
    references: Optional[list]       # Supporting References
    
    # RAG context
    retrieved_docs: Optional[list]
    
    # Final assembled output
    final_report: Optional[str]
    
    # LLM config
    llm_provider: Optional[str]

# ---------------------------------------------------------------------------
# Data Loading Utility
# ---------------------------------------------------------------------------

def load_station_data():
    """Load processed data and compute per-station summaries."""
    data_path = os.path.join(os.path.dirname(__file__), "..", "..", "data", "processed", "processed_data.csv")
    
    if not os.path.exists(data_path):
        return None, None
    
    df = pd.read_csv(data_path)
    
    # Station-level aggregation
    station_stats = df.groupby(["Charging Station ID", "Charging Station Location"]).agg({
        "Load_Score": ["mean", "max", "min", "std"],
        "Energy Consumed (kWh)": ["sum", "mean"],
        "Vehicle_Count": ["sum", "mean"],
        "Temperature (°C)": ["mean"],
        "Hour": ["count"]
    }).reset_index()
    
    station_stats.columns = [
        "Station_ID", "Location", 
        "Avg_Load", "Max_Load", "Min_Load", "Load_Std",
        "Total_Energy", "Avg_Energy",
        "Total_Vehicles", "Avg_Vehicles",
        "Avg_Temperature",
        "Session_Count"
    ]
    
    station_stats = station_stats.round(2)
    
    # Data summary
    summary = {
        "total_stations": len(station_stats),
        "total_sessions": int(df.shape[0]),
        "cities": list(df["Charging Station Location"].unique()),
        "avg_load_score": round(df["Load_Score"].mean(), 2),
        "max_load_score": round(df["Load_Score"].max(), 2),
        "min_load_score": round(df["Load_Score"].min(), 2),
        "avg_temperature": round(df["Temperature (°C)"].mean(), 2),
        "peak_hours": list(df.groupby("Hour")["Load_Score"].mean().nlargest(3).index),
        "total_energy_kwh": round(df["Energy Consumed (kWh)"].sum(), 2)
    }
    
    station_records = station_stats.to_dict("records")
    return summary, station_records

# ---------------------------------------------------------------------------
# LLM Utility
# ---------------------------------------------------------------------------

def call_llm(prompt: str, system_prompt: str = "") -> str:
    """Call the configured LLM (Groq with open-source models)."""
    try:
        from langchain_groq import ChatGroq
        
        llm = ChatGroq(
            model="llama-3.3-70b-versatile",
            temperature=0.3,
            max_tokens=2048,
        )
        
        messages = []
        if system_prompt:
            messages.append(("system", system_prompt))
        messages.append(("human", prompt))
        
        response = llm.invoke(messages)
        return response.content
        
    except Exception as e:
        # Fallback: rule-based response if LLM fails
        return f"[LLM unavailable — rule-based fallback] {str(e)}"

# ---------------------------------------------------------------------------
# Node 1: ANALYZE — Charging Demand Summary
# ---------------------------------------------------------------------------

def analyze_node(state: EGridState) -> dict:
    """Analyze charging demand patterns from the data."""
    summary, stations = load_station_data()
    
    if not summary:
        return {
            "data_summary": {},
            "station_data": [],
            "analysis": "⚠️ No processed data available. Please run the data preprocessing pipeline first."
        }
    
    # Find key patterns
    high_load = [s for s in stations if s["Max_Load"] > 60]
    low_load = [s for s in stations if s["Avg_Load"] < 35]
    
    # City-level aggregation
    city_loads = {}
    for s in stations:
        city = s["Location"]
        if city not in city_loads:
            city_loads[city] = []
        city_loads[city].append(s["Avg_Load"])
    
    city_avg = {city: round(np.mean(loads), 2) for city, loads in city_loads.items()}
    hottest_city = max(city_avg, key=city_avg.get)
    
    system_prompt = """You are EGrid's demand analysis engine. You produce concise, data-driven 
    charging demand summaries. Use actual numbers from the data provided. Be specific about 
    station IDs, locations, and load scores. Format your response with clear sections and bullet points."""
    
    prompt = f"""Analyze the following EV charging network data and produce a Charging Demand Summary.

**User Query:** {state.get('user_query', 'General demand analysis')}

**Network Overview:**
- Total Stations: {summary['total_stations']}
- Total Sessions: {summary['total_sessions']}
- Cities Covered: {', '.join(summary['cities'])}
- Network Average Load Score: {summary['avg_load_score']}
- Peak Load Score: {summary['max_load_score']}
- Peak Hours: {summary['peak_hours']}
- Total Energy Delivered: {summary['total_energy_kwh']} kWh

**High-Load Stations (Max Load > 60):**
{json.dumps(high_load[:10], indent=2)}

**City Average Load Scores:**
{json.dumps(city_avg, indent=2)}

Produce a structured demand summary covering:
1. Overall network health assessment
2. Key demand patterns (temporal, geographic)
3. Stations of concern (high load)
4. Energy consumption trends
5. Temperature impact observations"""

    analysis = call_llm(prompt, system_prompt)
    
    return {
        "data_summary": summary,
        "station_data": stations,
        "analysis": analysis
    }

# ---------------------------------------------------------------------------
# Node 2: LOCATE — Identify High-Load Locations
# ---------------------------------------------------------------------------

def locate_node(state: EGridState) -> dict:
    """Identify and rank high-load locations needing attention."""
    stations = state.get("station_data", [])
    summary = state.get("data_summary", {})
    
    if not stations:
        return {"high_load_locations": []}
    
    # Classify stations by load severity
    critical = [s for s in stations if s["Max_Load"] > 70]     # GS-CRIT-03
    optimization = [s for s in stations if 40 <= s["Max_Load"] <= 70]  # GS-CAP-02
    phantom = [s for s in stations if s["Avg_Load"] > 25 and s["Avg_Energy"] < 1.0]  # GS-EFF-01
    
    # Sort by severity
    critical.sort(key=lambda x: x["Max_Load"], reverse=True)
    optimization.sort(key=lambda x: x["Max_Load"], reverse=True)
    
    high_load_list = []
    
    for s in critical[:5]:
        high_load_list.append({
            "station_id": s["Station_ID"],
            "location": s["Location"],
            "severity": "CRITICAL",
            "protocol": "GS-CRIT-03",
            "max_load": s["Max_Load"],
            "avg_load": s["Avg_Load"],
            "avg_temperature": s["Avg_Temperature"],
            "sessions": s["Session_Count"]
        })
    
    for s in optimization[:5]:
        high_load_list.append({
            "station_id": s["Station_ID"],
            "location": s["Location"],
            "severity": "OPTIMIZATION",
            "protocol": "GS-CAP-02",
            "max_load": s["Max_Load"],
            "avg_load": s["Avg_Load"],
            "avg_temperature": s["Avg_Temperature"],
            "sessions": s["Session_Count"]
        })
    
    for s in phantom[:3]:
        high_load_list.append({
            "station_id": s["Station_ID"],
            "location": s["Location"],
            "severity": "PHANTOM_LOAD",
            "protocol": "GS-EFF-01",
            "max_load": s["Max_Load"],
            "avg_load": s["Avg_Load"],
            "avg_energy": s["Avg_Energy"],
            "sessions": s["Session_Count"]
        })
    
    return {"high_load_locations": high_load_list}

# ---------------------------------------------------------------------------
# Node 3: PLAN — Infrastructure Expansion Recommendations (RAG-augmented)
# ---------------------------------------------------------------------------

def plan_node(state: EGridState) -> dict:
    """Generate infrastructure expansion recommendations using RAG."""
    high_load = state.get("high_load_locations", [])
    analysis = state.get("analysis", "")
    
    # RAG Retrieval
    from src.vectordb.store import retrieve
    
    # Build retrieval queries from high-load locations
    rag_queries = [
        "infrastructure expansion when Load_Score is critical and above 70",
        "charger placement guidelines for high demand stations",
        "capacity expansion sizing and financial feasibility"
    ]
    
    # Add location-specific queries
    locations = set(h["location"] for h in high_load if h.get("location"))
    for loc in list(locations)[:2]:
        rag_queries.append(f"infrastructure guidelines for {loc} region")
    
    all_retrieved = []
    seen_contents = set()
    for query in rag_queries:
        docs = retrieve(query, n_results=3)
        for doc in docs:
            content_key = doc["content"][:100]
            if content_key not in seen_contents:
                seen_contents.add(content_key)
                all_retrieved.append(doc)
    
    # Format retrieved context
    rag_context = "\n\n".join([
        f"[Source: {d['source']}]\n{d['content']}" 
        for d in all_retrieved[:8]
    ])
    
    system_prompt = """You are EGrid's infrastructure planning engine. You generate specific, 
    actionable infrastructure expansion recommendations grounded in policy guidelines. 
    Always reference specific station IDs, locations, and protocol numbers from the data and guidelines.
    Format as a structured plan with clear priorities and timelines."""
    
    critical_stations = [h for h in high_load if h["severity"] == "CRITICAL"]
    optimization_stations = [h for h in high_load if h["severity"] == "OPTIMIZATION"]
    
    prompt = f"""Generate an Infrastructure Expansion Plan based on the demand analysis and planning guidelines.

**Demand Analysis Summary:**
{analysis[:800]}

**Critical Stations (Load_Score > 70):**
{json.dumps(critical_stations, indent=2)}

**Optimization Zone Stations (Load_Score 40-70):**
{json.dumps(optimization_stations[:5], indent=2)}

**Planning Guidelines (Retrieved from Knowledge Base):**
{rag_context}

Generate a structured expansion plan covering:
1. **Immediate Actions (0-30 days)**: Emergency measures for critical stations
2. **Short-term Expansion (30-90 days)**: Hardware additions and upgrades
3. **Medium-term Strategy (90-180 days)**: Network-level improvements
4. **Charger Type Recommendations**: Specific charger types for each station based on demand patterns
5. **Grid Interconnection Needs**: Transformer/feeder requirements
6. **Estimated Costs**: Ballpark figures from guidelines"""

    plan = call_llm(prompt, system_prompt)
    
    return {
        "infrastructure_plan": plan,
        "retrieved_docs": all_retrieved
    }

# ---------------------------------------------------------------------------
# Node 4: OPTIMIZE — Scheduling Insights
# ---------------------------------------------------------------------------

def optimize_node(state: EGridState) -> dict:
    """Generate scheduling and load optimization insights."""
    high_load = state.get("high_load_locations", [])
    summary = state.get("data_summary", {})
    
    # RAG retrieval for scheduling
    from src.vectordb.store import retrieve
    
    schedule_docs = retrieve("scheduling optimization peak shifting dynamic pricing load balancing", n_results=5)
    seasonal_docs = retrieve("seasonal adjustment winter summer charging protocols", n_results=3)
    
    rag_context = "\n\n".join([
        f"[Source: {d['source']}]\n{d['content']}" 
        for d in (schedule_docs + seasonal_docs)[:6]
    ])
    
    system_prompt = """You are EGrid's scheduling optimization engine. You produce actionable 
    scheduling recommendations to reduce peak loads and improve station utilization. 
    Be specific about which stations, hours, and pricing strategies to apply.
    Format your response with clear sections on pricing, load balancing, and seasonal adjustments."""
    
    prompt = f"""Generate Scheduling Optimization Insights for the EGrid network.

**Network Context:**
- Peak Hours: {summary.get('peak_hours', 'N/A')}
- Average Load Score: {summary.get('avg_load_score', 'N/A')}
- Cities: {summary.get('cities', [])}
- Average Temperature: {summary.get('avg_temperature', 'N/A')}°C

**High-Load Stations Requiring Schedule Optimization:**
{json.dumps(high_load[:8], indent=2)}

**Scheduling Guidelines (Retrieved from Knowledge Base):**
{rag_context}

Generate scheduling insights covering:
1. **Dynamic Pricing Recommendations**: Specific pricing tiers for peak/off-peak/shoulder hours
2. **Load Balancing Strategy**: Station-level and network-level balancing approaches
3. **Peak Shifting Opportunities**: Which stations and hours offer the most potential
4. **Seasonal Adjustments**: Current season-appropriate recommendations based on temperature data
5. **Fleet/Commercial Scheduling**: If applicable, overnight fleet charging optimization
6. **Expected Impact**: Projected reduction in peak Load_Scores from implementing recommendations"""

    insights = call_llm(prompt, system_prompt)
    
    return {"scheduling_insights": insights}

# ---------------------------------------------------------------------------
# Node 5: REFERENCES — Compile Supporting References
# ---------------------------------------------------------------------------

def references_node(state: EGridState) -> dict:
    """Compile all supporting references from RAG retrievals."""
    retrieved_docs = state.get("retrieved_docs", [])
    
    # Deduplicate by source
    sources = {}
    for doc in retrieved_docs:
        source = doc.get("source_file", doc.get("source", "Unknown"))
        if source not in sources:
            sources[source] = {
                "source_name": doc.get("source", source),
                "source_file": source,
                "excerpts_used": 0,
                "sample_excerpt": doc["content"][:200] + "..."
            }
        sources[source]["excerpts_used"] += 1
    
    ref_list = list(sources.values())
    
    # Build final report
    analysis = state.get("analysis", "No analysis available.")
    high_load = state.get("high_load_locations", [])
    plan = state.get("infrastructure_plan", "No plan generated.")
    insights = state.get("scheduling_insights", "No scheduling insights available.")
    
    # Format high-load locations
    loc_lines = []
    for h in high_load:
        severity_emoji = "🔴" if h["severity"] == "CRITICAL" else "🟡" if h["severity"] == "OPTIMIZATION" else "⚪"
        loc_lines.append(
            f"{severity_emoji} **{h['station_id']}** ({h['location']}) — "
            f"Severity: {h['severity']} | Protocol: {h.get('protocol', 'N/A')} | "
            f"Max Load: {h['max_load']}"
        )
    
    locations_text = "\n".join(loc_lines) if loc_lines else "No high-load locations identified."
    
    # Format references
    ref_lines = []
    for i, ref in enumerate(ref_list, 1):
        ref_lines.append(f"{i}. **{ref['source_name']}** (`{ref['source_file']}`) — {ref['excerpts_used']} excerpt(s) used")
    
    references_text = "\n".join(ref_lines) if ref_lines else "No references retrieved."
    
    final_report = f"""# 📊 EGrid Infrastructure Planning Report

---

## 1. Charging Demand Analysis
{analysis}

---

## 2. High-Load Location Identification
{locations_text}

---

## 3. Infrastructure Expansion Plan
{plan}

---

## 4. Scheduling Optimization Insights
{insights}

---

## 5. Supporting References
{references_text}

---

*Report generated by EGrid Agentic Infrastructure Planning System*
"""
    
    return {
        "references": ref_list,
        "final_report": final_report
    }

# ---------------------------------------------------------------------------
# Build the LangGraph Workflow
# ---------------------------------------------------------------------------

def build_graph():
    """Build and compile the EGrid agentic workflow."""
    workflow = StateGraph(EGridState)
    
    # Add nodes
    workflow.add_node("analyze", analyze_node)
    workflow.add_node("locate", locate_node)
    workflow.add_node("plan", plan_node)
    workflow.add_node("optimize", optimize_node)
    workflow.add_node("references", references_node)
    
    # Define edges: Analyze → Locate → Plan → Optimize → References → END
    workflow.set_entry_point("analyze")
    workflow.add_edge("analyze", "locate")
    workflow.add_edge("locate", "plan")
    workflow.add_edge("plan", "optimize")
    workflow.add_edge("optimize", "references")
    workflow.add_edge("references", END)
    
    return workflow.compile()

def run_agent(query: str = "Analyze the EV charging network and provide infrastructure planning recommendations.") -> dict:
    """Run the full agentic workflow."""
    graph = build_graph()
    
    initial_state = {
        "user_query": query,
        "data_summary": None,
        "station_data": None,
        "analysis": None,
        "high_load_locations": None,
        "infrastructure_plan": None,
        "scheduling_insights": None,
        "references": None,
        "retrieved_docs": None,
        "final_report": None,
        "llm_provider": "groq"
    }
    
    result = graph.invoke(initial_state)
    return result

# ---------------------------------------------------------------------------
# CLI Entry Point
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    print("🚀 Running EGrid Agentic Infrastructure Planning System...")
    print("=" * 60)
    result = run_agent()
    print(result.get("final_report", "No report generated."))
