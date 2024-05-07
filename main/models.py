from django.conf import settings

from django.contrib.auth.models import AbstractUser
from django.db import models
from phonenumber_field.modelfields import PhoneNumberField


class Job(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    employer = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='jobs')
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title


class CustomUser(AbstractUser):
    is_employer = models.BooleanField(default=False)
    company_name = models.CharField(max_length=100, blank=True, null=True)
    skills = models.TextField(blank=True, null=True)
    desired_salary = models.FloatField(default=0.0, blank=True, null=True)
    experience = models.TextField(default="No experience provided.", blank=True, null=True)
    phone_number = PhoneNumberField(blank=True, null=True)

    def get_active_jobs(self):
        if self.is_employer:
            return self.jobs.filter(is_active=True)
        return []

    def get_inactive_jobs(self):
        if self.is_employer:
            return self.jobs.filter(is_active=False)
        return []


class Review(models.Model):
    from_user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='given_reviews')
    to_user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='received_reviews')
    job = models.ForeignKey(Job, on_delete=models.CASCADE, related_name='reviews')
    rating = models.IntegerField()
    comment = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.rating}/5 - {self.comment}'
