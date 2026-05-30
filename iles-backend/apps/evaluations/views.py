from rest_framework import permissions, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import Evaluation, EvaluationCriteria
from .serializers import EvaluationCriteriaSerializer, EvaluationSerializer
from apps.common.choices import (
    ROLE_ACADEMIC_SUPERVISOR, ROLE_ADMIN,
    ROLE_WORKPLACE_SUPERVISOR,
)


class EvaluationViewSet(viewsets.ModelViewSet):
    queryset = Evaluation.objects.select_related(
        'weekly_log', 'weekly_log__student', 'evaluator'
    ).all().order_by('-created_at')
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

    @action(detail=False, methods=['get'])
    def weights(self, request):
        """
        Return the active scoring weights so the frontend can display
        the formula: Total = tech × w1 + comm × w2 + prof × w3
        """
        criteria = EvaluationCriteria.objects.filter(is_active=True)
        if criteria.exists():
            data = {c.name.lower().replace(' ', '_'): str(c.weight) for c in criteria}
        else:
            # Default weights matching scoring.py
            data = {
                'technical_skills':  '0.40',
                'communication':     '0.30',
                'professionalism':   '0.30',
            }
        return Response(data)
