from django.contrib import admin

from meetings.models import (
    Meeting,
    CoffeeMeeting,
    CoffeeEducation,
    OfficialEvent
)

admin.site.register(Meeting)
# Register your models here.
