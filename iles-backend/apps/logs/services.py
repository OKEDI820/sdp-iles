"""Service layer for weekly log workflow.

Each function:
  - takes the log + the acting user
  - validates the transition
  - mutates the log atomically
  - returns the updated log

Business logic lives here, NOT in views or serializers. Views are thin
HTTP adapters; services are testable, reusable, transactional.
"""
from __future__ import annotations

from datetime import date, timedelta

from django.db import transaction
from django.utils import timezone
from rest_framework.exceptions import PermissionDenied

from apps.common.choices import LogStatus, Role

from .models import WeeklyLog
from .validators import (
    assert_deadline_not_passed,
    assert_editable,
    assert_transition,
)


# ---------- creation ----------

def compute_deadline(week_end: date, deadline_day: int) -> date:
    """Returns the next occurrence of `deadline_day` (0=Mon) after week_end."""
    days_ahead = (deadline_day - week_end.weekday()) % 7
    if days_ahead == 0:
        days_ahead = 7
    return week_end + timedelta(days=days_ahead)


@transaction.atomic
def create_draft_log(*, student, placement, week_number, week_start, week_end,
                    title, activities, challenges="", lessons_learned="") -> WeeklyLog:
    deadline = compute_deadline(week_end, placement.weekly_log_deadline_day)
    return WeeklyLog.objects.create(
        student=student,
        placement=placement,
        week_number=week_number,
        title=title,
        activities=activities,
        challenges=challenges,
        lessons_learned=lessons_learned,
        week_start=week_start,
        week_end=week_end,
        submission_deadline=deadline,
        status=LogStatus.DRAFT,
    )


# ---------- transitions ----------

@transaction.atomic
def submit_log(log: WeeklyLog, *, actor) -> WeeklyLog:
    if actor.role != Role.STUDENT or log.student_id != actor.id:
        raise PermissionDenied("Only the owning student can submit a log.")
    assert_transition(log.status, LogStatus.SUBMITTED)
    assert_deadline_not_passed(log.submission_deadline)

    log.status = LogStatus.SUBMITTED
    log.submitted_at = timezone.now()
    log.save(update_fields=["status", "submitted_at", "updated_at"])
    return log


@transaction.atomic
def review_log(log: WeeklyLog, *, actor, feedback: str = "") -> WeeklyLog:
    _ensure_assigned_supervisor(log, actor, action="review")
    assert_transition(log.status, LogStatus.REVIEWED)

    log.status = LogStatus.REVIEWED
    log.review_feedback = feedback
    log.reviewed_at = timezone.now()
    log.reviewed_by = actor
    log.save(update_fields=[
        "status", "review_feedback", "reviewed_at", "reviewed_by", "updated_at",
    ])
    return log


@transaction.atomic
def approve_log(log: WeeklyLog, *, actor) -> WeeklyLog:
    if actor.role not in (Role.ACADEMIC_SUPERVISOR, Role.ADMIN):
        raise PermissionDenied("Only academic supervisors or admins can approve.")
    if actor.role == Role.ACADEMIC_SUPERVISOR and log.placement.academic_supervisor_id != actor.id:
        raise PermissionDenied("You are not the assigned academic supervisor.")
    assert_transition(log.status, LogStatus.APPROVED)

    log.status = LogStatus.APPROVED
    log.approved_at = timezone.now()
    log.approved_by = actor
    log.save(update_fields=[
        "status", "approved_at", "approved_by", "updated_at",
    ])
    return log


@transaction.atomic
def reject_log(log: WeeklyLog, *, actor, reason: str) -> WeeklyLog:
    if not reason:
        raise PermissionDenied("Rejection reason is required.")
    _ensure_assigned_supervisor(log, actor, action="reject")
    assert_transition(log.status, LogStatus.REJECTED)

    log.status = LogStatus.REJECTED
    log.rejection_reason = reason
    log.rejected_at = timezone.now()
    log.save(update_fields=[
        "status", "rejection_reason", "rejected_at", "updated_at",
    ])
    return log


@transaction.atomic
def request_revision(log: WeeklyLog, *, actor, message: str) -> WeeklyLog:
    """Sends a reviewed log back to draft for the student to revise."""
    _ensure_assigned_supervisor(log, actor, action="request revision on")
    assert_transition(log.status, LogStatus.DRAFT)

    log.status = LogStatus.DRAFT
    log.revision_request = message
    log.save(update_fields=["status", "revision_request", "updated_at"])
    return log


@transaction.atomic
def update_draft(log: WeeklyLog, *, actor, **fields) -> WeeklyLog:
    """Edit an existing draft. Approved logs are immutable."""
    assert_editable(log)
    if actor.role == Role.STUDENT and log.student_id != actor.id:
        raise PermissionDenied("Students may only edit their own logs.")
    if log.status not in (LogStatus.DRAFT, LogStatus.REJECTED):
        raise PermissionDenied(
            f"Cannot edit a log in status '{log.status}'. Only drafts/rejected are editable."
        )

    allowed = {"title", "activities", "challenges", "lessons_learned"}
    for key, value in fields.items():
        if key in allowed:
            setattr(log, key, value)
    log.save()
    return log


# ---------- helpers ----------

def _ensure_assigned_supervisor(log: WeeklyLog, actor, *, action: str) -> None:
    """Only assigned supervisors (and admins) may act on a log.

    This implements the Lecture 2 NFR: "Only assigned supervisors can review
    a student's logs."
    """
    if actor.role == Role.ADMIN:
        return
    if actor.role == Role.WORKPLACE_SUPERVISOR and log.placement.workplace_supervisor_id == actor.id:
        return
    if actor.role == Role.ACADEMIC_SUPERVISOR and log.placement.academic_supervisor_id == actor.id:
        return
    raise PermissionDenied(f"You are not authorised to {action} this log.")
