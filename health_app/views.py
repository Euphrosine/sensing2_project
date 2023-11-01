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


def add_temp(request):
    return render(request,'health_app/sensor_summary.html')


