from django.db import models
from django.contrib.postgres.fields import ArrayField
from django.conf import settings
from utils.mixins import PostableMixin


class Post(PostableMixin):
    author = models.ForeignKey(settings.AUTH_USER_MODEL)
    title = models.CharField(max_length=100, verbose_name='제목', help_text='제목을 입력해주세요. 100자 내외')

    # TODO: add support for multiple photos.

    def __str__(self):
        return self.title


class Meeting(Post):
    people_number = models.PositiveIntegerField()
    participants = ArrayField(models.PositiveIntegerField(), size=people_number)
    meeting_date = models.DateTimeField()

    class Meta:
        abstract = True


class CoffeeMeeting(Meeting):
    # TODO: create CAFE DB and connect to it
    pass


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
    address = models.CharField(max_length=50,
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
    address = models.CharField(max_length=50,
                               null=True,
                               blank=True,
                               verbose_name='행사 장소')
    # TODO: add lnglat variable for NAVER map , Google map link.


class Comment(PostableMixin):
    post = models.ForeignKey(Post)
    author = models.ForeignKey(settings.AUTH_USER_MODEL)

# TODO: Create PhotoPost class and link every Post model dependent class to it.
