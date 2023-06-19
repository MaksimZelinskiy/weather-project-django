from rest_framework import serializers

from .models import Weather_info


class Weather_serializer(serializers.ModelSerializer):
    class Meta:
        model = Weather_info
        fields = ('date', 'weather_description', 'temperature')