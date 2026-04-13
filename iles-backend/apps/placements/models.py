from django.conf import settings
from django.db import models

class InternshipPlacement(models.Model):
    student = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='placement')
    company_name = models.CharField(max_length=255)
    company_address = models.CharField(max_length=255, blank=True)
    supervisor_name = models.CharField(max_length=150)
    supervisor_email = models.EmailField(blank=True)
    start_date = models.DateField()
    end_date = models.DateField()
    status = models.CharField(max_length=20, default='active')
    created_at = models.DateTimeField(auto_now_add=False)


    def __str__(self):
        return f'{self.student.full_name} - {self.company_name}'
