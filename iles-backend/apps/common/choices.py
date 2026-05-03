"""Single source of truth for enumerated values used across the project.

Roles come from CSC 1202 Lecture 2 (four roles).
Workflow states come from Lecture 2 (five states for weekly logs).
"""
from django.db import models


class Role(models.TextChoices):
    STUDENT = "student", "Student Intern"
    WORKPLACE_SUPERVISOR = "workplace_supervisor", "Workplace Supervisor"
    ACADEMIC_SUPERVISOR = "academic_supervisor", "Academic Supervisor"
    ADMIN = "admin", "Internship Administrator"


# Convenience tuple — anyone allowed to act on a submitted log.
SUPERVISOR_ROLES = (
    Role.WORKPLACE_SUPERVISOR,
    Role.ACADEMIC_SUPERVISOR,
    Role.ADMIN,
)


class LogStatus(models.TextChoices):
    DRAFT = "draft", "Draft"
    SUBMITTED = "submitted", "Submitted"
    REVIEWED = "reviewed", "Reviewed"
    APPROVED = "approved", "Approved"
    REJECTED = "rejected", "Rejected"


class PlacementStatus(models.TextChoices):
    PENDING = "pending", "Pending"
    ACTIVE = "active", "Active"
    COMPLETED = "completed", "Completed"
    TERMINATED = "terminated", "Terminated"
