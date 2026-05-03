from rest_framework import serializers, viewsets
from rest_framework.permissions import IsAuthenticated

from apps.common.permissions import IsAdmin

from .models import AuditEntry


class AuditEntrySerializer(serializers.ModelSerializer):
    actor_name = serializers.CharField(source="actor.full_name", read_only=True)

    class Meta:
        model = AuditEntry
        fields = ["id", "actor", "actor_name", "action",
                  "target_type", "target_id", "metadata", "created_at"]
        read_only_fields = fields


class AuditEntryViewSet(viewsets.ReadOnlyModelViewSet):
    """Read-only audit log. Admin only — auditors don't write through the API."""
    queryset = AuditEntry.objects.select_related("actor")
    serializer_class = AuditEntrySerializer
    permission_classes = [IsAuthenticated, IsAdmin]
    filterset_fields = ["actor", "action", "target_type"]
    ordering_fields = ["created_at"]
