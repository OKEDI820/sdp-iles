from django.db import models


class Placement(models.Model):
    STATUS_CHOICES = (
        ('pending', 'Pending'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
    )

    student_name = models.CharField(max_length=150)
    student_email = models.EmailField()
    organization_name = models.CharField(max_length=200)
    supervisor_name = models.CharField(max_length=150)
    supervisor_email = models.EmailField()
    location = models.CharField(max_length=200)
    start_date = models.DateField()
    end_date = models.DateField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.student_name} - {self.organization_name}"