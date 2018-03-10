from django.conf.urls import url
from django.urls import path, re_path
from django.contrib.auth import views as auth_views
from .views import *

app_name = 'accounts'

urlpatterns = [
    path('signup/', signup, name='user-signup'),
    path('activate/<int:uid>/<slug:token>/',activate, name='user-activate'),

    path('<int:pk>/profile/', UserDetail.as_view(), name='user-detail'),
    path('<int:pk>/update/', UserUpdateView.as_view(), name='user-update'),
    path('delete/', user_delete_view, name='user-delete'),
]
