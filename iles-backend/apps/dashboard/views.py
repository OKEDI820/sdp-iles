"""Dashboard endpoint.

Returns a summary tailored to the requesting user's role. Each role gets
a different shape, so the frontend can render a role-specific dashboard.
"""
from django.db.models import Avg, Count, Q
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.common.choices import LogStatus, Role
from apps.evaluations.models import Evaluation
from apps.logs.models import WeeklyLog
from apps.placements.models import InternshipPlacement
from apps.users.models import User


def _status_counts(qs):
    """Returns a {status: count} dict over a queryset of WeeklyLogs."""
    rows = qs.values("status").annotate(n=Count("id"))
    counts = {s.value: 0 for s in LogStatus}
    for row in rows:
        counts[row["status"]] = row["n"]
    return counts


class DashboardView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        if user.role == Role.STUDENT:
            return Response(self._student(user))
        if user.role == Role.WORKPLACE_SUPERVISOR:
            return Response(self._workplace(user))
        if user.role == Role.ACADEMIC_SUPERVISOR:
            return Response(self._academic(user))
        return Response(self._admin())

    # ---- per-role builders ----

    def _student(self, user):
        logs = WeeklyLog.objects.filter(student=user)
        evals = Evaluation.objects.filter(weekly_log__student=user)
        return {
            "role": "student",
            "log_counts": _status_counts(logs),
            "total_logs": logs.count(),
            "average_score": float(
                evals.aggregate(avg=Avg("total_score")).get("avg") or 0
            ),
            "recent_logs": list(
                logs.order_by("-week_number")
                .values("id", "week_number", "title", "status", "submission_deadline")[:5]
            ),
            "has_placement": InternshipPlacement.objects.filter(student=user).exists(),
        }

    def _workplace(self, user):
        logs = WeeklyLog.objects.filter(placement__workplace_supervisor=user)
        return {
            "role": "workplace_supervisor",
            "students_supervised": InternshipPlacement.objects.filter(
                workplace_supervisor=user
            ).count(),
            "log_counts": _status_counts(logs),
            "awaiting_review": logs.filter(status=LogStatus.SUBMITTED).count(),
            "recent_submissions": list(
                logs.filter(status=LogStatus.SUBMITTED)
                .order_by("-submitted_at")
                .values("id", "week_number", "title",
                        "student__full_name", "submitted_at")[:10]
            ),
        }

    def _academic(self, user):
        logs = WeeklyLog.objects.filter(placement__academic_supervisor=user)
        evals = Evaluation.objects.filter(evaluator=user)
        return {
            "role": "academic_supervisor",
            "students_supervised": InternshipPlacement.objects.filter(
                academic_supervisor=user
            ).count(),
            "log_counts": _status_counts(logs),
            "awaiting_approval": logs.filter(status=LogStatus.REVIEWED).count(),
            "evaluations_given": evals.count(),
            "average_score_given": float(
                evals.aggregate(avg=Avg("total_score")).get("avg") or 0
            ),
            "to_approve": list(
                logs.filter(status=LogStatus.REVIEWED)
                .order_by("-reviewed_at")
                .values("id", "week_number", "title",
                        "student__full_name", "reviewed_at")[:10]
            ),
        }

    def _admin(self):
        logs = WeeklyLog.objects.all()
        return {
            "role": "admin",
            "user_counts": {
                row["role"]: row["n"]
                for row in User.objects.values("role").annotate(n=Count("id"))
            },
            "active_placements": InternshipPlacement.objects.filter(
                status="active"
            ).count(),
            "total_placements": InternshipPlacement.objects.count(),
            "log_counts": _status_counts(logs),
            "average_score": float(
                Evaluation.objects.aggregate(avg=Avg("total_score")).get("avg") or 0
            ),
            "overdue_submissions": logs.filter(
                Q(status=LogStatus.DRAFT) | Q(status=LogStatus.REJECTED),
                submission_deadline__lt=__import__("datetime").date.today(),
            ).count(),
        }
