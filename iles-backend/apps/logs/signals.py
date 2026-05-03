"""Signal-driven side effects for weekly logs.

Lecture 7 explicitly demonstrates `post_save` signals as the integration
point between workflow updates and notifications. We use the same pattern
here, plus we record an audit entry on every status transition.

Note: we don't compute "what changed" inside the signal — we keep a
shadow of the old status on the instance via pre_save, so we can detect
transitions reliably.
"""
from django.conf import settings
from django.core.mail import send_mail
from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver

from apps.audit.services import record as record_audit
from apps.common.choices import LogStatus

from .models import WeeklyLog


# --- Capture previous status so post_save can detect transitions. ---

@receiver(pre_save, sender=WeeklyLog)
def remember_old_status(sender, instance: WeeklyLog, **kwargs):
    if instance.pk:
        try:
            previous = WeeklyLog.objects.get(pk=instance.pk)
            instance._previous_status = previous.status
        except WeeklyLog.DoesNotExist:
            instance._previous_status = None
    else:
        instance._previous_status = None


# --- After save: notify and audit. ---

@receiver(post_save, sender=WeeklyLog)
def notify_and_audit(sender, instance: WeeklyLog, created: bool, **kwargs):
    previous = getattr(instance, "_previous_status", None)
    student = instance.student
    placement = instance.placement
    week = instance.week_number
    from_email = getattr(settings, "DEFAULT_FROM_EMAIL", "iles@example.com")

    if created:
        record_audit(
            actor=student, action="log.created",
            target_type="WeeklyLog", target_id=instance.pk,
            metadata={"week_number": week, "status": instance.status},
        )
        return

    if previous == instance.status:
        return  # not a status change; ignore field edits

    record_audit(
        actor=instance.reviewed_by or instance.approved_by or student,
        action=f"log.status.{instance.status}",
        target_type="WeeklyLog", target_id=instance.pk,
        metadata={"from": previous, "to": instance.status, "week_number": week},
    )

    new = instance.status

    if new == LogStatus.SUBMITTED:
        send_mail(
            subject=f"Log submitted – {student.full_name}, week {week}",
            message=(
                f"{student.full_name} submitted their week {week} log "
                f"'{instance.title}' for review."
            ),
            from_email=from_email,
            recipient_list=[placement.workplace_supervisor.email],
            fail_silently=True,
        )

    elif new == LogStatus.REVIEWED:
        send_mail(
            subject=f"Your week {week} log was reviewed",
            message=(
                f"Hello {student.full_name},\n\n"
                f"Your week {week} log was reviewed.\n\n"
                f"Feedback: {instance.review_feedback or '(none)'}\n\n"
                "It will now be considered for academic approval."
            ),
            from_email=from_email,
            recipient_list=[student.email, placement.academic_supervisor.email],
            fail_silently=True,
        )

    elif new == LogStatus.APPROVED:
        send_mail(
            subject=f"Week {week} log approved",
            message=(
                f"Hello {student.full_name},\n\n"
                f"Your week {week} log has been approved. Well done."
            ),
            from_email=from_email,
            recipient_list=[student.email],
            fail_silently=True,
        )

    elif new == LogStatus.REJECTED:
        send_mail(
            subject=f"Week {week} log rejected",
            message=(
                f"Hello {student.full_name},\n\n"
                f"Your week {week} log was rejected.\n\n"
                f"Reason: {instance.rejection_reason or '(none provided)'}"
            ),
            from_email=from_email,
            recipient_list=[student.email],
            fail_silently=True,
        )

    elif new == LogStatus.DRAFT and previous == LogStatus.REVIEWED:
        # Revision requested
        send_mail(
            subject=f"Revision requested – week {week}",
            message=(
                f"Hello {student.full_name},\n\n"
                f"A revision was requested for your week {week} log.\n\n"
                f"Message: {instance.revision_request or '(none provided)'}"
            ),
            from_email=from_email,
            recipient_list=[student.email],
            fail_silently=True,
        )
