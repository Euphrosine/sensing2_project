# Test the usage og saved model
import pickle
import pandas as pd
# from health_app.romeoModel.utils import make_recommendation


with open('saved_models/motor_recommendation.pkl', 'rb') as f:
    best_model, make_recommendation, labelencoder = pickle.load(f)
print("Model loaded successfully.")
column_names = ['current_1_lebelling','current_2_lebelling','current_3_lebelling','temperature','speed','vibration']
inputs_test = pd.DataFrame([[1,1,2,3,2,3],[1,1,2,2,2,2]],columns=column_names)
# Get list of inputs fro each row
model_pred_test = best_model.predict(inputs_test)
inputs = inputs_test.values.tolist()
print(inputs)
# Decode the predicted values
recommendations = make_recommendation(inputs,model_pred_test,labelencoder)
print(recommendations)