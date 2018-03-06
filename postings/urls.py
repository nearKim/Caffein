from django.conf import settings
from django.urls import path
from . import views

app_name = 'postings'

urlpatterns = [
    path('', views.photo_post, name='photo-post'),
]
