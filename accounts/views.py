from django.contrib import messages
from django.http import HttpResponse
from django.shortcuts import render
from django.urls import reverse_lazy
from .models import User
from django.views.generic import (
    View,
    CreateView,
    UpdateView,
    DetailView
)
from .forms import UserForm


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


def user_delete_view(request, pk):
    return HttpResponse("들어올땐 마음대로였지만 나갈땐 아니란다.")


class UserDetail(DetailView):
    model = User

