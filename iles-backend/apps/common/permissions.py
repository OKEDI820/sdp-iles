"""Reusable DRF permission classes.

Putting role logic in permission classes (instead of `if user.role == ...`
in every view) gives us declarative RBAC — a view simply lists what it
requires.
"""
from rest_framework.permissions import BasePermission, SAFE_METHODS

from apps.common.choices import Role, SUPERVISOR_ROLES


class IsAdmin(BasePermission):
    """Internship Administrator only."""

    def has_permission(self, request, view):
        return bool(request.user and request.user.is_authenticated and request.user.role == Role.ADMIN)


class IsStudent(BasePermission):
    def has_permission(self, request, view):
        return bool(request.user and request.user.is_authenticated and request.user.role == Role.STUDENT)


class IsSupervisor(BasePermission):
    """Either workplace supervisor, academic supervisor, or admin."""

    def has_permission(self, request, view):
        return bool(
            request.user
            and request.user.is_authenticated
            and request.user.role in SUPERVISOR_ROLES
        )


class IsAcademicSupervisorOrAdmin(BasePermission):
    """Final approval is restricted to academics and admin."""

    def has_permission(self, request, view):
        return bool(
            request.user
            and request.user.is_authenticated
            and request.user.role in (Role.ACADEMIC_SUPERVISOR, Role.ADMIN)
        )


class IsOwnerOrSupervisor(BasePermission):
    """Object-level: owners (the student) and any supervisor can read.

    Mutations are still restricted by the role checks on the view's actions.
    """

    def has_object_permission(self, request, view, obj):
        if not (request.user and request.user.is_authenticated):
            return False
        if request.user.role in SUPERVISOR_ROLES:
            return True
        # Owners can read their own records.
        owner_id = getattr(obj, "student_id", None)
        return owner_id == request.user.id and request.method in SAFE_METHODS


class ReadOnly(BasePermission):
    def has_permission(self, request, view):
        return request.method in SAFE_METHODS
