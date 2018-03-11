from django.urls import path
from .views import *

app_name='partners'

urlpatterns = [
    path('<int:pk>/', PartnerDetail.as_view(), name='show-partner'),
    path('<int:pk>/register-meeting/', register_meeting, name='register-partner-meeting')
]