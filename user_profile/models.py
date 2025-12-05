from django.conf import settings
from django.db import models

# Create your models here.


class UserProfile(models.Model):
    user = models.OneToOneField(to=settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    job = models.CharField(blank=True, null=True, max_length=255)
    avatar = models.CharField(blank=True, null=True, max_length=255)
    location = models.CharField(blank=True, null=True, max_length=255)
    phone_number = models.CharField(blank=True, null=True, max_length=50)
    about_me = models.CharField(blank=True, null=True, max_length=1024)
    user_hashtags = models.JSONField(default=list, blank=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user.email}'s profile"
