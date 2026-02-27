from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver


# Create your models here.
# class SignModel(models.Model):
#     username = models.CharField(max_length=50)
#     email = models.CharField(max_length=50)
#     password = models.CharField(max_length=50)
#     confirm_password = models.CharField(max_length=50,default="abc")
#     date = models.DateField()
    
class OTPStorage(models.Model):
    email = models.EmailField(unique=True)
    otp_code = models.CharField(max_length=6)
    attempts = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    
class Profile(models.Model):
    ROLE_CHOICES = (
        ('seeker', 'Job Seeker'),
        ('provider', 'Job Provider'),
    )
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    role = models.CharField(max_length=20, choices=ROLE_CHOICES)

    def __str__(self):
        return self.user.username
    
@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)