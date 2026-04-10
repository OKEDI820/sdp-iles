from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from .models import Placement
from .serializers import PlacementSerializer
from users.permissions import IsAdminUserRole

class PlacementViewSet(viewsets.ModelViewSet):
    queryset = Placement.objects.all().order_by('-created_at')
    serializer_class = PlacementSerializer
    permission_classes = [IsAuthenticated]