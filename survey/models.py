from django.db import models
from django.contrib.auth.models import User

SEMESTER_CATEGORY = (
    ('s', '1학기'),
    ('f', '2학기')
)


class Survey(models.Model):
    survey_year = models.DateField(null=False, blank=False)
    survey_semester = models.CharField(max_length=1, choices=SEMESTER_CATEGORY,
                                       blank=False,
                                       null=False)
    survey_question = models.TextField(blank=False, null=False)

    # Default Data
    created_at = models.DateField(auto_now_add=True)
    modified_at = models.DateField(auto_now=True)


class Answer(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    survey = models.ForeignKey(Survey, on_delete=models.PROTECT)
    survey_answer = models.TextField()

    # Default Data
    created_at = models.DateField(auto_now_add=True)
    modified_at = models.DateField(auto_now=True)

    class Meta:
        unique_together = ['user', 'survey']
