from django.conf import settings
from django.db import models

# Create your models here.


class UserProfile(models.Model):
    user = models.OneToOneField(
        to=settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="profile"
    )
    job = models.CharField(blank=True, max_length=100, default="")
    avatar = models.URLField(blank=True, default="")
    location = models.CharField(blank=True, max_length=100, default="")
    phone_number = models.CharField(blank=True, max_length=30, default="")
    about_me = models.TextField(blank=True, default="")
    user_hashtags = models.JSONField(default=list, blank=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user.email}'s profile"
