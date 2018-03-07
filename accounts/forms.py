from django import forms
from django.contrib.auth.models import User

from .models import (

    Partners,
    ActiveUser
)
from django.conf import settings


class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('username', 'password', 'email')
