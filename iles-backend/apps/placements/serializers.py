from rest_framework import serializers
from .models import InternshipPlacement


class InternshipPlacementSerializer(serializers.ModelSerializer):
    student_name = serializers.CharField(source='student.full_name', read_only=True)
    workplace_supervisor_name = serializers.CharField(
        source='workplace_supervisor.full_name',
        read_only=True,
        allow_null=True
    )
    academic_supervisor_name = serializers.CharField(
        source='academic_supervisor.full_name',
        read_only=True,
        allow_null=True
    )

    class Meta:
        model = InternshipPlacement
        fields = [
            'id', 'student', 'student_name',
            'company_name', 'company_address',
            'workplace_supervisor', 'workplace_supervisor_name',
            'academic_supervisor', 'academic_supervisor_name',
            'supervisor_name', 'supervisor_email',
            'start_date', 'end_date',
            'status', 'created_at'
        ]