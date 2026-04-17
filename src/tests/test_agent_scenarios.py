import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

from src.agent.graph import app

def run_test_suite():
    test_cases = [
        {
            "name": "Chicago Winter Crisis",
            "input": {"station_id": "Station_1", "city": "Chicago", "hour": 18, "day": "Monday", "temp": -10, "predicted_load": 92}
        },
        {
            "name": "Houston Summer Heat",
            "input": {"station_id": "Station_101", "city": "Houston", "hour": 14, "day": "Wednesday", "temp": 40, "predicted_load": 75}
        },
        {
            "name": "NY Phantom Load Check",
            "input": {"station_id": "Station_101", "city": "New York", "hour": 2, "day": "Monday", "temp": 15, "predicted_load": 30}
        }
    ]

    for case in test_cases:
        print(f"\n🧪 TESTING SCENARIO: {case['name']}")
        # We pass the input directly to the compiled graph
        result = app.invoke(case['input'])
        print(f"RESULT:\n{result['final_recommendation']}\n")
        print("-" * 30)

if __name__ == "__main__":
    run_test_suite()