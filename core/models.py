import datetime
from django.db import models
from django.conf import settings
from django.utils.timezone import now
from core.category import SEMESTER_CATEGORY


class OperationScheme(models.Model):
    BANK_CATEGORY = (
        ('kb', 'KB국민은행'),
        ('nh', 'NH농협'),
        ('sh', '신한은행'),
        ('wr', '우리은행'),
        ('hn', '하나(구 외환)'),
        ('kk', '케이뱅크'),
        ('ka', '카카오뱅크'),
        ('kd', 'KDB산업은행'),
        ('ib', 'IBK기업은행'),
        ('sh', '수협은행'),
        ('sm', '새마을금고')

    )
    current_year = models.PositiveIntegerField(null=False, blank=False, default=now().year, verbose_name='현재 년도')
    current_semester = models.PositiveIntegerField(null=False, blank=False, default=True, choices=SEMESTER_CATEGORY,
                                                   verbose_name='현재 학기')
    old_register_start = models.DateField(null=True, blank=True, verbose_name="기존회원 재가입 시작일")
    old_register_end = models.DateField(null=True, blank=True, verbose_name="기존회원 재가입 마감일")

    new_register_end = models.DateField(null=False, blank=False, verbose_name='신입회원 가입마감일')

    max_newcomers = models.PositiveIntegerField(null=False, blank=False, verbose_name='최대 신입수')

    # This field is not needed hence right when a partner is confirmed, it should be opened immediately
    # partner_open_date = models.DateField(null=True, blank=True, verbose_name='짝지 시작일')
    partner_close_date = models.DateField(null=True, blank=True, verbose_name='짝지 마감일')

    money_account = models.CharField(max_length=20, null=False, blank=False, verbose_name='입금 계좌')
    bank_account = models.CharField(max_length=2, null=False, blank=False, choices=BANK_CATEGORY, verbose_name='입금 은행')

    boss = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, primary_key=False)

    old_pay = models.PositiveIntegerField(blank=False, null=False, verbose_name='기존 가입비')
    new_pay = models.PositiveIntegerField(blank=False, null=False, verbose_name='신입 가입비')

    def new_register_start(self):
        march_second = datetime.date(year=self.current_year, month=3, day=2)
        september_first = datetime.date(year=self.current_year, month=9, day=1)
        return march_second if self.current_semester == 1 else september_first

    new_register_start.short_description = '신입회원 가입시작일'

    class Meta:
        verbose_name = '운영 정보'
        verbose_name_plural = '운영 정보'
        unique_together = ['current_year', 'current_semester']
