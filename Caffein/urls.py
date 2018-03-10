"""Caffein URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from django.conf.urls import include

from django.conf import settings
from django.contrib.auth import views as auth_views
if not settings.configured:
    settings.configure('Caffein.settings.dev', DEBUG=True)
from django.conf.urls.static import static
from core import views as core_views

urlpatterns = [
    path('', core_views.index, name='index'),
    path('login/', auth_views.LoginView.as_view(template_name='accounts/user_login.html'), name='login'),
    path('admin/', admin.site.urls, name='admin'),
    path('accounts/', include('accounts.urls', namespace='accounts')),
    path('postings/', include('postings.urls', namespace='postings')),
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
