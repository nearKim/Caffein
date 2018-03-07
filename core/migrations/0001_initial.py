# Generated by Django 2.0.2 on 2018-03-07 06:50

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='OperationScheme',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('current_year', models.PositiveIntegerField(default=2018, verbose_name='현재 년도')),
                ('current_semester', models.PositiveIntegerField(choices=[(1, '1학기'), (2, '2학기')], default=True, verbose_name='현재 학기')),
                ('max_newcomers', models.PositiveIntegerField(verbose_name='최대 신입수')),
                ('partner_open_date', models.DateField(blank=True, null=True, verbose_name='짝지 시작일')),
                ('partner_close_date', models.DateField(blank=True, null=True, verbose_name='짝지 마감일')),
                ('money_account', models.CharField(max_length=20, verbose_name='입금 계좌')),
                ('bank_account', models.CharField(choices=[('kb', 'KB국민은행'), ('nh', 'NH농협'), ('sh', '신한은행'), ('wr', '우리은행'), ('hn', '하나(구 외환)'), ('kk', '케이뱅크'), ('ka', '카카오뱅크'), ('kd', 'KDB산업은행'), ('IB', 'IBK기업은행'), ('sh', '수협은행'), ('sm', '새마을금고')], max_length=2, verbose_name='입금 은행')),
                ('old_dues', models.PositiveIntegerField(verbose_name='기존 가입비')),
                ('new_dues', models.PositiveIntegerField(verbose_name='신입 가입비')),
                ('boss', models.OneToOneField(on_delete=django.db.models.deletion.PROTECT, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': '운영 정보',
                'verbose_name_plural': '운영 정보',
            },
        ),
    ]
