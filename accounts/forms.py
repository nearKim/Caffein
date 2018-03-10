from django import forms

from .models import (
    User,
)


class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['email', 'name', 'phone', 'student_no', 'college', 'department',
                  'student_category', 'enroll_year', 'enroll_semester', 'profile_pic']

