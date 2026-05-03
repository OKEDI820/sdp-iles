"""Workflow rules for weekly logs (CSC 1202 Lecture 2).

Centralising these in one module is deliberate: the lecture warns
"Rules must be enforced centrally". Anywhere status changes — admin,
API, management command — must funnel through `assert_transition`.
"""
from datetime import date as date_type

from django.utils import timezone
from rest_framework.exceptions import ValidationError

from apps.common.choices import LogStatus


# Adjacency map of legal transitions. Approved is terminal; rejected can
# go back to draft so the student can fix and retry.
VALID_TRANSITIONS: dict[str, set[str]] = {
    LogStatus.DRAFT: {LogStatus.SUBMITTED},
    LogStatus.SUBMITTED: {LogStatus.REVIEWED, LogStatus.REJECTED},
    LogStatus.REVIEWED: {LogStatus.APPROVED, LogStatus.DRAFT, LogStatus.REJECTED},
    LogStatus.REJECTED: {LogStatus.DRAFT},
    LogStatus.APPROVED: set(),
}


def assert_transition(current: str, new: str) -> None:
    if new not in VALID_TRANSITIONS.get(current, set()):
        raise ValidationError(
            {"detail": f"Cannot transition from '{current}' to '{new}'."}
        )


def assert_deadline_not_passed(deadline: date_type) -> None:
    if timezone.localdate() > deadline:
        raise ValidationError(
            {"detail": "Submission deadline has passed for this log."}
        )


def assert_editable(log) -> None:
    """Approved logs are immutable (Lecture 1 deadline-enforcement spec)."""
    if log.status == LogStatus.APPROVED:
        raise ValidationError({"detail": "Approved logs cannot be edited."})
