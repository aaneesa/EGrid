from typing import TypedDict, Annotated, List
import operator

class AgentState(TypedDict):
    # Input from the user/telemetry
    station_id: str
    city: str
    hour: int
    day: str
    temp: float
    
    # Processed Data
    predicted_load: float
    retrieved_rules: str
    
    # Final Output
    final_recommendation: str