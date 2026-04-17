import joblib
import pandas as pd
import os
from langchain.tools import tool

# Internal logic function (Callable by other Python scripts)
def get_prediction_logic(hour: int, day: str, temp: int, location: str = "Chicago"):
    model_path = 'src/models/demand_predictor.pkl'
    if not os.path.exists(model_path):
        return {"error": "Model file not found."}

    model = joblib.load(model_path)

    day_map = {'Monday': 0, 'Tuesday': 1, 'Wednesday': 2, 'Thursday': 3, 
               'Friday': 4, 'Saturday': 5, 'Sunday': 6}
    day_numeric = day_map.get(day, 0)
    loc_map = {'Chicago': 0, 'Houston': 1, 'New York': 2, 'San Francisco': 3, 'Los Angeles': 4}
    location_numeric = loc_map.get(location, 0)
    is_peak = 1 if (8 <= hour <= 10 or 17 <= hour <= 20) else 0
    forecasted_energy = 50.0 

    input_data = pd.DataFrame([[
        hour, day_numeric, temp, is_peak, location_numeric, forecasted_energy
    ]], columns=['Hour', 'Day_Numeric', 'Temperature (°C)', 'Is_Peak', 'Location_Numeric', 'Forecasted_Energy'])

    prediction = model.predict(input_data)[0]
    return float(round(prediction, 2))

# Tool wrapper (Callable by the AI Agent)
@tool
def station_load_analyst(hour: int, day: str, temp: int, location: str = "Chicago"):
    """
    Predicts the EV charging station load score (0-100) based on time and weather.
    Use this tool to analyze current or predicted demand.
    """
    return get_prediction_logic(hour, day, temp, location)