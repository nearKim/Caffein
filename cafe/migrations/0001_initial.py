# Generated by Django 2.0.2 on 2018-03-07 03:27

from django.conf import settings
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Cafe',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=30, verbose_name='카페 한글 이름')),
                ('en_name', models.CharField(blank=True, max_length=50, null=True, verbose_name='카페 영문 이름')),
                ('address', models.CharField(max_length=100, verbose_name='카페 주소')),
                ('espresso_machine', models.CharField(blank=True, max_length=20, null=True, verbose_name='에스프레소 머신')),
                ('grinder', models.CharField(blank=True, max_length=20, null=True, verbose_name='그라인더')),
                ('price', models.CharField(blank=True, choices=[('l', '낮음'), ('m', '보통'), ('h', '높음')], max_length=1, null=True, verbose_name='가격대')),
            ],
        ),
        migrations.CreateModel(
            name='CafeComment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('modified', models.DateTimeField(auto_now=True)),
                ('content', models.TextField(verbose_name='내용')),
                ('cafe', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='cafe.Cafe')),
                ('commenter', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='CoffeeNote',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('modified', models.DateTimeField(auto_now=True)),
                ('coffee_category', models.CharField(choices=[('d', 'Hand drip'), ('e', 'Espresso variation')], max_length=1)),
                ('acidity', models.SmallIntegerField(default=0, validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(10)])),
                ('sweet', models.SmallIntegerField(default=0, validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(10)])),
                ('bitter', models.SmallIntegerField(default=0, validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(10)])),
                ('aroma', models.SmallIntegerField(default=0, validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(10)])),
                ('body', models.SmallIntegerField(default=0, validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(10)])),
                ('total', models.SmallIntegerField(default=0, validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(10)])),
                ('cafe', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='cafe.Cafe')),
                ('commenter', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
