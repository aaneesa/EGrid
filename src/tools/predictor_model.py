import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_absolute_error, r2_score
from sklearn.preprocessing import StandardScaler
import joblib
import os

def train_demand_model():
    df = pd.read_csv('data/processed/processed_data.csv')

    # 1. LOG TRANSFORMATION (The #1 fix for negative R2)
    # This compresses large outliers and makes the distribution more "Normal"
    y = np.log1p(df['Load_Score']) 

    # 2. FEATURE ENGINEERING (Simplifying for a small dataset)
    df['Day_Numeric'] = pd.factorize(df['Day_of_Week'])[0]
    
    # Peak hours: 8-10 AM and 5-8 PM
    df['Is_Peak'] = df['Hour'].apply(lambda x: 1 if (8 <= x <= 10 or 17 <= x <= 20) else 0)

    X = df[['Hour', 'Day_Numeric', 'Temperature (°C)', 'Is_Peak']]

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    # 3. CONSTRAINED RANDOM FOREST
    # By limiting 'max_depth' and 'min_samples_leaf', we stop the model from 
    # memorizing noise (which is what causes negative R2)
    model = RandomForestRegressor(
        n_estimators=150,
        max_depth=6,             
        min_samples_leaf=5,       
        random_state=42,
        n_jobs=-1
    )
    
    model.fit(X_train, y_train)

    # 4. INVERSE TRANSFORM FOR EVALUATION
    # We must turn the Log values back into real Load Scores to evaluate
    log_preds = model.predict(X_test)
    predictions = np.expm1(log_preds)
    y_test_original = np.expm1(y_test)

    mae = mean_absolute_error(y_test_original, predictions)
    r2 = r2_score(y_test_original, predictions)

    print(f"--- 🛠️ OPTIMIZED RANDOM FOREST EVALUATION ---")
    print(f"Mean Absolute Error: {mae:.2f}")
    print(f"R2 Score: {r2:.4f}")

    # Save
    os.makedirs('src/models', exist_ok=True)
    joblib.dump(model, 'src/models/demand_predictor.pkl')
    print("✅ Optimized Random Forest Model saved.")

if __name__ == "__main__":
    train_demand_model()