from django.contrib.postgres.fields import ArrayField
from django.db import models
from django.utils.timezone import now

from accounts.models import ActiveUser
from core.category import SEMESTER_CATEGORY
from core.mixins import TimeStampedModelMixin

from postings.models import (
    Post,
    Photo,
    Comment
)


class Partners(TimeStampedModelMixin):
    partner_year = models.PositiveIntegerField(default=now().year,
                                               null=False,
                                               blank=False,
                                               verbose_name='짝지 년도')
    partner_semester = models.PositiveIntegerField(choices=SEMESTER_CATEGORY,
                                                   null=False,
                                                   blank=False,
                                                   verbose_name='짝지 학기')
    old_partner = models.OneToOneField(ActiveUser,
                                       on_delete=models.CASCADE,
                                       verbose_name='위짝지',
                                       related_name='old_partner')
    new_partner = ArrayField(models.PositiveIntegerField(),
                             size=3,
                             verbose_name='아래짝지')
    score = models.PositiveIntegerField(default=0, verbose_name='점수')

    class Meta:
        verbose_name = '짝지'
        verbose_name_plural = '짝지'


class Partner_Meeting(Post):
    partners = models.ForeignKey(Partners, on_delete=models.CASCADE, verbose_name='짝지')
    participants = ArrayField(models.PositiveIntegerField(), verbose_name='참석자')
    meeting_date = models.DateField(null=False, blank=False, verbose_name='짝모 날짜')
