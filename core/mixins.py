from django.conf import settings
from django.db import models


class TimeStampedModelMixin(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class PostableMixin(TimeStampedModelMixin):
    """
    Inherits every object which needs content field along with created, and modified fields.
    ie) Post, Comment etc
    """
    content = models.TextField(verbose_name='내용')

    class Meta:
        abstract = True
