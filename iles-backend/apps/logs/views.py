from rest_framework import permissions, status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import WeeklyLog
from .serializers import ReviewSerializer, SubmitSerializer, WeeklyLogSerializer
from .validators import validate_transition
from apps.common.choices import ROLE_COORDINATOR, ROLE_STUDENT, ROLE_SUPERVISOR

class WeeklyLogViewSet(viewsets.ModelViewSet):
    queryset = WeeklyLog.objects.select_related('student', 'placement').all()
    serializer_class = WeeklyLogSerializer
    permission_classes = [permissions.IsAuthenticated]
    search_fields = ['title', 'student__full_name', 'placement__company_name', 'status']
    ordering_fields = ['week_number', 'created_at', 'status']

    def get_queryset(self):
        user = self.request.user
        qs = super().get_queryset()
        if user.role == ROLE_STUDENT:
            return qs.filter(student=user)
        return qs

    def perform_create(self, serializer):
        user = self.request.user
        if user.role == ROLE_STUDENT:
            serializer.save(student=user)
        else:
            serializer.save()

    @action(detail=True, methods=['post'])
    def submit(self, request, pk=None):
        log = self.get_object()
        validate_transition(log.status, 'submitted')
        serializer = SubmitSerializer(data=request.data, context={'log': log})
        serializer.is_valid(raise_exception=True)
        log.mark_submitted()
        return Response(WeeklyLogSerializer(log).data)

    @action(detail=True, methods=['post'])
    def review(self, request, pk=None):
        log = self.get_object()
        if request.user.role not in [ROLE_SUPERVISOR, ROLE_COORDINATOR]:
            return Response({'detail': 'Only supervisors/coordinators can review logs.'}, status=403)
        validate_transition(log.status, 'reviewed')
        serializer = ReviewSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        log.mark_reviewed(serializer.validated_data.get('feedback', ''))
        return Response(WeeklyLogSerializer(log).data)

    @action(detail=True, methods=['post'])
    def approve(self, request, pk=None):
        log = self.get_object()
        if request.user.role not in [ROLE_SUPERVISOR, ROLE_COORDINATOR]:
            return Response({'detail': 'Only supervisors/coordinators can approve logs.'}, status=403)
        validate_transition(log.status, 'approved')
        log.mark_approved()
        return Response(WeeklyLogSerializer(log).data)

    @action(detail=True, methods=['post'], url_path='request-revision')
    def request_revision(self, request, pk=None):
        log = self.get_object()
        if request.user.role not in [ROLE_SUPERVISOR, ROLE_COORDINATOR]:
            return Response({'detail': 'Only supervisors/coordinators can request revision.'}, status=403)
        validate_transition(log.status, 'draft')
        serializer = ReviewSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        log.request_revision(serializer.validated_data.get('feedback', ''))
        return Response(WeeklyLogSerializer(log).data)
