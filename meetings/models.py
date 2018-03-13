from django.db import models

from accounts.models import ActiveUser
from cafe.models import Cafe
from postings.models import Post


class Meeting(Post):
    people_number = models.PositiveIntegerField(null=True, blank=True, verbose_name='참석 인원')
    meeting_date = models.DateField(null=False, blank=False, verbose_name='모임 일시')
    participants = models.ManyToManyField(ActiveUser)


# class Participants(models.Model):
#     """
#     Intermediate table for solving many-to-many relationship between Meeting and ActiveUser
#     """
#     meeting = models.ForeignKey(Meeting, on_delete=models.CASCADE)
#     participant = models.ForeignKey(ActiveUser, on_delete=models.CASCADE)


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


