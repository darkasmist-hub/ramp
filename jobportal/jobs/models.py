from django.db import models

# Create your models here.
from django.conf import settings
from django.db import models
from django.utils import timezone
from datetime import timedelta

class Job(models.Model):
    employer = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="jobs", 
        null=True,        # 👈 IMPORTANT
        blank=True  
    )
    title = models.CharField(max_length=200)
    company_name = models.CharField(max_length=200)
    location = models.CharField(max_length=100)
    job_type = models.CharField(max_length=50)
    companyEmail = models.EmailField(null=True,blank=True)
    salary = models.IntegerField()
    station = models.CharField(max_length=100)
    description = models.TextField(null=True,blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    experience = models.CharField(max_length=100)
    education= models.CharField(max_length=200)
    skills = models.CharField(max_length=400)
    shift = models.CharField(max_length=50)
    expires_at = models.DateField(null=True, blank=True)
    
    def is_expired(self):
        return self.expires_at and self.expires_at < timezone.now()

    def save(self, *args, **kwargs):
        if not self.expires_at:
            self.expires_at = timezone.now() + timedelta(days=30)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title
    
class JobApplication(models.Model):
    job = models.ForeignKey(Job, on_delete=models.CASCADE, related_name="applications")
    applicant = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    resume = models.FileField(upload_to="resumes/")
    cover_letter = models.TextField(blank=True, null=True)
    applied_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.applicant.username} - {self.job.title}"
# class Requirnment(models.Model):
#     experience = models.CharField(max_length=100)
#     education= models.CharField(max_length=200)
#     skills = models.CharField(max_length=400)
#     shift = models.CharField(max_length=50)
    