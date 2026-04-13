from rest_framework import permissions, viewsets
from .models import InternshipPlacement
from .serializers import InternshipPlacementSerializer
from apps.common.choices import *

class InternshipPlacementViewSet(viewsets.ModelViewSet):
    queryset = InternshipPlacement.objects.select_related('student').all().order_by('-created_at')
    serializer_class = InternshipPlacementSerializer
    permission_classes = [permissions.IsAuthenticated]
    search_fields = ['company_name', 'supervisor_name', 'student__full_name']

    def get_queryset(self):
        user = self.request.user
        qs = super().get_queryset()
        if user.role == ROLE_STUDENT:
            return qs.filter(student=user)
        return qs

