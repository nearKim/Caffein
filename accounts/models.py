from django.db import models
from imagekit.models import ProcessedImageField
from imagekit.processors import Thumbnail
from django.conf import settings
from utils.category import (
    SEMESTER_CATEGORY,
    STUDENT_CATEGORY,
    COLLEGE_CATEGORY,
    DEPARTMENT_CATEGORY
)

from utils.mixins import (
    PostableMixin,
    TimeStampedModelMixin
)


class Profile(TimeStampedModelMixin):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, primary_key=True)
    name = models.CharField(max_length=30, null=False, blank=False, verbose_name='이름')
    birth_date = models.DateField(null=False, blank=False, verbose_name='생년월일')
    phone = models.CharField(max_length=20, blank=False, null=False, verbose_name='전화번호')
    student_no = models.CharField(max_length=12, blank=False, null=False, verbose_name='학번')
    college = models.CharField(max_length=3, choices=COLLEGE_CATEGORY,
                               null=False,
                               blank=False,
                               verbose_name='단과대학')
    department = models.CharField(max_length=2, choices=DEPARTMENT_CATEGORY,
                                  null=False,
                                  blank=False,
                                  verbose_name='학과')
    student_category = models.CharField(max_length=1,
                                        choices=STUDENT_CATEGORY,
                                        null=False,
                                        blank=False,
                                        verbose_name='학생 유형')
    enroll_year = models.DateField(auto_now_add=True, verbose_name='가입년도')
    enroll_semester = models.CharField(max_length=1, choices=SEMESTER_CATEGORY,
                                       null=False,
                                       blank=False,
                                       verbose_name='가입학기')
    profile_pic = ProcessedImageField(blank=True, upload_to='profile_pic',
                                      processors=[Thumbnail(300, 300)],
                                      format='JPEG',
                                      options={'quality': 60})

    def __str__(self):
        return self.name


class ActiveUser(TimeStampedModelMixin):
    user = models.OneToOneField(Profile, on_delete=models.CASCADE)
    active_year = models.DateField(auto_now=True, verbose_name='활동년도')
    active_semester = models.CharField(max_length=1, choices=SEMESTER_CATEGORY,
                                       null=False,
                                       blank=False,
                                       verbose_name='활동학기')
    is_paid = models.BooleanField(default=False, blank=False, null=False, verbose_name='입금확인')

    class Meta:
        unique_together = ['user', 'active_year', 'active_semester']


class Partners(TimeStampedModelMixin):
    partner_year = models.DateField(null=False, blank=False, verbose_name='짝지 년도')
    partner_semester = models.CharField(max_length=1,
                                        choices=SEMESTER_CATEGORY,
                                        null=False,
                                        blank=False,
                                        verbose_name='짝지 학기')
    old_partner = models.OneToOneField(ActiveUser,
                                       on_delete=models.CASCADE,
                                       verbose_name='위짝지',
                                       related_name='old_partner')
    new_partner1 = models.OneToOneField(ActiveUser,
                                        null=True,
                                        blank=True,
                                        on_delete=models.SET_NULL,
                                        default=None,
                                        verbose_name='아래짝지1',
                                        related_name='new_partner1')
    new_partner2 = models.OneToOneField(ActiveUser,
                                        null=True,
                                        blank=True,
                                        on_delete=models.SET_NULL,
                                        default=None,
                                        verbose_name='아래짝지2',
                                        related_name='new_partner2')
    new_partner3 = models.OneToOneField(ActiveUser,
                                        null=True,
                                        blank=True,
                                        on_delete=models.SET_NULL,
                                        default=None,
                                        verbose_name='아래짝지3',
                                        related_name='new_partner3')
    score = models.IntegerField(default=0, verbose_name='점수')
