from django.conf import settings
from django.db import models


class InternshipPlacement(models.Model):
    student = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='placement'
    )
    company_name = models.CharField(max_length=255)
    company_address = models.CharField(max_length=255, blank=True)
    
    # NEW: Supervisor ForeignKeys
    workplace_supervisor = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='placements_as_workplace_supervisor'
    )
    academic_supervisor = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='placements_as_academic_supervisor'
    )
    
    # Optional: Keep legacy field for backward compatibility
    supervisor_name = models.CharField(max_length=150, blank=True)
    supervisor_email = models.EmailField(blank=True)
    
    # Dates
    start_date = models.DateField()
    end_date = models.DateField()
    
    # Status
    status = models.CharField(max_length=20, default='active')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f'{self.student.full_name} - {self.company_name}'