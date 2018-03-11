import os

from django.conf import settings
from django.contrib.postgres.fields import ArrayField
from django.urls import reverse

if not settings.configured:
    settings.configure('Caffein.settings.dev', DEBUG=True)

from django.contrib.auth.base_user import AbstractBaseUser
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.models import PermissionsMixin
from django.core.mail import send_mail
from django.contrib.auth.base_user import BaseUserManager

from django.db import models

from imagekit.models import ProcessedImageField
from imagekit.processors import Thumbnail
from django.utils.timezone import now
from core.category import (
    SEMESTER_CATEGORY,
    STUDENT_CATEGORY,
    COLLEGE_CATEGORY,
    DEPARTMENT_CATEGORY
)

from core.mixins import TimeStampedModelMixin
from .validators import *


def get_profile_path(instance, filename):
    user_id = instance.pk
    return 'accounts/profile/{}/{:%Y/%m/%d}/{}'.format(user_id, now(), filename)
    # return os.path.join(settings.MEDIA_ROOT,
    #                     'profiles/{}/{:%Y/%m/%d}/{}'.format(user_id, now(), filename))


class UserManager(BaseUserManager):
    use_in_migrations = True

    def _create_user(self, email, password, **extra_fields):
        """
        Creates and saves a User with the given email and password.
        """
        if not email:
            raise ValueError('The given email must be set')
        email_ = self.normalize_email(email)
        user = self.model(email=email_, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email, password, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self._create_user(email, password, **extra_fields)


class User(AbstractBaseUser, PermissionsMixin):
    """
    Custom user model for Caffein. Username would be replaced to Email field.
    is_new flag designates if this user is newmember or not.
    """
    email = models.EmailField(_('이메일'),
                              unique=True,
                              validators=[snumail_validator],
                              help_text='snu.ac.kr 계정 메일을 입력해주세요')
    name = models.CharField(_('이름'), max_length=30)
    phone = models.CharField(_('휴대폰번호'), max_length=20,
                             validators=[phone_validator],
                             blank=False,
                             null=False,
                             help_text='01x-xxxx-xxxx 형식으로 적어주세요')
    student_no = models.CharField(_('학번'), max_length=12,
                                  validators=[student_no_validator],
                                  blank=False,
                                  null=False,
                                  help_text='20xx-xxxxx 형식으로 적어주세요')
    college = models.CharField(_('단과대학'), max_length=3,
                               choices=COLLEGE_CATEGORY,
                               null=False,
                               blank=False)
    department = models.CharField(_('학과'), max_length=2,
                                  choices=DEPARTMENT_CATEGORY,
                                  null=False,
                                  blank=False)
    student_category = models.CharField(_('분류'), max_length=1,
                                        choices=STUDENT_CATEGORY,
                                        null=False,
                                        blank=False)
    enroll_year = models.IntegerField(_('가입년도'),
                                      validators=[enroll_year_validator],
                                      null=False,
                                      blank=False,
                                      default=now().year)
    enroll_semester = models.PositiveIntegerField(_('가입학기'),
                                                  choices=SEMESTER_CATEGORY,
                                                  default=1,
                                                  null=False,
                                                  blank=False)
    profile_pic = ProcessedImageField(blank=True,
                                      upload_to=get_profile_path,
                                      processors=[Thumbnail(100,100)],
                                      format='JPEG',
                                      options={'quality':60})
    rule_confirm = models.BooleanField(default=False,
                                       null=False,
                                       blank=False,
                                       verbose_name='약관동의')

    date_joined = models.DateTimeField(_('가입일'), auto_now_add=True)

    is_active = models.BooleanField(
        _('활동상태'),
        default=True,
        help_text=_(
            'Designates whether this user should be treated as active. '
            'Unselect this instead of deleting accounts.'
        ),
    )
    is_staff = models.BooleanField(
        _('운영진 여부'),
        default=False,
        help_text=_('Designates whether the user can log into this admin site.'),
    )

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    class Meta:
        verbose_name = _('회원')
        verbose_name_plural = _('회원')

    def get_full_name(self):
        '''
        Returns the first_name plus the last_name, with a space in between.
        '''
        # full_name = '%s %s' % (self.first_name, self.last_name)
        return self.name.strip()

    def get_short_name(self):
        '''
        Returns the short name for the user.
        '''
        return self.name

    def email_user(self, subject, message, from_email=None, **kwargs):
        '''
        Sends an email to this User.
        '''
        send_mail(subject, message, from_email, [self.email], **kwargs)

    def get_absolute_url(self):
        return reverse('accounts:user-detail', kwargs={'pk': self.pk})


class ActiveUser(TimeStampedModelMixin):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    active_year = models.PositiveIntegerField(default=now().year, verbose_name='활동년도')
    active_semester = models.PositiveIntegerField(choices=SEMESTER_CATEGORY,
                                                  null=False,
                                                  blank=False,
                                                  verbose_name='활동학기')
    is_new = models.BooleanField(default=False, blank=False,null=False, verbose_name='신입회원여부')
    is_paid = models.BooleanField(default=False, blank=False, null=False, verbose_name='입금확인')

    class Meta:
        unique_together = ['user', 'active_year', 'active_semester']
        verbose_name = '활동 회원'
        verbose_name_plural = '활동 회원'

