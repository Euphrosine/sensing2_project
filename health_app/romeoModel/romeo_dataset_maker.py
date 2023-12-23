import pandas as pd
import numpy as np

# Set the safe ranges for motor specifications
safe_ranges = {
    'current': {'min': 3, 'max': 20},
    'speed': {'min': 600, 'max': 1800},
    'temperature': {'min': 25, 'max': 90},
    'vibration': {'min': 0.1, 'max': 2}
}

# Number of data points
num_data_points = 1000

# Tolerance percentage for data generation
tolerance_percentage = 25

# Random seed for reproducibility
np.random.seed(42)


# Function to generate random data for a specific label
def generate_data(label, num_points, safe_ranges, tolerance_percentage):
    data = {}
    for param, param_range in safe_ranges.items():
        min_value = param_range['min'] - (tolerance_percentage / 100) * param_range['min']
        max_value = param_range['max'] + (tolerance_percentage / 100) * param_range['max']
        data[param] = np.random.uniform(low=min_value, high=max_value, size=num_points)

    labels = np.full(num_points, label, dtype=object)  # Use dtype=object for string labels
    return pd.DataFrame({**data, 'system_condition': labels})


# Generate data for each label with the desired distribution
num_normal = num_data_points // 2
num_pre_failure = num_failure = num_data_points // 4

data_normal = generate_data('Normal', num_normal, safe_ranges, tolerance_percentage)
data_pre_failure = generate_data('Pre-Failure', num_pre_failure, safe_ranges, tolerance_percentage)
data_failure = generate_data('Failure', num_failure, safe_ranges, tolerance_percentage)

# Concatenate data for all labels
data = pd.concat([data_normal, data_pre_failure, data_failure], ignore_index=True)

# Shuffle the DataFrame to randomize the order
data = data.sample(frac=1, random_state=42).reset_index(drop=True)


# Define the conditions for each feature
def determine_condition_current(row):
    current_min = 3
    current_max = 20
    if current_min <= row['current'] <= current_max:
        return 'Normal'
    elif row['current'] > current_max:
        return 'Pre-Failure'
    else:
        return 'Failure'


def determine_condition_speed(row):
    speed_min = 600
    speed_max = 1800
    if speed_min <= row['speed'] <= speed_max:
        return 'Normal'
    elif row['speed'] > speed_max:
        return 'Pre-Failure'
    else:
        return 'Failure'


def determine_condition_temperature(row):
    temp_min = 25
    temp_max = 90
    if temp_min <= row['temperature'] <= temp_max:
        return 'Normal'
    elif row['temperature'] > temp_max:
        return 'Pre-Failure'
    else:
        return 'Failure'


def determine_condition_vibration(row):
    vibe_min = 0.1
    vibe_max = 2
    if vibe_min <= row['vibration'] <= vibe_max:
        return 'Normal'
    elif row['vibration'] > vibe_max:
        return 'Pre-Failure'
    else:
        return 'Failure'


# Apply the condition functions to create new columns for each feature
data['current_result'] = data.apply(determine_condition_current, axis=1)
data['speed_result'] = data.apply(determine_condition_speed, axis=1)
data['temperature_result'] = data.apply(determine_condition_temperature, axis=1)
data['vibration_result'] = data.apply(determine_condition_vibration, axis=1)


# Define the system_condition based on the results of individual features
def determine_system_condition(row):
    if 'Failure' in [row['current_result'], row['speed_result'], row['temperature_result'], row['vibration_result']]:
        return 'Failure'
    elif all(result == 'Normal' for result in
             [row['current_result'], row['speed_result'], row['temperature_result'], row['vibration_result']]):
        return 'Normal'
    else:
        return 'Pre-Failure'


# Apply the system_condition function to create the final label
data['system_condition'] = data.apply(determine_system_condition, axis=1)

# Save the randomized data to a CSV file
data.to_csv('D:/python_codes/romeoModel/motor_dataset_Romeo.csv', index=False)

# Display the first few rows of the randomized dataset
print("Randomized Dataset:")
print(data.head())
