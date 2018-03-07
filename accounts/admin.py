from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User
from .models import (
    ActiveUser,
    Partners
)

admin.site.register(User)

admin.site.register(ActiveUser)
admin.site.register(Partners)
