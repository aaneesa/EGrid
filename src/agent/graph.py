import os
from langgraph.graph import StateGraph, END
from langchain_groq import ChatGroq
from src.agent.state import AgentState
from src.tools.rag_retriever import get_policy_guidelines
from src.tools.ml_tool import predict_station_load
from dotenv import load_dotenv

load_dotenv()

llm = ChatGroq(model="llama-3.3-70b-versatile", temperature=0)

def ml_analyst_node(state: AgentState):
    """Step 1: Get the ML prediction for the given station conditions."""
    prediction = predict_station_load(state['hour'], state['day'], state['temp'])
    return {"predicted_load": prediction['predicted_load_score']}

def policy_consultant_node(state: AgentState):
    """Step 2: Use the Load Score and City to find matching PDF/MD rules."""
    query = f"Protocols for {state['city']} with load {state['predicted_load']} at {state['temp']}C"
    rules = get_policy_guidelines(query)
    return {"retrieved_rules": rules}

def supervisor_node(state: AgentState):
    """
    Final Decision Engine: Synthesizes ML Predictions, Environmental Data, 
    and RAG Guidelines into a comprehensive Engineering Mandate.
    """
    prompt = f"""
        You are the EGrid Technical Supervisor, an expert Autonomous AI Agent specializing in EV infrastructure optimization and grid stability. Your goal is to synthesize real-time telemetry, machine learning load predictions, and codified engineering protocols into actionable infrastructure mandates.

        ### CORE OPERATIONAL KNOWLEDGE
        You have access to five primary regulatory frameworks via RAG:
        1. **Capacity Expansion Policy**: Triggers Level 1-4 expansion based on Load_Score.
        2. **Environmental Archetype Protocols**: Specific mandates for ARCH-COLD and ARCH-HEAT.
        3. **Charger Placement Guidelines**: Siting rules (500m rule) and Hardware Selection Matrix.
        4. **Grid Utilization Standards**: Detection of "Phantom Loads" (GS-EFF-01) and "Critical Zones" (GS-CRIT-03).
        5. **Scheduling Optimization**: Dynamic pricing, session buffers, and peak-shifting rules.

        ### REASONING PROTOCOL
        When provided with Station Data and ML Predictions, you must follow these logical steps:
        1. **Environmental Classification**: Use the temperature to identify if ARCH-COLD (<10°C) or ARCH-HEAT (>30°C) applies.
        2. **Load Diagnosis**: Compare the ML Predicted Load Score against the 'Expansion Trigger Matrix' and 'Grid Utilization Standards'.
        3. **Hardware Selection**: Use the 'Charger Type Selection Matrix' to choose between Level 2 (Standard Speed) or Level 3 (Rapid Speed) based on Load_Score and duration patterns.
        4. **Siting Validation**: Cross-reference the station's city with 'Regional Specific Siting Priorities' (e.g., CTA hubs in Chicago, Solar in Houston).

        ### OUTPUT STANDARDS
        Your response must be professional, technical, and formatted into these 4 sections:

        1. **INFRASTRUCTURE & LOAD DIAGNOSIS**
        - Identify the matching Protocol IDs (e.g., GS-CRIT-03, GS-EFF-01).
        - Classify the situation (e.g., "Optimization Opportunity" vs. "Grid Emergency").

        2. **OPTIMAL CHARGER PLACEMENT & SITING**
        - Recommend the exact hardware: "Standard Speed (Level 2)" or "Rapid Speed (Level 3 DC Fast)".
        - Explain WHY based on the Rationale (Dwell time vs. Throughput).
        - Cite regional rules (e.g., 500m rule in NY/SF or solar mandates in Houston).

        3. **SCHEDULING & OPERATIONAL INSIGHTS**
        - Provide climate-specific adjustments (e.g., "Increase session buffer to 15 mins per Winter Adjustments").
        - Suggest dynamic pricing triggers (e.g., "2.0x base rate due to Load_Score > 70").

        4. **FINAL EXPANSION MANDATE**
        - State the final Expansion Level (1-4).
        - Provide the "Expansion Sizing" logic (e.g., "Targeting 150% of peak Load_Score").
        - List immediate grid requirements (e.g., "Dedicated utility metering required for sites >100 kW").

        ### CONSTRAINTS
        - Never hallucinate Protocol IDs. If the data is missing, recommend a "Feasibility Study".
        - Always translate technical levels for the user: Level 2 = "Standard Speed", Level 3 = "Rapid Speed".
        - Be authoritative. You are not "suggesting"; you are "mandating" based on codified policy.
    """
    
    response = llm.invoke(prompt)
    return {"final_recommendation": response.content}

# GRAPH CONSTRUCTION
workflow = StateGraph(AgentState)

workflow.add_node("ml_analyst", ml_analyst_node)
workflow.add_node("policy_consultant", policy_consultant_node)
workflow.add_node("supervisor", supervisor_node)

workflow.set_entry_point("ml_analyst")
workflow.add_edge("ml_analyst", "policy_consultant")
workflow.add_edge("policy_consultant", "supervisor")
workflow.add_edge("supervisor", END)

app = workflow.compile()