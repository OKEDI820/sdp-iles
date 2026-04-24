from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django.contrib.auth import get_user_model
from placements.models import Placement

User = get_user_model()

@api_view(["GET"])
@permission_classes([IsAuthenticated])
def dashboard_summary(request):
    return Response({
        "total_users": User.objects.count(),
        "total_placements": Placement.objects.count(),
        "pending_placements": Placement.objects.filter(status="pending").count(),
    })
