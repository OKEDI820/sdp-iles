from rest_framework import generics, permissions, viewsets
from rest_framework.response import Response
from .models import User
from .serializers import UserCreateSerializer, UserSerializer
from apps.common.choices import ROLE_COORDINATOR


class CurrentUserView(generics.RetrieveAPIView):
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        return self.request.user


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all().order_by('id')
    permission_classes = [permissions.IsAuthenticated]
    search_fields = ['full_name', 'email', 'role']
    ordering_fields = ['id', 'full_name', 'email', 'role']

    def get_serializer_class(self):
        if self.action == 'create':
            return UserCreateSerializer
        return UserSerializer

    def get_queryset(self):
        user = self.request.user
        if user.role == ROLE_COORDINATOR:
            return User.objects.all().order_by('id')
        return User.objects.filter(id=user.id)

    def create(self, request, *args, **kwargs):
        if request.user.role != ROLE_COORDINATOR:
            return Response({'detail': 'Only coordinators can create users.'}, status=403)
        return super().create(request, *args, **kwargs)
