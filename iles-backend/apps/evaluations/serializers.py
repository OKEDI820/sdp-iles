from rest_framework import serializers
from .models import Evaluation, EvaluationCriteria
from .scoring import calculate_total_score

class EvaluationCriteriaSerializer(serializers.ModelSerializer):
    class Meta:
        model = EvaluationCriteria
        fields = ['id', 'name', 'weight', 'max_score', 'is_active']

class EvaluationSerializer(serializers.ModelSerializer):
    evaluator_name = serializers.CharField(source='evaluator.full_name', read_only=True)
    student_name = serializers.CharField(source='weekly_log.student.full_name', read_only=True)
    week_number = serializers.IntegerField(source='weekly_log.week_number', read_only=True)

    class Meta:
        model = Evaluation
        fields = ['id', 'weekly_log', 'week_number', 'student_name', 'evaluator', 'evaluator_name', 'technical_skills', 'communication', 'professionalism', 'total_score', 'remarks', 'created_at']
        read_only_fields = ['evaluator', 'total_score']

    def validate(self, attrs):
        for field in ['technical_skills', 'communication', 'professionalism']:
            value = attrs.get(field, getattr(self.instance, field, 0) if self.instance else 0)
            if value < 0 or value > 100:
                raise serializers.ValidationError({field: 'Scores must be between 0 and 100.'})
        return attrs

    def create(self, validated_data):
        validated_data['evaluator'] = self.context['request'].user
        validated_data['total_score'] = calculate_total_score(
            validated_data['technical_skills'],
            validated_data['communication'],
            validated_data['professionalism'],
        )
        return super().create(validated_data)

    def update(self, instance, validated_data):
        technical = validated_data.get('technical_skills', instance.technical_skills)
        communication = validated_data.get('communication', instance.communication)
        professionalism = validated_data.get('professionalism', instance.professionalism)
        validated_data['total_score'] = calculate_total_score(technical, communication, professionalism)
        return super().update(instance, validated_data)
