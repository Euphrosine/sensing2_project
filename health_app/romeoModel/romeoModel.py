import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, classification_report
import joblib

# Load the dataset
dataset_path = 'D:/python_codes/romeoModel/motor_dataset_Romeo.csv'
df = pd.read_csv(dataset_path)

# Separate features (X) and labels (y)
X = df[['current', 'speed', 'temperature', 'vibration']]
y = df['system_condition']

# Split the dataset into training and testing sets
X_train_full, X_test, y_train_full, y_test = train_test_split(X, y, test_size=0.2, random_state=42, stratify=y)

# Create a Random Forest classifier
clf = RandomForestClassifier(n_estimators=100, random_state=42)

# Train the classifier on the full dataset
clf.fit(X_train_full, y_train_full)

# Save the trained model
joblib.dump(clf, 'random_forest_model_full.joblib')

# Make predictions on the test set
y_pred = clf.predict(X_test)

# Evaluate the classifier on the test set
accuracy = accuracy_score(y_test, y_pred)
classification_report_text = classification_report(y_test, y_pred)

# Print the results
print('Accuracy:', accuracy)
print('Classification Report (Test Set):')
print(classification_report_text)

# Evaluate the classifier on the full dataset
y_full_pred = clf.predict(X)

# Print the results for the full dataset
full_dataset_accuracy = accuracy_score(y, y_full_pred)
full_dataset_classification_report = classification_report(y, y_full_pred)

print('\nAccuracy on Full Dataset:', full_dataset_accuracy)
print('Classification Report (Full Dataset):')
print(full_dataset_classification_report)
