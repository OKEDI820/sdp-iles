from rest_framework import serializers

from .models import WeeklyLog


class WeeklyLogSerializer(serializers.ModelSerializer):
    student_name = serializers.CharField(source="student.full_name", read_only=True)
    company_name = serializers.CharField(source="placement.company_name", read_only=True)
    status_label = serializers.CharField(source="get_status_display", read_only=True)
    reviewed_by_name = serializers.CharField(source="reviewed_by.full_name", read_only=True)
    approved_by_name = serializers.CharField(source="approved_by.full_name", read_only=True)

    class Meta:
        model = WeeklyLog
        fields = [
            "id",
            "student", "student_name",
            "placement", "company_name",
            "week_number", "title",
            "activities", "challenges", "lessons_learned",
            "week_start", "week_end", "submission_deadline",
            "status", "status_label",
            "review_feedback", "rejection_reason", "revision_request",
            "submitted_at", "reviewed_at", "approved_at", "rejected_at",
            "reviewed_by", "reviewed_by_name",
            "approved_by", "approved_by_name",
            "created_at", "updated_at",
        ]
        read_only_fields = [
            "id", "status", "status_label", "submission_deadline",
            "review_feedback", "rejection_reason", "revision_request",
            "submitted_at", "reviewed_at", "approved_at", "rejected_at",
            "reviewed_by", "reviewed_by_name",
            "approved_by", "approved_by_name",
            "created_at", "updated_at",
        ]


class CreateLogSerializer(serializers.Serializer):
    """Used for `POST /logs/` — only fields a student fills in.

    placement is a plain int — the view validates ownership.
    """
    placement = serializers.IntegerField()
    week_number = serializers.IntegerField(min_value=1, max_value=52)
    title = serializers.CharField(max_length=200, min_length=3)
    activities = serializers.CharField(min_length=10)
    challenges = serializers.CharField(required=False, allow_blank=True)
    lessons_learned = serializers.CharField(required=False, allow_blank=True)
    week_start = serializers.DateField()
    week_end = serializers.DateField()

    def validate(self, attrs):
        if attrs["week_start"] > attrs["week_end"]:
            raise serializers.ValidationError(
                {"week_end": "Week end cannot be before week start."}
            )
        return attrs


class FeedbackSerializer(serializers.Serializer):
    feedback = serializers.CharField(required=False, allow_blank=True)


class RejectionSerializer(serializers.Serializer):
    reason = serializers.CharField(min_length=5)


class RevisionSerializer(serializers.Serializer):
    message = serializers.CharField(min_length=5)


class UpdateDraftSerializer(serializers.Serializer):
    title = serializers.CharField(max_length=200, required=False, min_length=3)
    activities = serializers.CharField(min_length=10, required=False)
    challenges = serializers.CharField(required=False, allow_blank=True)
    lessons_learned = serializers.CharField(required=False, allow_blank=True)
