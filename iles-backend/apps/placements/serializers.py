from rest_framework import serializers
from .models import InternshipPlacement

class InternshipPlacementSerializer(serializers.ModelSerializer):
    student_name = serializers.CharField(source='student.full_name', read_only=True)

    class Meta:
        model = InternshipPlacement
        fields = ['id', 'student', 'student_name', 'company_name', 'company_address', 'supervisor_name', 'supervisor_email', 'start_date', 'end_date', 'status', 'created_at']
