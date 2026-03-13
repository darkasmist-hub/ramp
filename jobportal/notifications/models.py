from django.db import models
from django.contrib.auth.models import User
from jobs.models import JobApplication

# Create your models here.
from django.conf import settings


class Notification(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="notifications"
    )
    message = models.TextField()
    link = models.URLField(blank=True, null=True)
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Notification for {self.user.username}"
    
    
class Interview(models.Model):

    MODE_CHOICES = (
        ("online", "Online"),
        ("offline", "Offline"),
    )

    application = models.ForeignKey(
        JobApplication,
        on_delete=models.CASCADE
    )

    date = models.DateField()
    time = models.TimeField()
    mode = models.CharField(max_length=10, choices=MODE_CHOICES)

    meeting_link = models.CharField(max_length=255, blank=True, null=True)
    notes = models.TextField(blank=True, null=True)

    created_at = models.DateTimeField(auto_now_add=True)