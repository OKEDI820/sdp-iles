from rest_framework import permissions, viewsets
from .models import Evaluation, EvaluationCriteria
from .serializers import EvaluationCriteriaSerializer, EvaluationSerializer
from apps.common.choices import ROLE_COORDINATOR, ROLE_SUPERVISOR

class EvaluationViewSet(viewsets.ModelViewSet):
    queryset = Evaluation.objects.select_related('weekly_log', 'weekly_log__student', 'evaluator').all().order_by('-created_at')
    serializer_class = EvaluationSerializer
    permission_classes = [permissions.IsAuthenticated]
    search_fields = ['weekly_log__student__full_name', 'remarks']

    def get_queryset(self):
        user = self.request.user
        qs = super().get_queryset()
        if user.role == 'student':
            return qs.filter(weekly_log__student=user)
        return qs

    def perform_create(self, serializer):
        serializer.save(evaluator=self.request.user)

class EvaluationCriteriaViewSet(viewsets.ModelViewSet):
    queryset = EvaluationCriteria.objects.all().order_by('id')
    serializer_class = EvaluationCriteriaSerializer
    permission_classes = [permissions.IsAuthenticated]
