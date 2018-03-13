from django.db import models
from django.utils.timezone import now

from accounts.models import ActiveUser
from core.category import SEMESTER_CATEGORY
from core.mixins import TimeStampedModelMixin
from meetings.models import Meeting
from postings.models import Post


class Partners(TimeStampedModelMixin):
    partner_year = models.PositiveIntegerField(default=now().year,
                                               null=False,
                                               blank=False,
                                               verbose_name='짝지 년도')
    partner_semester = models.PositiveIntegerField(choices=SEMESTER_CATEGORY,
                                                   null=False,
                                                   blank=False,
                                                   verbose_name='짝지 학기')
    old_partner = models.ForeignKey(ActiveUser,
                                    on_delete=models.CASCADE,
                                    verbose_name='위짝지',
                                    related_name='old_partner')
    new_partner = models.OneToOneField(ActiveUser,
                                       on_delete=models.CASCADE,
                                       verbose_name='아래짝지',
                                       related_name='new_partner')
    score = models.PositiveIntegerField(default=0, verbose_name='점수')

    class Meta:
        verbose_name = '짝지'
        verbose_name_plural = '짝지'

    def __str__(self):
        return str(self.partner_year)+"년 "+str(self.partner_semester)+"학기"+" ("+self.old_partner.user.name+", "+self.new_partner.user.name+")"


class PartnerMeeting(Meeting):
    """
    Every PartnerMeeting needs an Old_partner.
    """
    old_partner = models.ForeignKey(ActiveUser, on_delete=models.CASCADE, verbose_name='위짝지')