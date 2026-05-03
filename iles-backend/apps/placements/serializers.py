from rest_framework import serializers

from apps.users.models import User
from apps.common.choices import Role

from .models import InternshipPlacement


class PlacementSerializer(serializers.ModelSerializer):
    student_name = serializers.CharField(source="student.full_name", read_only=True)
    workplace_supervisor_name = serializers.CharField(
        source="workplace_supervisor.full_name", read_only=True
    )
    academic_supervisor_name = serializers.CharField(
        source="academic_supervisor.full_name", read_only=True
    )

    class Meta:
        model = InternshipPlacement
        fields = [
            "id",
            "student", "student_name",
            "workplace_supervisor", "workplace_supervisor_name",
            "academic_supervisor", "academic_supervisor_name",
            "company_name", "company_address", "company_contact",
            "start_date", "end_date", "weekly_log_deadline_day",
            "status", "created_at", "updated_at",
        ]
        read_only_fields = ["id", "created_at", "updated_at"]

    def validate(self, attrs):
        student = attrs.get("student") or getattr(self.instance, "student", None)
        ws = attrs.get("workplace_supervisor") or getattr(
            self.instance, "workplace_supervisor", None
        )
        acad = attrs.get("academic_supervisor") or getattr(
            self.instance, "academic_supervisor", None
        )

        if student and student.role != Role.STUDENT:
            raise serializers.ValidationError({"student": "User must have role 'student'."})
        if ws and ws.role != Role.WORKPLACE_SUPERVISOR:
            raise serializers.ValidationError(
                {"workplace_supervisor": "User must be a workplace supervisor."}
            )
        if acad and acad.role != Role.ACADEMIC_SUPERVISOR:
            raise serializers.ValidationError(
                {"academic_supervisor": "User must be an academic supervisor."}
            )

        start = attrs.get("start_date") or getattr(self.instance, "start_date", None)
        end = attrs.get("end_date") or getattr(self.instance, "end_date", None)
        if start and end and start > end:
            raise serializers.ValidationError(
                {"end_date": "End date cannot be before start date."}
            )

        return attrs
