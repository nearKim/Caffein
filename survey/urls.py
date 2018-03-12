from django.conf import settings
from django.urls import path
from .views import survey_detail

app_name = 'surveys'

urlpatterns = [
    # id means User id
    path('<int:id>/', survey_detail, name='survey-detail')
]