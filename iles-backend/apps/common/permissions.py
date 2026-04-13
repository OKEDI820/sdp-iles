from rest_framework.permissions import BasePermission
from apps.common.choices import ROLE_COORDINATOR, ROLE_STUDENT, ROLE_SUPERVISOR

class IsCoordinator(BasePermission):
    def has_permission(self, request, view):
        return bool(request.user and request.user.is_authenticated and request.user.role == ROLE_COORDINATOR)

class IsSupervisor(BasePermission):
    def has_permission(self, request,view):
        return bool(request.user and request.user.is_authenticated and request.user.role == ROLE_SUPERVISOR)

class IsStudent(BasePermission):
    def has_permission(self, request, view):
        return bool(request.user and request.user.is_authenticated and request.user.role == ROLE_STUDENT)
