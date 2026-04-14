import pandas as pd
import numpy as np
import os

def generate_processed_data(input_filename='ev_charging_patterns.csv'):
    raw_path = os.path.join('data', 'raw', input_filename)
    processed_path = os.path.join('data', 'processed', 'processed_data.csv')

    print(f"Reading from: {raw_path}")
    df = pd.read_csv(raw_path)

    # 1. Cleaning & Formatting
    df['Charging Start Time'] = pd.to_datetime(df['Charging Start Time'])
    
    # 2. Feature Engineering: Time-based
    df['Hour'] = df['Charging Start Time'].dt.hour
    df['Day_of_Week'] = df['Charging Start Time'].dt.day_name()
    df['Is_Weekend'] = df['Charging Start Time'].dt.dayofweek >= 5

    # 3. Aggregating by Station and Hour to find "Patterns"
    processed = df.groupby(['Charging Station ID', 'Charging Station Location', 'Hour', 'Day_of_Week']).agg({
        'Energy Consumed (kWh)': 'sum',
        'User ID': 'count',           # Number of vehicles in that hour
        'Temperature (°C)': 'mean',
        'Charging Duration (hours)': 'mean'
    }).reset_index()

    processed.rename(columns={'User ID': 'Vehicle_Count'}, inplace=True)

    # 4. The "Infrastructure Stress Score" (Target Variable)
    # We normalize these to create a score between 0 and 100
    # Higher score = Station is struggling/Needs expansion
    max_energy = processed['Energy Consumed (kWh)'].max()
    max_vehicles = processed['Vehicle_Count'].max()

    processed['Load_Score'] = (
        (processed['Energy Consumed (kWh)'] / max_energy) * 50 + 
        (processed['Vehicle_Count'] / max_vehicles) * 50
    ).round(2)

    os.makedirs(os.path.dirname(processed_path), exist_ok=True)
    processed.to_csv(processed_path, index=False)
    print(f"✅ Success! Processed data saved to: {processed_path}")
    return processed

if __name__ == "__main__":
    generate_processed_data()