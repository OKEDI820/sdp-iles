from rest_framework import serializers
from .models import WeeklyLog
from .validators import validate_deadline

class WeeklyLogSerializer(serializers.ModelSerializer):
    student_name = serializers.CharField(source='student.full_name', read_only=True)
    company_name = serializers.CharField(source='placement.company_name', read_only=True)
    
    # FIELD NAME MAPPINGS FOR FRONTEND COMPATIBILITY
    week_start = serializers.DateField(source='date_from', write_only=True)
    week_end = serializers.DateField(source='date_to', write_only=True)
    
    # READ-ONLY OUTPUT FIELDS
    week_start_read = serializers.DateField(source='date_from', read_only=True)
    week_end_read = serializers.DateField(source='date_to', read_only=True)
    
    reviewed_by_name = serializers.CharField(
        source='reviewed_by.full_name',
        read_only=True,
        allow_null=True
    )
    approved_by_name = serializers.CharField(
        source='approved_by.full_name',
        read_only=True,
        allow_null=True
    )

    class Meta:
        model = WeeklyLog
        fields = [
            'id', 'student', 'student_name', 'placement', 'company_name',
            'week_number', 'title', 'activities', 'challenges', 'lessons_learned',
            'week_start', 'week_start_read', 'week_end', 'week_end_read',
            'submission_deadline', 'status',
            'review_feedback', 'rejection_reason', 'revision_request',
            'submitted_at', 'reviewed_at', 'reviewed_by', 'reviewed_by_name',
            'approved_at', 'approved_by', 'approved_by_name', 'rejected_at',
            'created_at', 'updated_at'
        ]
        read_only_fields = [
            'id', 'student_name', 'company_name', 'status',
            'week_start_read', 'week_end_read',
            'review_feedback', 'rejection_reason', 'revision_request',
            'submitted_at', 'reviewed_at', 'reviewed_by', 'reviewed_by_name',
            'approved_at', 'approved_by', 'approved_by_name', 'rejected_at',
            'created_at', 'updated_at'
        ]

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