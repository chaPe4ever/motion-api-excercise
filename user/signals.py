from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver

from user_profile.models import UserProfile


@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        # Create author profile
        UserProfile.objects.create(user=instance)
