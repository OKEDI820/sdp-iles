"""Custom user model with the four roles from CSC 1202 Lecture 2.

We use email as the login identifier (more conventional than username)
and provide convenience role-check properties.
"""
from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.db import models

from apps.common.choices import Role


class UserManager(BaseUserManager):
    """Email-based user manager."""

    use_in_migrations = True

    def _create_user(self, email, password, **extra_fields):
        if not email:
            raise ValueError("Email is required")
        email = self.normalize_email(email)
        # username is still required by AbstractUser; use email's local part.
        if "username" not in extra_fields or not extra_fields["username"]:
            extra_fields["username"] = email.split("@")[0]
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", False)
        extra_fields.setdefault("is_superuser", False)
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("role", Role.ADMIN)
        return self._create_user(email, password, **extra_fields)


class User(AbstractUser):
    email = models.EmailField(unique=True)
    role = models.CharField(max_length=30, choices=Role.choices, default=Role.STUDENT)
    full_name = models.CharField(max_length=150, blank=True)
    student_number = models.CharField(max_length=20, blank=True, db_index=True)
    staff_number = models.CharField(max_length=20, blank=True, db_index=True)
    department = models.CharField(max_length=100, blank=True)
    phone = models.CharField(max_length=20, blank=True)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["username"]

    objects = UserManager()

    class Meta:
        ordering = ["full_name", "email"]

    def save(self, *args, **kwargs):
        if not self.full_name:
            derived = f"{self.first_name} {self.last_name}".strip()
            self.full_name = derived or self.username
        super().save(*args, **kwargs)

    # Convenience role checks — used in serializers and views.
    @property
    def is_student(self) -> bool:
        return self.role == Role.STUDENT

    @property
    def is_workplace_supervisor(self) -> bool:
        return self.role == Role.WORKPLACE_SUPERVISOR

    @property
    def is_academic_supervisor(self) -> bool:
        return self.role == Role.ACADEMIC_SUPERVISOR

    @property
    def is_admin_role(self) -> bool:
        return self.role == Role.ADMIN

    @property
    def is_supervisor(self) -> bool:
        return self.role in (
            Role.WORKPLACE_SUPERVISOR,
            Role.ACADEMIC_SUPERVISOR,
            Role.ADMIN,
        )

    def __str__(self) -> str:
        return f"{self.full_name} ({self.get_role_display()})"
