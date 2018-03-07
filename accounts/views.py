from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.http import HttpResponse
from django.shortcuts import render
from .forms import (
    UserForm
)


def create_user(request):
    if request.method == 'POST':
        form = UserForm(request.POST)
        if form.is_valid():
            form.save()
            # user_email = form.cleaned_data('email')
            # raw_pass = form.cleaned_data.get('password')
            # user = authenticate(username=user_email, password=raw_pass)
            # login(request, user)
            return HttpResponse('SUCCESS!')
    else:
        form = UserForm(request.POST)
    return render(request, 'accounts/account_test.html', {'form': form})
