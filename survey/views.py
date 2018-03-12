
from django.core.exceptions import ValidationError
from django.db import transaction
from django.http import HttpResponse
from django.shortcuts import render
from django.contrib.auth import login
from django.views.generic import CreateView, ListView

from accounts.models import User
from accounts.tokens import account_activation_token
from .forms import (ResponseForm, QuestionFormSet)
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
            return render(request, 'accounts/user_verified_now_pay.html', {'operation': latest_os, 'user': user})
    else:
        form = ResponseForm(user=user, survey=survey)
    return render(request, 'survey/survey.html', {'response_form': form, 'survey': survey, 'user': user})


class SurveyList(ListView):
    model = Survey


class SurveyQuestionCreate(CreateView):
    model = Survey
    fields = '__all__'

    def get_context_data(self, **kwargs):
        data = super(SurveyQuestionCreate, self).get_context_data(**kwargs)
        if self.request.POST:
            data['questions'] = QuestionFormSet(self.request.POST)
        else:
            data['questions'] = QuestionFormSet()
        return data

    def form_valid(self, form):
        context = self.get_context_data()
        questions = context['questions']
        with transaction.atomic():
            self.object = form.save()

            if questions.is_valid():
                questions.instance = self.object
                questions.save()
        return super(SurveyQuestionCreate, self).form_valid(form)
