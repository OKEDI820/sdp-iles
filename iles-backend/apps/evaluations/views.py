from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from apps.common.choices import Role
from apps.common.permissions import IsAcademicSupervisorOrAdmin, IsAdmin, ReadOnly
from apps.logs.models import WeeklyLog

from . import services
from .models import Evaluation, EvaluationCriterion
from .serializers import (
    CreateEvaluationSerializer,
    EvaluationCriterionSerializer,
    EvaluationSerializer,
    WeightsSerializer,
)


class EvaluationCriterionViewSet(viewsets.ModelViewSet):
    """Admin-managed list of criteria. Anyone authenticated can read."""
    queryset = EvaluationCriterion.objects.all()
    serializer_class = EvaluationCriterionSerializer
    permission_classes = [IsAuthenticated, IsAdmin | ReadOnly]


class EvaluationViewSet(viewsets.ModelViewSet):
    queryset = Evaluation.objects.select_related(
        "weekly_log", "weekly_log__student", "evaluator"
    )
    serializer_class = EvaluationSerializer
    permission_classes = [IsAuthenticated]
    filterset_fields = ["weekly_log", "evaluator"]
    search_fields = ["weekly_log__student__full_name", "remarks"]
    ordering_fields = ["created_at", "total_score"]

    def get_queryset(self):
        qs = super().get_queryset()
        user = self.request.user
        if user.role == Role.STUDENT:
            return qs.filter(weekly_log__student=user)
        if user.role == Role.WORKPLACE_SUPERVISOR:
            return qs.filter(weekly_log__placement__workplace_supervisor=user)
        if user.role == Role.ACADEMIC_SUPERVISOR:
            return qs.filter(weekly_log__placement__academic_supervisor=user)
        return qs

    def get_permissions(self):
        if self.action == "create":
            return [IsAuthenticated(), IsAcademicSupervisorOrAdmin()]
        return super().get_permissions()

    def create(self, request, *args, **kwargs):
        ser = CreateEvaluationSerializer(data=request.data)
        ser.is_valid(raise_exception=True)
        try:
            log = WeeklyLog.objects.get(pk=ser.validated_data["weekly_log"])
        except WeeklyLog.DoesNotExist:
            return Response(
                {"detail": "weekly_log not found."},
                status=status.HTTP_404_NOT_FOUND,
            )

        evaluation = services.create_evaluation(
            weekly_log=log,
            evaluator=request.user,
            technical_skills=ser.validated_data["technical_skills"],
            communication=ser.validated_data["communication"],
            professionalism=ser.validated_data["professionalism"],
            remarks=ser.validated_data.get("remarks", ""),
        )
        return Response(
            EvaluationSerializer(evaluation).data, status=status.HTTP_201_CREATED
        )

    @action(detail=False, methods=["get"], url_path="weights",
            permission_classes=[IsAuthenticated])
    def weights(self, request):
        """Returns the canonical weighting so the frontend can render
        labels that can't drift from the formula."""
        return Response(WeightsSerializer(WeightsSerializer.current()).data)
