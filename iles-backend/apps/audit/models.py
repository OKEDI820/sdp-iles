"""Audit trail.

Lecture 4 listed "Audit Logs" as a system resource and Lecture 2's NFR
slide called out "All review actions must be logged." A dedicated model
gives us a queryable history that survives row deletes (we don't FK to
the target — we store its type+id as text).
"""
from django.conf import settings
from django.db import models


class AuditEntry(models.Model):
    actor = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True, blank=True,
        related_name="audit_entries",
    )
    action = models.CharField(max_length=80, db_index=True)
    target_type = models.CharField(max_length=80, blank=True)
    target_id = models.PositiveBigIntegerField(null=True, blank=True)
    metadata = models.JSONField(default=dict, blank=True)
    created_at = models.DateTimeField(auto_now_add=True, db_index=True)

    class Meta:
        ordering = ["-created_at"]
        indexes = [
            models.Index(fields=["target_type", "target_id"]),
        ]

    def __str__(self) -> str:
        actor_name = self.actor.full_name if self.actor else "system"
        return f"[{self.created_at:%Y-%m-%d %H:%M}] {actor_name}: {self.action}"
