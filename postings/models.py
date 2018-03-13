from django.db import models
from django.conf import settings
from django.utils.text import slugify
from datetime import datetime
import os

from core.mixins import PostableMixin


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
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='photo')
    photo = models.ImageField(upload_to=get_photo_path, verbose_name='사진')


class Comment(PostableMixin):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    commenter = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

# TODO: Create PhotoPost class and link every Post model dependent class to it.
