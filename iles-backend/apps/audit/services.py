"""Audit recording service.

Used as `from apps.audit.services import record as record_audit`.
Designed to never raise — failing to record an audit entry should never
break the user flow it was tracking.
"""
from .models import AuditEntry


def record(*, actor=None, action: str, target_type: str = "",
           target_id=None, metadata: dict | None = None) -> AuditEntry | None:
    try:
        return AuditEntry.objects.create(
            actor=actor,
            action=action,
            target_type=target_type,
            target_id=target_id,
            metadata=metadata or {},
        )
    except Exception:
        # Swallow — audit must not break the path it observes.
        return None
