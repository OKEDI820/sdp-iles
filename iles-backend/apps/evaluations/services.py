"""Evaluation business logic.

A log can only be evaluated once, only after it's been approved, and
only by the assigned academic supervisor (or admin).
"""
from django.db import transaction
from rest_framework.exceptions import PermissionDenied, ValidationError

from apps.common.choices import LogStatus, Role

from .models import Evaluation
from .scoring import calculate_total


@transaction.atomic
def create_evaluation(*, weekly_log, evaluator, technical_skills,
                     communication, professionalism, remarks="") -> Evaluation:
    if evaluator.role not in (Role.ACADEMIC_SUPERVISOR, Role.ADMIN):
        raise PermissionDenied(
            "Only academic supervisors or admins can create evaluations."
        )
    if weekly_log.status != LogStatus.APPROVED:
        raise ValidationError(
            {"weekly_log": "Logs must be approved before they can be evaluated."}
        )
    if (
        evaluator.role == Role.ACADEMIC_SUPERVISOR
        and weekly_log.placement.academic_supervisor_id != evaluator.id
    ):
        raise PermissionDenied("You are not the assigned academic supervisor.")
    if hasattr(weekly_log, "evaluation"):
        raise ValidationError(
            {"weekly_log": "This log has already been evaluated."}
        )

    total = calculate_total(technical_skills, communication, professionalism)

    return Evaluation.objects.create(
        weekly_log=weekly_log,
        evaluator=evaluator,
        technical_skills=technical_skills,
        communication=communication,
        professionalism=professionalism,
        total_score=total,
        remarks=remarks,
    )
