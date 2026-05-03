"""Weekly log API views.

Pattern: views are thin HTTP adapters. All workflow logic lives in
services.py. Views just:
  - parse inputs (via serializers)
  - call the appropriate service
  - serialize the result

If you find yourself writing business rules here, move them to services.
"""
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from apps.common.choices import Role

from . import services
from .models import WeeklyLog
from .serializers import (
    CreateLogSerializer,
    FeedbackSerializer,
    RejectionSerializer,
    RevisionSerializer,
    UpdateDraftSerializer,
    WeeklyLogSerializer,
)


class WeeklyLogViewSet(viewsets.ModelViewSet):
    queryset = WeeklyLog.objects.select_related(
        "student", "placement", "placement__workplace_supervisor",
        "placement__academic_supervisor", "reviewed_by", "approved_by",
    )
    permission_classes = [IsAuthenticated]
    filterset_fields = ["status", "placement", "student"]
    search_fields = ["title", "student__full_name", "placement__company_name"]
    ordering_fields = ["week_number", "submitted_at", "created_at"]

    def get_serializer_class(self):
        return {
            "create": CreateLogSerializer,
            "partial_update": UpdateDraftSerializer,
            "update": UpdateDraftSerializer,
        }.get(self.action, WeeklyLogSerializer)

    def get_queryset(self):
        """Lecture 2 NFR: a student only ever sees their own logs;
        a workplace supervisor sees only logs for placements they supervise.
        """
        qs = super().get_queryset()
        user = self.request.user
        if user.role == Role.STUDENT:
            return qs.filter(student=user)
        if user.role == Role.WORKPLACE_SUPERVISOR:
            return qs.filter(placement__workplace_supervisor=user)
        if user.role == Role.ACADEMIC_SUPERVISOR:
            return qs.filter(placement__academic_supervisor=user)
        return qs  # admin

    # ---- create / edit ----

    def create(self, request, *args, **kwargs):
        if request.user.role != Role.STUDENT:
            return Response(
                {"detail": "Only students can create logs."},
                status=status.HTTP_403_FORBIDDEN,
            )
        ser = CreateLogSerializer(data=request.data, context={"request": request})
        ser.is_valid(raise_exception=True)

        from apps.placements.models import InternshipPlacement
        try:
            placement = InternshipPlacement.objects.get(
                pk=ser.validated_data["placement"], student=request.user
            )
        except InternshipPlacement.DoesNotExist:
            return Response(
                {"detail": "Placement not found or doesn't belong to you."},
                status=status.HTTP_404_NOT_FOUND,
            )

        payload = {**ser.validated_data, "placement": placement}
        log = services.create_draft_log(student=request.user, **payload)
        return Response(
            WeeklyLogSerializer(log).data, status=status.HTTP_201_CREATED
        )

    def update(self, request, *args, **kwargs):
        return self._do_update(request, partial=False)

    def partial_update(self, request, *args, **kwargs):
        return self._do_update(request, partial=True)

    def _do_update(self, request, *, partial):
        log = self.get_object()
        ser = UpdateDraftSerializer(data=request.data, partial=partial)
        ser.is_valid(raise_exception=True)
        log = services.update_draft(log, actor=request.user, **ser.validated_data)
        return Response(WeeklyLogSerializer(log).data)

    # ---- workflow actions ----

    @action(detail=True, methods=["post"])
    def submit(self, request, pk=None):
        log = services.submit_log(self.get_object(), actor=request.user)
        return Response(WeeklyLogSerializer(log).data)

    @action(detail=True, methods=["post"])
    def review(self, request, pk=None):
        ser = FeedbackSerializer(data=request.data)
        ser.is_valid(raise_exception=True)
        log = services.review_log(
            self.get_object(),
            actor=request.user,
            feedback=ser.validated_data.get("feedback", ""),
        )
        return Response(WeeklyLogSerializer(log).data)

    @action(detail=True, methods=["post"])
    def approve(self, request, pk=None):
        log = services.approve_log(self.get_object(), actor=request.user)
        return Response(WeeklyLogSerializer(log).data)

    @action(detail=True, methods=["post"])
    def reject(self, request, pk=None):
        ser = RejectionSerializer(data=request.data)
        ser.is_valid(raise_exception=True)
        log = services.reject_log(
            self.get_object(),
            actor=request.user,
            reason=ser.validated_data["reason"],
        )
        return Response(WeeklyLogSerializer(log).data)

    @action(detail=True, methods=["post"], url_path="request-revision")
    def request_revision(self, request, pk=None):
        ser = RevisionSerializer(data=request.data)
        ser.is_valid(raise_exception=True)
        log = services.request_revision(
            self.get_object(),
            actor=request.user,
            message=ser.validated_data["message"],
        )
        return Response(WeeklyLogSerializer(log).data)
