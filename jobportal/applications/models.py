from django.db import models

# Create your models here.
from django.db import models
from django.contrib.auth.models import User
from jobs.models import Job


# class Application(models.Model):
#     STATUS_CHOICES = (
#         ("Pending", "Pending"),
#         ("Reviewed", "Reviewed"),
#         ("Accepted", "Accepted"),
#         ("Rejected", "Rejected"),
#     )

#     user = models.ForeignKey(User, on_delete=models.CASCADE)
#     job = models.ForeignKey(Job, on_delete=models.CASCADE)
#     cover_letter = models.TextField(blank=True, null=True)
#     resume = models.FileField(upload_to="resumes/", blank=True, null=True)
#     status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="Pending")
#     applied_at = models.DateTimeField(auto_now_add=True)

#     def __str__(self):
#         return f"{self.user.username} applied to {self.job.title}"

class AssessmentTemplate(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    duration = models.IntegerField(help_text="Duration in minutes")
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

class Question(models.Model):
    assessment = models.ForeignKey(AssessmentTemplate, on_delete=models.CASCADE)
    text = models.TextField()
    correct_option = models.IntegerField()


class Option(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    text = models.CharField(max_length=255)