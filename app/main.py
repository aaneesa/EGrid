from src.agent.graph import app
import os
from dotenv import load_dotenv

load_dotenv()

def run_egrid_agent(station_id, city, hour, day, temp):
    print(f"\n{'='*50}")
    print(f"🚀 RUNNING EGRID AGENT: {station_id} ({city})")
    print(f"{'='*50}")
    
    initial_state = {
        "station_id": station_id,
        "city": city,
        "hour": hour,
        "day": day,
        "temp": temp
    }
    
    # Run the Graph
    final_output = app.invoke(initial_state)
    
    print(final_output["final_recommendation"])

if __name__ == "__main__":
    # SCENARIO 1: Chicago Station 1 (Sub-zero temp, Likely High Load)
    # This will trigger [ARCH-COLD] and Expansion Level 3/4
    run_egrid_agent("Station_1", "Chicago", 19, "Saturday", -2.5)
    
    # SCENARIO 2: Houston Station 101 (Extreme Heat)
    # This will trigger [ARCH-HEAT] and Solar Integration priority
    run_egrid_agent("Station_101", "Houston", 14, "Wednesday", 39.0)