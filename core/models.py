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
        ('IB', 'IBK기업은행'),
        ('sh', '수협은행'),
        ('sm', '새마을금고')

    )
    current_year = models.PositiveIntegerField(null=False, blank=False, default=now().year, verbose_name='현재 년도')
    current_semester = models.PositiveIntegerField(null=False, blank=False, default=True, choices=SEMESTER_CATEGORY,
                                                   verbose_name='현재 학기')
    max_newcomers = models.PositiveIntegerField(null=False, blank=False, verbose_name='최대 신입수')
    partner_open_date = models.DateField(null=True, blank=True, verbose_name='짝지 시작일')
    partner_close_date = models.DateField(null=True, blank=True, verbose_name='짝지 마감일')
    money_account = models.CharField(max_length=20, null=False, blank=False, verbose_name='입금 계좌')
    bank_account = models.CharField(max_length=2, null=False, blank=False, choices=BANK_CATEGORY, verbose_name='입금 은행')
    boss = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.PROTECT)
    old_dues = models.PositiveIntegerField(blank=False, null=False, verbose_name='기존 가입비')
    new_dues = models.PositiveIntegerField(blank=False, null=False, verbose_name='신입 가입비')

    class Meta:
        verbose_name = '운영 정보'
        verbose_name_plural = '운영 정보'
