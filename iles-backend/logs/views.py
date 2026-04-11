from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from .models import WeeklyLog
from .serializers import WeeklyLogSerializer

class WeeklyLogViewSet(viewsets.ModelViewSet):
    queryset = WeeklyLog.objects.all().order_by("-created_at")
    serializer_class = WeeklyLogSerializer
    permission_classes = [IsAuthenticated]
