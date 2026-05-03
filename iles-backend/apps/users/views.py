"""User-facing API views.

The pattern: minimal logic in views; permission classes guard access;
serializers handle validation and shape; services (when needed) hold
business rules.
"""
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework_simplejwt.views import TokenObtainPairView

from apps.common.permissions import IsAdmin

from .models import User
from .serializers import (
    PasswordChangeSerializer,
    UserCreateSerializer,
    UserSerializer,
)


class LoginView(TokenObtainPairView):
    """Standard JWT login. Subclassed so we can extend later (e.g. log audit)."""


class CurrentUserView(viewsets.ViewSet):
    """`GET /auth/me/` and `POST /auth/change-password/`."""

    permission_classes = [IsAuthenticated]

    def list(self, request):
        return Response(UserSerializer(request.user).data)

    @action(detail=False, methods=["post"], url_path="change-password")
    def change_password(self, request):
        serializer = PasswordChangeSerializer(
            data=request.data, context={"request": request}
        )
        serializer.is_valid(raise_exception=True)
        user = request.user
        if not user.check_password(serializer.validated_data["old_password"]):
            return Response(
                {"detail": "Current password is incorrect."},
                status=status.HTTP_400_BAD_REQUEST,
            )
        user.set_password(serializer.validated_data["new_password"])
        user.save()
        return Response({"detail": "Password updated."})


class UserViewSet(viewsets.ModelViewSet):
    """Admin-only CRUD over users."""

    queryset = User.objects.all()
    permission_classes = [IsAuthenticated, IsAdmin]
    filterset_fields = ["role", "is_active", "department"]
    search_fields = ["full_name", "email", "student_number", "staff_number"]
    ordering_fields = ["full_name", "email", "role", "date_joined"]

    def get_serializer_class(self):
        if self.action == "create":
            return UserCreateSerializer
        return UserSerializer
