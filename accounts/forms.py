from django import forms
from django.views.generic import FormView
from django.views.generic.detail import SingleObjectMixin

from .models import (
    User,
    Partners,
    ActiveUser
)


class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['email', 'name', 'phone', 'student_no', 'college', 'department',
                  'student_category', 'enroll_year', 'enroll_semester', 'profile_pic']

