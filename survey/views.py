from django.core.exceptions import ValidationError
from django.http import HttpResponse
from django.shortcuts import render
from django.contrib.auth import login
from accounts.models import User
from accounts.tokens import account_activation_token
from .forms import (ResponseForm)
from .models import (
    Survey,
    Category
)
from core.utils import get_latest_os


def survey_detail(request, id):
    user = User.objects.get(id=id)
    # Quickfix: Don't know why but is_Active sets to True when this view is called.
    user.is_active = False
    latest_os = get_latest_os()
    survey = Survey.objects.get(survey_year=latest_os.current_year,
                                survey_semester=latest_os.current_semester)

    if request.method == 'POST':
        form = ResponseForm(request.POST, user=user, survey=survey)
        if form.is_valid():
            user.is_active = True
            user.save()
            login(request, user)
            response = form.save()
            return render(request, 'accounts/user_verified_now_pay.html', {'operation': latest_os, 'user':user})
    else:
        form = ResponseForm(user=user, survey=survey)
    return render(request, 'survey/survey.html', {'response_form': form, 'survey': survey, 'user': user})
