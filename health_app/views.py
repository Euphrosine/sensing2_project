from django.shortcuts import render
from django.http import JsonResponse
from .models import HealthData
from django.utils import timezone


# Create your views here.
# http://127.0.0.1:8000/chart_data/?temperature=15&current=16&vibration=18&speed=20
def chart_data_view(request):
    temperature = request.GET.get('temperature', None)
    current = request.GET.get('current', None)
    vibration = request.GET.get('vibration', None)
    speed = request.GET.get('speed', None)
  

    # Create a dictionary to store the data you want to save
    data_to_save = {
        'timestamp': timezone.now(),
        'temperature': temperature,
        'current': current,
        'vibration': vibration,
        'speed': speed,
    }

    # Remove None values from the dictionary
    data_to_save = {k: v for k, v in data_to_save.items() if v is not None}

    # Create a new entry in the database using the data
    HealthData.objects.create(**data_to_save)

    return JsonResponse({"message": "Data saved successfully"})

def display_chart_data(request):
    health_data = HealthData.objects.all()
    return render(request, 'health_app/chart_data_view.html', {'health_data': health_data})


#charts
def chart_view(request):
    # Get the data for each field
    temperature_data = HealthData.objects.values_list('timestamp', 'temperature')
    current_data = HealthData.objects.values_list('timestamp', 'current')
    vibration_data = HealthData.objects.values_list('timestamp', 'vibration')
    speed_data = HealthData.objects.values_list('timestamp', 'speed')

    # Prepare the data in a format suitable for Chart.js
    temperature_labels = [entry[0].strftime('%H:%M:%S') for entry in temperature_data]
    temperature_values = [entry[1] for entry in temperature_data]

    current_labels = [entry[0].strftime('%H:%M:%S') for entry in current_data]
    current_values = [entry[1] for entry in current_data]

    vibration_labels = [entry[0].strftime('%H:%M:%S') for entry in vibration_data]
    vibration_values = [entry[1] for entry in vibration_data]

    speed_labels = [entry[0].strftime('%H:%M:%S') for entry in speed_data]
    speed_values = [entry[1] for entry in speed_data]

    # Get the table data for each field
    temperature_data = HealthData.objects.all()
    current_data = HealthData.objects.all()
    vibration_data = HealthData.objects.all()
    speed_data = HealthData.objects.all()

    return render(request, 'health_app/table-chart.html', {
        'temperature_labels': temperature_labels,
        'temperature_values': temperature_values,
        'current_labels': current_labels,
        'current_values': current_values,
        'vibration_labels': vibration_labels,
        'vibration_values': vibration_values,
        'speed_labels': speed_labels,
        'speed_values': speed_values,

        #for tables
        'temperature_data': temperature_data,
        'current_data': current_data,
        'vibration_data': vibration_data,
        'speed_data': speed_data,
    })



