from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.template import loader
from django.urls import reverse_lazy
from .models import User
from django.views.generic import (
    View,
    CreateView,
    UpdateView,
    DetailView
)
from .forms import (
    UserForm,

)
from django.contrib.auth import authenticate, login


class UserActionMixin(object):
    fields = ('name', 'email', 'phone', 'student_no', 'college', 'department',
              'student_category', 'enroll_year', 'enroll_semester', 'profile_pic')

    @property
    def success_msg(self):
        return NotImplemented

    def form_valid(self, form):
        messages.info(self.request, self.success_msg)
        return super(UserActionMixin, self).form_valid(form)


class UserCreateView(UserActionMixin, CreateView):
    model = User
    success_msg = "회원가입이 완료되었습니다."


class UserUpdateView(UserActionMixin, UpdateView):
    model = User
    success_msg = "회원정보가 수정되었습니다."


class UserDetail(DetailView):
    model = User


def user_delete_view(request):
    template = loader.get_template('accounts/user_delete_fake.html')
    return HttpResponse(template.render(context=None, request=request))


@login_required()
def account_index(request, user):
    return render(request, 'accounts/index.html', context={'user': user})
