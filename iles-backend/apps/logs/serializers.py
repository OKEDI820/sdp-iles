from rest_framework import serializers
from .models import WeeklyLog
from .validators import validate_deadline

class WeeklyLogSerializer(serializers.ModelSerializer):
    student_name = serializers.CharField(source='student.full_name', read_only=True)
    placement_name = serializers.CharField(source='placement.company_name', read_only=True)

    class Meta:
        model = WeeklyLog
        fields = [
            'id', 'student', 'student_name', 'placement', 'placement_name', 'week_number', 'title',
            'activities', 'challenges', 'lessons_learned', 'date_from', 'date_to', 'submission_deadline',
            'status', 'feedback', 'submitted_at', 'reviewed_at', 'approved_at', 'created_at', 'updated_at'
        ]
        read_only_fields = ['status', 'feedback', 'submitted_at', 'reviewed_at', 'approved_at']

    def validate(self, attrs):
        instance = getattr(self, 'instance', None)
        if instance and instance.status == 'approved':
            raise serializers.ValidationError('Approved logs cannot be edited.')
        if attrs.get('date_from') and attrs.get('date_to') and attrs['date_from'] > attrs['date_to']:
            raise serializers.ValidationError('date_from cannot be after date_to.')
        return attrs

class ReviewSerializer(serializers.Serializer):
    feedback = serializers.CharField(required=False, allow_blank=True)

class SubmitSerializer(serializers.Serializer):
    def validate(self, attrs):
        validate_deadline(self.context['log'].submission_deadline)
        return attrs
