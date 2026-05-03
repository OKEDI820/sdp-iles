"""Weekly log — the core unit of work in ILES.

Lecture 1 framing: Software = Data + Rules + States + Behavior.
This model is the data; validators.py is the rules and states;
services.py is the behavior.
"""
from django.conf import settings
from django.db import models

from apps.common.choices import LogStatus, Role
from apps.common.models import TimeStampedModel


class WeeklyLog(TimeStampedModel):
    student = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="weekly_logs",
        limit_choices_to={"role": Role.STUDENT},
    )
    placement = models.ForeignKey(
        "placements.InternshipPlacement",
        on_delete=models.CASCADE,
        related_name="weekly_logs",
    )
    week_number = models.PositiveIntegerField()

    title = models.CharField(max_length=200)
    activities = models.TextField()
    challenges = models.TextField(blank=True)
    lessons_learned = models.TextField(blank=True)

    week_start = models.DateField()
    week_end = models.DateField()
    submission_deadline = models.DateField(
        help_text="Computed from placement.weekly_log_deadline_day; not user-set."
    )

    status = models.CharField(
        max_length=20,
        choices=LogStatus.choices,
        default=LogStatus.DRAFT,
        db_index=True,
    )

    # Reviewer feedback. Distinct from "rejection reason" so each transition
    # captures its own context.
    review_feedback = models.TextField(blank=True)
    rejection_reason = models.TextField(blank=True)
    revision_request = models.TextField(blank=True)

    submitted_at = models.DateTimeField(null=True, blank=True)
    reviewed_at = models.DateTimeField(null=True, blank=True)
    approved_at = models.DateTimeField(null=True, blank=True)
    rejected_at = models.DateTimeField(null=True, blank=True)

    reviewed_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True, blank=True,
        related_name="logs_reviewed",
    )
    approved_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True, blank=True,
        related_name="logs_approved",
    )

    class Meta:
        ordering = ["-week_number", "-created_at"]
        constraints = [
            models.UniqueConstraint(
                fields=["student", "week_number"],
                name="unique_student_week",
            ),
            models.CheckConstraint(
                condition=models.Q(week_end__gte=models.F("week_start")),
                name="weeklylog_end_after_start",
            ),
        ]
        indexes = [
            models.Index(fields=["status", "submission_deadline"]),
        ]

    def __str__(self) -> str:
        return f"Week {self.week_number} – {self.student.full_name} – {self.get_status_display()}"
