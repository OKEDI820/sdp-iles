from rest_framework import serializers
from .models import WeeklyLog

class WeeklyLogSerializer(serializers.ModelSerializer):
    class Meta:
        model = WeeklyLog
        fields = "__all__"

    def validate_week_number(self, value):
        if value < 1:
            raise serializers.ValidationError("Week number must be greater than 0.")
        return value
