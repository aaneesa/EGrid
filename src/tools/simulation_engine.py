import numpy as np
from src.tools.ml_tool import get_prediction_logic
from langchain.tools import tool

@tool
def scenario_simulator(load_multiplier: float, temp_increase: float):
    """
    Runs a hypothetical 24-hour grid stress test. 
    Use this tool ONLY for 'What-if' or 'Scenario' queries.
    """
    failure_count = 0
    total_load = 0
    peak_load = 0
    
    for hour in range(24):
        simulated_temp = 25 + temp_increase 
        
        # Call the logic function directly
        predicted_load = get_prediction_logic(hour=hour, day="Monday", temp=simulated_temp)
        
        # Guard against model errors
        if isinstance(predicted_load, dict) and "error" in predicted_load:
            return f"Simulation aborted: {predicted_load['error']}"

        simulated_load = predicted_load * load_multiplier
        
        total_load += simulated_load
        if simulated_load > peak_load:
            peak_load = simulated_load
            
        if simulated_load > 90:
            failure_count += 1
            
    avg_load = total_load / 24
    
    return {
        "avg_load": round(avg_load, 2),
        "peak_load": round(peak_load, 2),
        "failure_hours": failure_count,
        "risk_level": "CRITICAL" if failure_count > 3 else "STABLE"
    }