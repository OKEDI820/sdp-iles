"""Placement model.

Key design choice: workplace_supervisor and academic_supervisor are
ForeignKeys to User, not free-text fields. This lets us:
  - send notifications to real accounts (Lecture 7)
  - authorise specific supervisors (only the assigned supervisor
    can review *this* student's logs — Lecture 2 NFR: security)
  - run dashboards filtered by supervisor.
"""
from django.conf import settings
from django.core.exceptions import ValidationError
from django.db import models

from apps.common.choices import PlacementStatus, Role
from apps.common.models import TimeStampedModel


class InternshipPlacement(TimeStampedModel):
    student = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="placement",
        limit_choices_to={"role": Role.STUDENT},
    )
    workplace_supervisor = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.PROTECT,
        related_name="workplace_placements",
        limit_choices_to={"role": Role.WORKPLACE_SUPERVISOR},
    )
    academic_supervisor = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.PROTECT,
        related_name="academic_placements",
        limit_choices_to={"role": Role.ACADEMIC_SUPERVISOR},
    )

    company_name = models.CharField(max_length=200)
    company_address = models.CharField(max_length=255, blank=True)
    company_contact = models.CharField(max_length=200, blank=True)

    start_date = models.DateField()
    end_date = models.DateField()
    weekly_log_deadline_day = models.PositiveSmallIntegerField(
        default=4,
        help_text=(
            "Day of week the next log is due (0=Mon..6=Sun). "
            "Used to compute submission_deadline server-side."
        ),
    )

    status = models.CharField(
        max_length=20,
        choices=PlacementStatus.choices,
        default=PlacementStatus.PENDING,
    )

    class Meta:
        ordering = ["-start_date"]
        constraints = [
            models.CheckConstraint(
                condition=models.Q(end_date__gte=models.F("start_date")),
                name="placement_end_after_start",
            ),
        ]

    def clean(self):
        super().clean()
        if self.start_date and self.end_date and self.start_date > self.end_date:
            raise ValidationError({"end_date": "End date cannot be before start date."})

    def __str__(self) -> str:
        return f"{self.student.full_name} → {self.company_name}"
