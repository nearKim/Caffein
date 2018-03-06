from django import forms
from .models import (
    Post,
    Photo,
)


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ('author', 'title',)


class PhotoForm(forms.ModelForm):
    class Meta:
        model = Photo
        fields = ('photo',)
