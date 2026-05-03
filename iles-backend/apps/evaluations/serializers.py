from rest_framework import serializers

from .models import Evaluation, EvaluationCriterion
from .scoring import (
    COMMUNICATION_WEIGHT,
    PROFESSIONALISM_WEIGHT,
    TECHNICAL_WEIGHT,
)


class EvaluationCriterionSerializer(serializers.ModelSerializer):
    class Meta:
        model = EvaluationCriterion
        fields = ["id", "name", "description", "weight_percent", "is_active"]


class EvaluationSerializer(serializers.ModelSerializer):
    student_name = serializers.CharField(
        source="weekly_log.student.full_name", read_only=True
    )
    week_number = serializers.IntegerField(
        source="weekly_log.week_number", read_only=True
    )
    evaluator_name = serializers.CharField(
        source="evaluator.full_name", read_only=True
    )

    class Meta:
        model = Evaluation
        fields = [
            "id", "weekly_log", "week_number", "student_name",
            "evaluator", "evaluator_name",
            "technical_skills", "communication", "professionalism",
            "total_score", "remarks", "created_at",
        ]
        read_only_fields = ["id", "evaluator", "evaluator_name", "total_score", "created_at"]


class CreateEvaluationSerializer(serializers.Serializer):
    weekly_log = serializers.IntegerField()
    technical_skills = serializers.IntegerField(min_value=0, max_value=100)
    communication = serializers.IntegerField(min_value=0, max_value=100)
    professionalism = serializers.IntegerField(min_value=0, max_value=100)
    remarks = serializers.CharField(required=False, allow_blank=True)


class WeightsSerializer(serializers.Serializer):
    """Read-only view of the canonical weights — used by the frontend
    so the UI label can never drift out of sync with the formula."""
    technical_skills = serializers.DecimalField(max_digits=3, decimal_places=2)
    communication = serializers.DecimalField(max_digits=3, decimal_places=2)
    professionalism = serializers.DecimalField(max_digits=3, decimal_places=2)

    @classmethod
    def current(cls):
        return {
            "technical_skills": TECHNICAL_WEIGHT,
            "communication": COMMUNICATION_WEIGHT,
            "professionalism": PROFESSIONALISM_WEIGHT,
        }
