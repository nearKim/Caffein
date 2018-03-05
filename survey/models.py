from django.db import models
from django.contrib.auth.models import User
from django.conf import settings
from utils.category import SEMESTER_CATEGORY
from utils.mixins import (
    PostableMixin,
    TimeStampedModelMixin
)


class Survey(TimeStampedModelMixin):
    survey_year = models.DateField(null=False, blank=False)
    survey_semester = models.CharField(max_length=1, choices=SEMESTER_CATEGORY,
                                       blank=False,
                                       null=False)
    survey_question = models.TextField(blank=False, null=False)


class Answer(TimeStampedModelMixin):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    survey = models.ForeignKey(Survey, on_delete=models.PROTECT)
    survey_answer = models.TextField()

    class Meta:
        unique_together = ['user', 'survey']
