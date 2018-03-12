from django.core.exceptions import ValidationError
from django.db import models
from django.conf import settings
from core.category import SEMESTER_CATEGORY
from core.mixins import (
    TimeStampedModelMixin
)


def validate_list(value):
    '''takes a text value and verifies that there is at least one comma '''
    values = value.split(',')
    if len(values) < 2:
        raise ValidationError(
            "The selected field requires an associated list of choices. Choices must contain more than one item.")


class Survey(models.Model):
    survey_year = models.PositiveIntegerField(null=False, blank=False, verbose_name='설문 년도')
    survey_semester = models.PositiveIntegerField(choices=SEMESTER_CATEGORY, blank=False, null=False, verbose_name='설문 학기')

    def questions(self):
        if self.pk:
            return Question.objects.filter(survey=self.pk).order_by('id')


class Category(models.Model):
    name = models.CharField(max_length=400)
    survey = models.ForeignKey(Survey, on_delete=models.CASCADE)

    def __str__(self):
        return self.name


class Question(TimeStampedModelMixin):
    TEXT = 'text'
    RADIO = 'radio'
    SELECT = 'select'
    SELECT_MULTIPLE = 'select-multiple'
    INTEGER = 'integer'

    QUESTION_TYPES = (
        (TEXT, '텍스트'),
        (RADIO, '라디오버튼'),
        (SELECT, '선택형'),
        (SELECT_MULTIPLE, '다중선택형'),
        (INTEGER, '숫자형'),
    )

    survey = models.ForeignKey(Survey, on_delete=models.PROTECT)
    text = models.CharField(max_length=200, blank=False, null=False, verbose_name='설문 내용')
    required = models.BooleanField(default=True, verbose_name='필수 여부')
    category = models.ForeignKey(Category, blank=True, null=True, on_delete=models.SET_NULL)

    question_type = models.CharField(max_length=200, choices=QUESTION_TYPES, default=TEXT, verbose_name='질문종류')
    # the choices field is only used if the question type
    choices = models.TextField(blank=True, null=True,
                               help_text='질문종류가 "라디오버튼", "선택형", "다중선택형" 이면 선택지들을 쉼표로 구분하여 입력하세요.')

    def save(self, *args, **kwargs):
        if (self.question_type == Question.RADIO or self.question_type == Question.SELECT
                or self.question_type == Question.SELECT_MULTIPLE):
            validate_list(self.choices)
        super(Question, self).save(*args, **kwargs)

    def get_choices(self):
        """ parse the choices field and return a tuple formatted appropriately
        for the 'choices' argument of a form widget."""
        choices = self.choices.split(',')
        choices_list = []
        for c in choices:
            c = c.strip()
            choices_list.append((c, c))
        choices_tuple = tuple(choices_list)
        return choices_tuple


class Response(TimeStampedModelMixin):
    # a response object is just a collection of questions and answers
    survey = models.ForeignKey(Survey, on_delete=models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)


class AnswerBase(TimeStampedModelMixin):
    question = models.ForeignKey(Question, on_delete=models.PROTECT)
    response = models.ForeignKey(Response, on_delete=models.PROTECT)


class AnswerText(AnswerBase):
    body = models.TextField(blank=True, null=True)


class AnswerRadio(AnswerBase):
    body = models.TextField(blank=True, null=True)


class AnswerSelect(AnswerBase):
    body = models.TextField(blank=True, null=True)


class AnswerSelectMultiple(AnswerBase):
    body = models.TextField(blank=True, null=True)


class AnswerInteger(AnswerBase):
    body = models.IntegerField(blank=True, null=True)
