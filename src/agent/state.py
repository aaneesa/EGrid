from typing import TypedDict, List, Annotated
import operator

class AgentState(TypedDict):
    # Input Keys 
    task: str
    city: str
    temp: int
    hour: int
    day: str
    
    # Internal Processing Keys
    predicted_load: float
    retrieved_rules: str
    final_recommendation: str
    critic_feedback: str
    
    # History/Logs (The 'operator.add' allows agents to append to this list)
    history: Annotated[List[str], operator.add]