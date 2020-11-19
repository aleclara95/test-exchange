from django.conf import settings
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import User


@admin.register(User)
class UserAdmin(UserAdmin):
	model = settings.AUTH_USER_MODEL
