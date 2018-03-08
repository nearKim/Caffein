from django.urls import path
from .views import *

app_name = 'accounts'

urlpatterns = [
    path('<int:pk>/', UserDetail.as_view(), name='user-detail'),
    path('create/', UserCreateView.as_view(), name='user-add'),
    path('<int:pk>/update/', UserUpdateView.as_view(), name='user-update'),
    path('<int:pk>/delete/', user_delete_view, name='user-delete'),
]
