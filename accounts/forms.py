from django import forms
from django.utils.translation import gettext_lazy as _

from .models import (
    User,
)
from django.contrib.auth.forms import UserCreationForm


class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['email', 'name', 'phone', 'student_no', 'college', 'department',
                  'student_category', 'enroll_year', 'enroll_semester', 'profile_pic']


class SignUpForm(UserCreationForm):
    error_messages = {
        'password_mismatch': _("비밀번호가 일치하지 않습니다."),
    }
    email = forms.EmailField(max_length=100,
                             help_text='SNU메일을 입력해주세요',
                             error_messages={'invalid': '이메일 주소가 부정확합니다.',
                                             'unique': '이미 같은 이메일이 존재합니다.'})
    password1 = forms.CharField(
        label=_("비밀번호"),
        strip=False,
        widget=forms.PasswordInput,
    )
    password2 = forms.CharField(
        label=_("비밀번호 확인"),
        widget=forms.PasswordInput,
        strip=False,
        help_text=_("확인을 위해 비밀번호를 다시한번 입력해주세요."),
    )

    def clean(self):
        cleaned_data = super(SignUpForm, self).clean()
        password = cleaned_data.get('password1')
        confirm_password = cleaned_data.get('password2')
        confirm_rule = cleaned_data.get('rule_confirm')

        if not confirm_rule:
            raise forms.ValidationError(
                "약관에 반드시 동의하셔야 합니다."
            )
        if not password == confirm_password:
            forms.ValidationError()
            raise forms.ValidationError(
                self.error_messages['password_mismatch'],
                code='password_mismatch'
            )
    # TODO: ADD dependent dropdown
    # TODO: ADD semester, year valiations
    class Meta:
        model = User
        fields = ['rule_confirm', 'email', 'password1', 'password2', 'name', 'phone', 'student_no', 'college',
                  'department', 'student_category', 'enroll_year', 'enroll_semester', 'profile_pic']
