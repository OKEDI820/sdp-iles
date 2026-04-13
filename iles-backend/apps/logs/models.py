from django.conf import settings
from django.db import models
from django.utils import timezone
from apps.common.choices import LOG_DRAFT, LOG_STATUS_CHOICES

class WeeklyLog(models.Model):
    student = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='weekly_logs')
    placement = models.ForeignKey('placements.InternshipPlacement', on_delete=models.CASCADE, related_name='weekly_logs')
    week_number = models.PositiveIntegerField()
    title = models.CharField(max_length=200)
    activities = models.TextField()
    challenges = models.TextField(blank=True)
    lessons_learned = models.TextField(blank=True)
    date_from = models.DateField()
    date_to = models.DateField()
    submission_deadline = models.DateField()
    status = models.CharField(max_length=20, choices=LOG_STATUS_CHOICES, default=LOG_DRAFT)
    feedback = models.TextField(blank=True)
    submitted_at = models.DateTimeField(null=True, blank=True)
    reviewed_at = models.DateTimeField(null=True, blank=True)
    approved_at = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ('student', 'week_number')
        ordering = ['-week_number', '-created_at']

    def mark_submitted(self):
        self.status = 'submitted'
        self.submitted_at = timezone.now()
        self.save(update_fields=['status', 'submitted_at', 'updated_at'])

    def mark_reviewed(self, feedback=''):
        self.status = 'reviewed'
        self.feedback = feedback
        self.reviewed_at = timezone.now()
        self.save(update_fields=['status', 'feedback', 'reviewed_at', 'updated_at'])

    def mark_approved(self):
        self.status = 'approved'
        self.approved_at = timezone.now()
        self.save(update_fields=['status', 'approved_at', 'updated_at'])

    def request_revision(self, feedback=''):
        self.status = 'draft'
        self.feedback = feedback
        self.save(update_fields=['status', 'feedback', 'updated_at'])

    def __str__(self):
        return f'Week {self.week_number} - {self.student.full_name}'
