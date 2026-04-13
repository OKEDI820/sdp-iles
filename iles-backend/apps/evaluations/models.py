from django.conf import settings
from django.db import models

class EvaluationCriteria(models.Model):
    name = models.CharField(max_length=100)
    weight = models.DecimalField(max_digits=5, decimal_places=2)
    max_score = models.PositiveIntegerField(default=100)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.name

class Evaluation(models.Model):
    weekly_log = models.OneToOneField('logs.WeeklyLog', on_delete=models.CASCADE, related_name='evaluation')
    evaluator = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='evaluations')
    technical_skills = models.PositiveIntegerField(default=0)
    communication = models.PositiveIntegerField(default=0)
    professionalism = models.PositiveIntegerField(default=0)
    total_score = models.DecimalField(max_digits=5, decimal_places=2, default=0)
    remarks = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Evaluation for {self.weekly_log}'
