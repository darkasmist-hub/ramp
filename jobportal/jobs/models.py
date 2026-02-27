from django.db import models

# Create your models here.

from django.db import models

class Job(models.Model):
    title = models.CharField(max_length=200)
    company_name = models.CharField(max_length=200)
    location = models.CharField(max_length=100)
    job_type = models.CharField(max_length=50)
    salary = models.IntegerField()
    station = models.CharField(max_length=100)
    description = models.TextField(default="write some thing about job")
    created_at = models.DateTimeField(auto_now_add=True)
    experience = models.CharField(max_length=100)
    education= models.CharField(max_length=200)
    skills = models.CharField(max_length=400)
    shift = models.CharField(max_length=50)

    def __str__(self):
        return self.title
    
# class Requirnment(models.Model):
#     experience = models.CharField(max_length=100)
#     education= models.CharField(max_length=200)
#     skills = models.CharField(max_length=400)
#     shift = models.CharField(max_length=50)
    