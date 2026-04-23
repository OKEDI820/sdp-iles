from rest_framework import serializers


class DashboardSummarySerializer(serializers.Serializer):
    total_users = serializers.IntegerField(),
    total_placements = serializers.IntegerField() 
    total_logs = serializers.IntegerField()
    draft_logs = serializers.IntegerField()
    submitted_logs = serializers.IntegerField()
    reviewed_logs = serializers.IntegerField()
    approved_logs = serializers.IntegerField()
    total_evaluations = serializers.IntegerField()
    average_score = serializers.FloatField()



