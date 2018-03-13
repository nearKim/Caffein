from django.contrib import admin

from meetings.models import CoffeeMeeting, CoffeeEducation, OfficialEvent
from .models import *

admin.site.register(Post)
admin.site.register(Photo)
# admin.site.register(Meeting)
admin.site.register(CoffeeEducation)
admin.site.register(CoffeeMeeting)
admin.site.register(Comment)
admin.site.register(OfficialEvent)
