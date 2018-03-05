from django.db import models
from django.contrib.auth.models import User
from django.conf import settings
from Caffein.utils.mixins import (
    PostableMixin,
    TimeStampedModelMixin
)

SEMESTER_CATEGORY = (
    ('s', '1학기'),
    ('f', '2학기')
)


class Survey(models.Model, TimeStampedModelMixin):
    survey_year = models.DateField(null=False, blank=False)
    survey_semester = models.CharField(max_length=1, choices=SEMESTER_CATEGORY,
                                       blank=False,
                                       null=False)
    survey_question = models.TextField(blank=False, null=False)


class Answer(models.Model, TimeStampedModelMixin):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    survey = models.ForeignKey(Survey, on_delete=models.PROTECT)
    survey_answer = models.TextField()

    class Meta:
        unique_together = ['user', 'survey']
