from django.db import models
from django.core.validators import MinLengthValidator
from django.contrib.auth.models import User

# Create your models here.
class Resume(models.Model):
    TEMPLATE_CHOICES = [
        ('template1', 'Classic'),
        ('template2', 'Modern'),
        ('template3', 'Minimal'),
    ]
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    full_name = models.CharField(max_length=100)
    email = models.EmailField()
    phone = models.CharField(max_length=10,validators=[MinLengthValidator(10)])
    location = models.CharField(max_length=100, null=True, blank=True)
    skills = models.TextField()
    languages = models.TextField(null=True, blank=True)
    hobbys = models.TextField(null=True, blank=True)
    summary = models.TextField()
    experience = models.TextField()
    education = models.TextField()
    image = models.ImageField(upload_to='website/', null=True, blank=True)
    template = models.CharField(max_length=20, choices=TEMPLATE_CHOICES, default='template1')
    @property
    def skills_list(self):
        return [s.strip() for s in self.skills.split(",")]
    @property
    def hobbys_list(self):
        return [h.strip() for h in self.hobbys.split(",")]
    @property
    def experience_lines(self):
        return self.experience.splitlines()
    @property
    def Languages_list(self):
        return [l.strip() for l in self.languages.split(",")]
    def __str__(self):
        return self.full_name
    
    

class Contact(models.Model):
    firstname = models.CharField(max_length=50)
    lastname = models.CharField(max_length=50)
    user = models.ForeignKey(User, on_delete=models.CASCADE,null=True, blank=True)
    Email = models.EmailField()
    Phone = models.CharField(max_length=10,validators=[MinLengthValidator(10)])
    message = models.CharField(max_length=1000)
    date = models.DateTimeField(auto_now_add=True)