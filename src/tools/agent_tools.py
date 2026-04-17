from langchain.tools import tool
from src.tools.ml_tool import predict_station_load
from src.tools.rag_retriever import get_policy_guidelines
from src.tools.simulation_engine import run_scenario_simulation

@tool
def station_load_predictor(hour: int, day: str, temp: int):
    """
    Predicts the EV station load score (0-100) based on time and weather. 
    Use this tool whenever you need to analyze a station's current or specific predicted state.
    """
    prediction = predict_station_load(hour, day, temp)
    return prediction['predicted_load_score']

@tool
def policy_researcher(query: str):
    """
    Searches the RAG database for EV grid protocols, RERA rules, and engineering mandates.
    Use this to find specific IDs like GS-CRIT-03 or hardware selection criteria.
    """
    return get_policy_guidelines(query)

@tool
def scenario_simulator(load_multiplier: float, temp_increase: float):
    """
    Runs a 24-hour 'What-if' simulation. Use this tool ONLY when the user asks 
    hypothetical questions about future adoption or climate changes.
    """
    return run_scenario_simulation(load_multiplier, temp_increase)