from rest_framework import serializers

class MotorRecommendationInputSerializer(serializers.Serializer):
    current_1_lebelling = serializers.IntegerField()
    current_2_lebelling = serializers.IntegerField()
    current_3_lebelling = serializers.IntegerField()
    temperature = serializers.FloatField()
    speed = serializers.FloatField()
    vibration = serializers.FloatField()
