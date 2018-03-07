from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator
from django.conf import settings
from core.mixins import (
    PostableMixin,
    TimeStampedModelMixin
)


class Cafe(models.Model):
    PRICE_CATEGORY = (
        ('l', '낮음'),
        ('m', '보통'),
        ('h', '높음')
    )

    name = models.CharField(max_length=30, null=False, blank=False, verbose_name='카페 한글 이름')
    en_name = models.CharField(max_length=50, null=True, blank=True, verbose_name='카페 영문 이름')
    address = models.CharField(max_length=100, null=False, blank=False, verbose_name='카페 주소')
    # TODO: Add lnglat variable for NAVER or Google map
    espresso_machine = models.CharField(max_length=20, null=True, blank=True, verbose_name='에스프레소 머신')
    grinder = models.CharField(max_length=20, null=True, blank=True, verbose_name='그라인더')
    price = models.CharField(max_length=1, choices=PRICE_CATEGORY,
                             null=True,
                             blank=True,
                             verbose_name='가격대')
    # TODO: Add multiple Images for Cafe model


class CafeComment(PostableMixin):
    cafe = models.ForeignKey(Cafe, on_delete=models.CASCADE)
    commenter = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)


class CoffeeNote(TimeStampedModelMixin):
    cafe = models.ForeignKey(Cafe, on_delete=models.CASCADE)
    commenter = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    coffee_category = models.CharField(max_length=1, choices=(
        ('d', 'Hand drip'),
        ('e', 'Espresso variation')
    ))
    acidity = models.SmallIntegerField(
        default=0,
        validators=[MinValueValidator(0), MaxValueValidator(10)])
    sweet = models.SmallIntegerField(
        default=0,
        validators=[MinValueValidator(0), MaxValueValidator(10)])
    bitter = models.SmallIntegerField(
        default=0,
        validators=[MinValueValidator(0), MaxValueValidator(10)])
    aroma = models.SmallIntegerField(
        default=0,
        validators=[MinValueValidator(0), MaxValueValidator(10)])
    body = models.SmallIntegerField(
        default=0,
        validators=[MinValueValidator(0), MaxValueValidator(10)])
    total = models.SmallIntegerField(
        default=0,
        validators=[MinValueValidator(0), MaxValueValidator(10)])
