from django.http import HttpResponse
from django.shortcuts import render

from accounts.models import User
from .forms import (ResponseForm)
from .models import (
    Survey,
    Category
)
from core.utils import get_latest_os


def SurveyDetail(request, id):
    latest_os = get_latest_os()
    survey = Survey.objects.get(survey_year=latest_os.current_year, survey_semester=latest_os.current_semester)
    user = User.objects.get(id=id)
    category_items = Category.objects.filter(survey=survey)
    categories = [c.name for c in category_items]
    print('categories for this survey:' + categories.__str__())

    if request.method == 'POST':
        print(request.method)
        print(request.user)
        form = ResponseForm(request.POST, user=user, survey=survey)
        if form.is_valid():
            response = form.save()
            return HttpResponse("씨발 됐다")
    else:
        print(request.method)
        print(request)
        form = ResponseForm(user=user, survey=survey)
    return render(request, 'survey/survey.html', {'response_form': form, 'survey': survey, 'categories': categories})
