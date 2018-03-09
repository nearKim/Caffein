from .base import *
from django.contrib.messages import constants

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

# Messaging
MESSAGE_LEVEL = constants.DEBUG  # 지금부터 debug 레벨의 messages 를 남길 수 있음.
MESSAGE_TAGS = {constants.ERROR: 'danger'}

# Database
# https://docs.djangoproject.com/en/2.0/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'caffein',
        'USER': 'admin',
        'PASSWORD': 'winteriscoming',
        'HOST': 'localhost',
        'PORT': '5432',
    }
}

# LOGIN REDIRECT URL
LOGIN_REDIRECT_URL = 'account-redirect'
