from django.forms import ValidationError
import re


def phone_validator(value):
    if not re.match(r'^(01[0169]{1}-[\d+]{3,4}-[\d+]{4})$', value):
        raise ValidationError('핸드폰 번호를 정확히 입력해 주세요.')


def student_no_validator(value):
    if not re.match(r'^(20[\d+]{2}-[\d+]{5})$', value):
        raise ValidationError('학번을 정확히 입력해 주세요.')


def enroll_year_validator(value):
    if not re.match(r'20[\d+]{2}', str(value)):
        raise ValidationError('가입년도를 정확히 입력해 주세요.')
