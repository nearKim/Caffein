from django.urls import path, re_path
from django.contrib.auth import views as auth_views
from .views import *

app_name = 'accounts'

urlpatterns = [

    path('<int:pk>/profile/', UserDetail.as_view(), name='user-detail'),
    path('create/', UserCreateView.as_view(), name='user-add'),
    path('<int:pk>/update/', UserUpdateView.as_view(), name='user-update'),
    path('delete/', user_delete_view, name='user-delete'),
]
