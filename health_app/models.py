from django.db import models

# Create your models here.
class HealthData(models.Model):
    timestamp = models.DateTimeField()
    temperature = models.FloatField(null=True)
    current1 = models.FloatField(null=True)
    current2 = models.FloatField(null=True)
    current3 = models.FloatField(null=True)
    vibration = models.FloatField(null=True)
    speed = models.FloatField(null=True)
    
    def __str__(self):
      return f"Health Data - ID: {self.id}"
    

class MachineLearningPrediction(models.Model):
    timestamp = models.DateTimeField()
    prediction = models.FloatField()

