from django.conf import settings
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models

from apps.common.models import TimeStampedModel


class EvaluationCriterion(TimeStampedModel):
    """Configurable description of a criterion (for display).

    The actual weight used in computation lives in `scoring.py` so we
    can guarantee invariants (sum to 1.00). The model simply mirrors
    those values for the UI.
    """
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True)
    weight_percent = models.PositiveSmallIntegerField()
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ["-weight_percent", "name"]

    def __str__(self) -> str:
        return f"{self.name} ({self.weight_percent}%)"


class Evaluation(TimeStampedModel):
    weekly_log = models.OneToOneField(
        "logs.WeeklyLog",
        on_delete=models.CASCADE,
        related_name="evaluation",
    )
    evaluator = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.PROTECT,
        related_name="evaluations_given",
    )

    technical_skills = models.PositiveSmallIntegerField(
        validators=[MinValueValidator(0), MaxValueValidator(100)]
    )
    communication = models.PositiveSmallIntegerField(
        validators=[MinValueValidator(0), MaxValueValidator(100)]
    )
    professionalism = models.PositiveSmallIntegerField(
        validators=[MinValueValidator(0), MaxValueValidator(100)]
    )

    total_score = models.DecimalField(max_digits=5, decimal_places=2)
    remarks = models.TextField(blank=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self) -> str:
        return f"Eval[{self.weekly_log_id}] = {self.total_score}"
