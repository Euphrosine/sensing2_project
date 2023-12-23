from django.shortcuts import render
from django.http import JsonResponse
from .models import HealthData
import joblib
import pandas as pd

from django.utils import timezone
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt

from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from .serializers import MotorRecommendationInputSerializer
from rest_framework.exceptions import ValidationError
import pandas as pd
import pickle

from health_app import serializers


@csrf_exempt

def prediction_view(request):
    template_name = 'health_app/prediction.html'

    if request.method == 'POST':
        # Load the pre-trained model
        clf = joblib.load('ml_models/romeo_motor_model.joblib')

        # Create a dictionary to map system conditions to human-readable recommendations
        condition_to_recommendation = {
            'Normal': "Maintain your system condition. It's good!",
            'Pre-Failure': "System condition is in a pre-failure state. Consider preventive maintenance.",
            'Failure': "System condition has failed. Immediate action is required."
        }

        # Set the safe ranges for motor specifications
        safe_ranges = {
            'Current 1': {'min': 2, 'max': 20},
            'Current 2': {'min': 2, 'max': 20},
            'Current 3': {'min': 2, 'max': 20},
            'Temperature': {'min': 25, 'max': 90},
            'Speed': {'min': 600, 'max': 1800},
            'Vibration': {'min': 0, 'max': 1}
        }

        # Get the latest health data from the database
        latest_health_data = HealthData.objects.last()

        if latest_health_data:
            # Use the latest health data for prediction
            user_input = {
                'Current 1': latest_health_data.current1,
                'Current 2': latest_health_data.current2,
                'Current 3': latest_health_data.current3,
                'Temperature': latest_health_data.temperature,
                'Speed': latest_health_data.speed,
                'Vibration': latest_health_data.vibration,
            }

            # Create a DataFrame with the user input
            user_input_df = pd.DataFrame([user_input], columns=safe_ranges.keys())

            # Make prediction using the trained model
            prediction = clf.predict(user_input_df)

            # Get the recommendation based on the predicted system condition
            recommendation = condition_to_recommendation.get(prediction[0], "Invalid system condition.")

            # Pass the prediction and recommendation to the template
            context = {
                'prediction': prediction[0],
                'recommendation': recommendation,
            }

            return render(request, template_name, context)
        else:
            return render(request, template_name, {'prediction': 'No data available', 'recommendation': 'No data available'})

    return render(request, template_name)


# http://127.0.0.1:8000/api/?temperature=15&current1=16&current2=20&current3=14&vibration=18&speed=20
def chart_data_view(request):
    temperature = request.GET.get('temperature', None)
    current1 = request.GET.get('current1', None)
    current2 = request.GET.get('current2', None)
    current3 = request.GET.get('current3', None)
    vibration = request.GET.get('vibration', None)
    speed = request.GET.get('speed', None)
  

    # Create a dictionary to store the data you want to save
    data_to_save = {
        'timestamp': timezone.now(),
        'temperature': temperature,
        'current1': current1,
        'current2': current2,
        'current3': current3,
        'vibration': vibration,
        'speed': speed,
    }

    # Remove None values from the dictionary
    data_to_save = {k: v for k, v in data_to_save.items() if v is not None}

    # Create a new entry in the database using the data
    HealthData.objects.create(**data_to_save)

    return JsonResponse({"message": "Data saved successfully"})

#to help in prediction
def latest_health_data(request):
    latest_health_data = HealthData.objects.last()

    if latest_health_data:
        data = {
            'temperature': latest_health_data.temperature,
            'current1': latest_health_data.current1,
            'current2': latest_health_data.current2,
            'current3': latest_health_data.current3,
            'vibration': latest_health_data.vibration,
            'speed': latest_health_data.speed,
        }
        return JsonResponse(data)
    else:
        return JsonResponse({'message': 'No health data available'})

#rendering data from database
def display_chart_data(request):
    health_data = HealthData.objects.all()

    return render(request, 'health_app/chart_data_view.html', {'health_data': health_data})


#charts
def chart_view(request):
    # Get the data for each field
    temperature_data = HealthData.objects.values_list('timestamp', 'temperature')
    current1_data = HealthData.objects.values_list('timestamp', 'current1')
    current2_data = HealthData.objects.values_list('timestamp', 'current2')
    current3_data = HealthData.objects.values_list('timestamp', 'current3')
    vibration_data = HealthData.objects.values_list('timestamp', 'vibration')
    speed_data = HealthData.objects.values_list('timestamp', 'speed')

    # Prepare the data in a format suitable for Chart.js
    temperature_labels = [entry[0].strftime('%H:%M:%S') for entry in temperature_data]
    temperature_values = [entry[1] for entry in temperature_data]

    current1_labels = [entry[0].strftime('%H:%M:%S') for entry in current1_data]
    current1_values = [entry[1] for entry in current1_data]

    current2_labels = [entry[0].strftime('%H:%M:%S') for entry in current2_data]
    current2_values = [entry[1] for entry in current2_data]

    current3_labels = [entry[0].strftime('%H:%M:%S') for entry in current3_data]
    current3_values = [entry[1] for entry in current3_data]

    vibration_labels = [entry[0].strftime('%H:%M:%S') for entry in vibration_data]
    vibration_values = [entry[1] for entry in vibration_data]

    speed_labels = [entry[0].strftime('%H:%M:%S') for entry in speed_data]
    speed_values = [entry[1] for entry in speed_data]

    # Get the table data for each field
    temperature_data = HealthData.objects.all()
    current1_data = HealthData.objects.all()
    current2_data = HealthData.objects.all()
    current3_data = HealthData.objects.all()
    vibration_data = HealthData.objects.all()
    speed_data = HealthData.objects.all()

    return render(request, 'health_app/table-chart.html', {
        'temperature_labels': temperature_labels,
        'temperature_values': temperature_values,
        'current1_labels': current1_labels,
        'current1_values': current1_values,
        'current2_labels': current2_labels,
        'current2_values': current2_values,
        'current3_labels': current3_labels,
        'current3_values': current3_values,
        'vibration_labels': vibration_labels,
        'vibration_values': vibration_values,
        'speed_labels': speed_labels,
        'speed_values': speed_values,

        #for tables
        'temperature_data': temperature_data,
        'current1_data': current1_data,
        'current2_data': current2_data,
        'current3_data': current3_data,
        'vibration_data': vibration_data,
        'speed_data': speed_data,
    })


def displayApi(request):
    return render(request,'health_app/display.html')


from rest_framework.exceptions import ValidationError

class MotorRecommendationAPIView(APIView):
    def post(self, request, format=None):
        try:
            # Load the saved model
            with open('health_app/romeoModel/motor_recommendation.pkl', 'rb') as f:
                best_model, make_recommendation, labelencoder = pickle.load(f)

            # Check if the incoming data is a list or a dictionary
            input_data = request.data

            if isinstance(input_data, list):
                # Deserialize input data as a list of dictionaries
                serializer = MotorRecommendationInputSerializer(data=input_data, many=True)
            elif isinstance(input_data, dict):
                # If a single item is sent, wrap it in a list
                serializer = MotorRecommendationInputSerializer(data=[input_data])
            else:
                raise ValidationError("Invalid input format")

            serializer.is_valid(raise_exception=True)

            # Extract the first item in the input list
            first_input = serializer.validated_data[0]

            # Convert input data to a DataFrame
            inputs_df = pd.DataFrame(serializer.validated_data)

            # Get list of inputs for each row
            model_pred = best_model.predict(inputs_df)
            inputs = inputs_df.values.tolist()

            # Decode the predicted values
            recommendations = make_recommendation(inputs, model_pred, labelencoder)

            # Prepare the response for the first item in the input list
            response_data = {
                "first_input": first_input,
                "prediction": model_pred[0].tolist(),  # Convert NumPy array to list
                "recommendation": recommendations[0]
            }

            return Response(response_data, status=status.HTTP_200_OK)

        except ValidationError as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


# class MotorRecommendationAPIView(APIView):
#     def post(self, request, format=None):
#         try:
#             # Load the saved model
#             with open('health_app/romeoModel/motor_recommendation.pkl', 'rb') as f:
#                 best_model, make_recommendation, labelencoder = pickle.load(f)

#             # Deserialize input data as a list of dictionaries
#             input_data = request.data
#             serializer = MotorRecommendationInputSerializer(data=input_data, many=True)
#             serializer.is_valid(raise_exception=True)

#             # Convert input data to a DataFrame
#             inputs_df = pd.DataFrame(serializer.validated_data)

#             # Get list of inputs for each row
#             model_pred = best_model.predict(inputs_df)
#             inputs = inputs_df.values.tolist()

#             # Decode the predicted values
#             recommendations = make_recommendation(inputs, model_pred, labelencoder)

#             # Prepare the response
#             response_data = {
#                 "inputs": inputs,
#                 "recommendations": recommendations
#             }

#             return Response(response_data, status=status.HTTP_200_OK)

#         except Exception as e:
#             return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

