from rest_framework import serializers
from .models import Placement


class PlacementSerializer(serializers.ModelSerializer):
    class Meta:
        model = Placement
        fields = '__all__'

    def validate(self, attrs):
        start_date = attrs.get('start_date')
        end_date = attrs.get('end_date')

        if start_date and end_date and end_date < start_date:
            raise serializers.ValidationError("End date cannot be earlier than start date.")

        return attrs
