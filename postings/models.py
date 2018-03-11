from django.core.exceptions import ValidationError
from django.db import models
from django.contrib.postgres.fields import ArrayField
from django.conf import settings
from django.utils.text import slugify
from datetime import datetime
import os

from accounts.models import ActiveUser
from core.mixins import PostableMixin
from cafe.models import Cafe


def get_photo_path(instance, filename):
    author = instance.post.author_id
    title = instance.post.title
    slug = slugify(title)
    return os.path.join(settings.MEDIA_ROOT,
                        'photo/{:%Y/%m/%d}/{}/{}-{}'.format(datetime.now(), author, slug, filename))


class Post(PostableMixin):
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    title = models.CharField(max_length=100, verbose_name='제목', help_text='제목을 입력해주세요. 100자 내외')

    def __str__(self):
        return self.title


class Photo(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, default=None, related_name='photo')
    photo = models.ImageField(upload_to=get_photo_path, verbose_name='사진')


class Meeting(Post):
    people_number = models.PositiveIntegerField(default=1, null=False, blank=False, verbose_name='참석 인원')
    participants = models.ForeignKey(ActiveUser, on_delete=models.PROTECT, verbose_name='참석자')
    meeting_date = models.DateField(null=False, blank=False, verbose_name='모임 일시')

    class Meta:
        abstract = True


class CoffeeMeeting(Meeting):
    cafe = models.ForeignKey(Cafe, on_delete=models.DO_NOTHING, blank=False, null=False)


class CoffeeEducation(Meeting):
    DRIP, CUPPING, ESPRESSO, ADMIN = 'd', 'c', 'e', 'a'
    EASY, HARD = 'e', 'h'

    EDUCATION_CATEGORY = (
        (DRIP, '드립 교육'),
        (CUPPING, '커핑 교육'),
        (ESPRESSO, '에스프레소 교육'),
        (ADMIN, '운영진 교육')
    )
    DIFFICULTY_CATEGORY = (
        (EASY, '기초'),
        (HARD, '심화')
    )

    category = models.CharField(max_length=1, choices=EDUCATION_CATEGORY,
                                null=False,
                                blank=False,
                                verbose_name='교육 분류')
    difficulty = models.CharField(max_length=1, choices=DIFFICULTY_CATEGORY,
                                  null=True,
                                  blank=True,
                                  verbose_name='난이도')
    address = models.CharField(max_length=100,
                               null=True,
                               blank=True,
                               verbose_name='교육 장소')

    # TODO: add lnglat variable for NAVER map , Google map link.


class OfficialEvent(Meeting):
    INTRODUCTION, WELCOME, MT, MARKET = 'i', 'w', 'm', 'k'
    EVENT_CATEGORY = (
        (INTRODUCTION, '동소제'),
        (WELCOME, '신환회'),
        (MT, 'MT'),
        (MARKET, '장터')
    )

    category = models.CharField(max_length=1, choices=EVENT_CATEGORY, null=False, blank=False)
    address = models.CharField(max_length=100,
                               null=True,
                               blank=True,
                               verbose_name='행사 장소')
    # TODO: add lnglat variable for NAVER map , Google map link.


class Comment(PostableMixin):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

# TODO: Create PhotoPost class and link every Post model dependent class to it.
