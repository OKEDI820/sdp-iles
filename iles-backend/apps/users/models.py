from django.contrib.auth.models import AbstractUser
from django.db import models
from apps.common.choices import ROLE_CHOICES, ROLE_STUDENT

class User(AbstractUser):
    email = models.EmailField(unique=True)
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default=ROLE_STUDENT)
    full_name = models.CharField(max_length=150, blank=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    def save(self, *args, **kwargs):
        if not self.full_name:
            self.full_name = f'{self.first_name} {self.last_name}'.strip() or self.username
        super().save(*args, **kwargs)

    def __str__(self):
        return f'{self.full_name} ({self.role})'
