from django.db import models


class TimeStampedModelMixin(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class PostableMixin(TimeStampedModelMixin):

    content = models.TextField(verbose_name='내용')

    class Meta:
        abstract = True
