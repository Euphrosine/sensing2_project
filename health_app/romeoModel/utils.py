# Function takes the predicted values and decodes them
def make_recommendation(inputs, pred, encoder):
    decoded_preds = encoder.inverse_transform(pred)
    recommendations = []
    for readings, decoded_pred in zip(inputs, decoded_preds):
        print("Motor status: ", decoded_pred)
        current_1, current_2, current_3, temperature, speed, vibration = readings
        recommendation = {"status": decoded_pred}
        # Check the state of each feature and display the appropriate message
        if decoded_pred == 'failure':
            if current_1 == 3 or current_2 == 3 or current_3 == 3:
                recommendation["problem"] = "Overheating"
                recommendation["solution"] = "Disconnect the motor until the issue is resolved"
            elif vibration == 3:

                recommendation["problem"] = "Unfixed bolt"
                recommendation[
                    "solution"] = ("Fix the bolts and check if the rotor is balanced. If the issue persists, check the "
                                   "bearing.")
            elif temperature == 3:
                recommendation["problem"] = "Overloading"
                recommendation["solution"] = "Reduce the load on the motor."

            elif speed == 3:
                print("Low speed detected. Please check if the motor is working on the rated speed")
                recommendation["problem"] = "Low speed"
                recommendation["solution"] = "Reduce the load or check if the motor is stopped."

        elif decoded_pred == 'pre_failure':
            recommendation["problem"] = "Reduced efficiency"
            recommendation[
                "solution"] = "Check the bearing and the rotor. And be ready to do preventive maintenance."
        else:
            recommendation["problem"] = "None"
            recommendation["solution"] = "None"
        recommendations.append(recommendation)

    return recommendations
