from django.conf import settings
from django.db import models
from django.utils import timezone
from apps.common.choices import LOG_DRAFT, LOG_STATUS_CHOICES


class WeeklyLog(models.Model):
    student = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='weekly_logs'
    )
    placement = models.ForeignKey(
        'placements.InternshipPlacement',
        on_delete=models.CASCADE,
        related_name='weekly_logs',
    )
    week_number = models.PositiveIntegerField()
    title = models.CharField(max_length=200)
    activities = models.TextField()
    challenges = models.TextField(blank=True)
    lessons_learned = models.TextField(blank=True)
    date_from = models.DateField()
    date_to = models.DateField()
    submission_deadline = models.DateField()
    status = models.CharField(
        max_length=20, choices=LOG_STATUS_CHOICES, default=LOG_DRAFT
    )
    
    # UPDATED & NEW FEEDBACK FIELDS
    review_feedback = models.TextField(blank=True)
    rejection_reason = models.TextField(blank=True)
    revision_request = models.TextField(blank=True)
    
    # NEW: Track who reviewed/approved
    reviewed_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='logs_reviewed'
    )
    approved_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='logs_approved'
    )
    
    # TIMESTAMPS
    submitted_at = models.DateTimeField(null=True, blank=True)
    reviewed_at = models.DateTimeField(null=True, blank=True)
    approved_at = models.DateTimeField(null=True, blank=True)
    rejected_at = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ('student', 'week_number')
        ordering = ['-week_number', '-created_at']

    def mark_submitted(self):
        self.status = 'submitted'
        self.submitted_at = timezone.now()
        self.save(update_fields=['status', 'submitted_at', 'updated_at'])

    def mark_reviewed(self, feedback='', user=None):
        self.status = 'reviewed'
        self.review_feedback = feedback
        self.reviewed_by = user
        self.reviewed_at = timezone.now()
        self.save(update_fields=['status', 'review_feedback', 'reviewed_by', 'reviewed_at', 'updated_at'])

    def mark_approved(self, user=None):
        self.status = 'approved'
        self.approved_by = user
        self.approved_at = timezone.now()
        self.save(update_fields=['status', 'approved_by', 'approved_at', 'updated_at'])

    def mark_rejected(self, reason=''):
        self.status = 'rejected'
        self.rejection_reason = reason
        self.rejected_at = timezone.now()
        self.save(update_fields=['status', 'rejection_reason', 'rejected_at', 'updated_at'])

    def request_revision(self, message=''):
        self.status = 'draft'
        self.revision_request = message
        self.save(update_fields=['status', 'revision_request', 'updated_at'])

    def __str__(self):
        return f'Week {self.week_number} - {self.student.full_name}'