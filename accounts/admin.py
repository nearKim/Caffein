from django.contrib import admin

from .models import (
    User,
    ActiveUser,
    Partners
)

admin.site.register(User)

admin.site.register(ActiveUser)
admin.site.register(Partners)
