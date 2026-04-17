import joblib
import pandas as pd
import numpy as np
import os

def predict_station_load(hour, day, temp, location="Chicago"):
    """
    Wrapper for the XGBoost model that matches the training feature engineering.
    """
    model_path = 'src/models/demand_predictor.pkl'
    
    if not os.path.exists(model_path):
        return {"error": "Model file not found. Run training script first."}

    model = joblib.load(model_path)

    # 1. Replicate Feature Engineering from your training code
    # Day Mapping (matching pd.factorize logic typically used in your dataset)
    day_map = {'Monday': 0, 'Tuesday': 1, 'Wednesday': 2, 'Thursday': 3, 
               'Friday': 4, 'Saturday': 5, 'Sunday': 6}
    day_numeric = day_map.get(day, 0)

    # Location Mapping
    loc_map = {'Chicago': 0, 'Houston': 1, 'New York': 2, 'San Francisco': 3, 'Los Angeles': 4}
    location_numeric = loc_map.get(location, 0)
    
    # Peak hours: 8-10 AM and 5-8 PM (matching your apply logic)
    is_peak = 1 if (8 <= hour <= 10 or 17 <= hour <= 20) else 0

    # Forecasted Energy Simulation
    # Since we are predicting the FUTURE, we simulate the energy demand 
    # based on typical station capacity (e.g., a 50kWh draw)
    forecasted_energy = 50.0 

    # 2. Create DataFrame with EXACT feature order as training
    # Features: ['Hour', 'Day_Numeric', 'Temperature (°C)', 'Is_Peak', 'Location_Numeric', 'Forecasted_Energy']
    input_data = pd.DataFrame([[
        hour, 
        day_numeric, 
        temp, 
        is_peak, 
        location_numeric, 
        forecasted_energy
    ]], columns=['Hour', 'Day_Numeric', 'Temperature (°C)', 'Is_Peak', 'Location_Numeric', 'Forecasted_Energy'])

    # 3. Predict
    prediction = model.predict(input_data)[0]
    
    return {"predicted_load_score": float(round(prediction, 2))}

if __name__ == "__main__":
    # Quick Test
    test_res = predict_station_load(19, "Saturday", -5.0, "Chicago")
    print(f"Test Prediction: {test_res}")