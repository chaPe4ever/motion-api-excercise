from django.contrib import admin

from user_profile.models import UserProfile


# Register your models here.
@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    pass
