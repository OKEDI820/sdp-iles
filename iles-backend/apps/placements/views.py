from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated

from apps.common.choices import Role
from apps.common.permissions import IsAdmin, ReadOnly

from .models import InternshipPlacement
from .serializers import PlacementSerializer


class PlacementViewSet(viewsets.ModelViewSet):
    serializer_class = PlacementSerializer
    queryset = InternshipPlacement.objects.select_related(
        "student", "workplace_supervisor", "academic_supervisor"
    )
    permission_classes = [IsAuthenticated, IsAdmin | ReadOnly]
    filterset_fields = ["status"]
    search_fields = ["student__full_name", "company_name"]
    ordering_fields = ["start_date", "end_date", "created_at"]

    def get_queryset(self):
        qs = super().get_queryset()
        user = self.request.user
        if user.role == Role.STUDENT:
            return qs.filter(student=user)
        if user.role == Role.WORKPLACE_SUPERVISOR:
            return qs.filter(workplace_supervisor=user)
        if user.role == Role.ACADEMIC_SUPERVISOR:
            return qs.filter(academic_supervisor=user)
        # Admin sees all.
        return qs
