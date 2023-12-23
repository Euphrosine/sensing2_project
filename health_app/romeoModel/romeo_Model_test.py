import joblib
import pandas as pd
import numpy as np

# Load the trained Random Forest model
clf = joblib.load('random_forest_model_full.joblib')

# Create a dictionary to map system conditions to human-readable recommendations
condition_to_recommendation = {
    'Normal': "Maintain your current system condition. It's good!",
    'Pre-Failure': "System condition is in a pre-failure state. Consider preventive maintenance.",
    'Failure': "System condition has failed. Immediate action is required."
}

# Set the safe ranges for motor specifications
safe_ranges = {
    'current': {'min': 3, 'max': 20},
    'speed': {'min': 600, 'max': 1800},
    'temperature': {'min': 25, 'max': 90},
    'vibration': {'min': 0.1, 'max': 2}
}

# Apply tolerance to the safe ranges for user input
tolerance_percentage = 25  # You can adjust this as needed

while True:
    user_input = {}
    for param, param_range in safe_ranges.items():
        low = param_range['min'] - (tolerance_percentage / 100) * param_range['min']
        high = param_range['max'] + (tolerance_percentage / 100) * param_range['max']
        user_input[param] = float(input(f"Enter {param} ({low}-{high}): "))

    # Create a DataFrame with the user input
    user_input_df = pd.DataFrame([user_input], columns=safe_ranges.keys())

    # Make prediction using the trained model
    prediction = clf.predict(user_input_df)

    # Get the recommendation based on the predicted system condition
    recommendation = condition_to_recommendation.get(prediction[0], "Invalid system condition.")

    # Print the recommendation
    print(f"Predicted System Condition: {prediction[0]}")
    print(recommendation)
