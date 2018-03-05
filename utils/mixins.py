from django.db import models


class TimeStampedModelMixin(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class PostableMixin(TimeStampedModelMixin):
    message = models.TextField()

    class Meta:
        abstract = True
