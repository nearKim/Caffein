from django.contrib import messages
from django.forms import modelformset_factory
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render

from .models import Photo
from .forms import *


def photo_post(request):
    # TODO: Currently the number of available photos is limited to 3. Dynamic upload is required.
    photo_formset = modelformset_factory(Photo, fields=('photo',), extra=3)

    if request.method == 'POST':
        post_form = PostForm(request.POST)
        formset = photo_formset(request.POST, request.FILES)

        if post_form.is_valid() and formset.is_valid():
            post_form = post_form.save(commit=False)
            post_form.author = request.user
            post_form.save()

            for form in formset.cleaned_data:
                photo = form['photo']
                temp_photo = Photo(post=post_form, photo=photo)
                temp_photo.save()
            messages.success(request, "Photo successfully uploaded.")
            # TODO: Add proper redirection
            return HttpResponse("SUCCESS!")
        else:
            print(post_form.errors)
            print(formset.errors)
    else:
        post_form = PostForm()
        formset = photo_formset(queryset=Photo.objects.none())
        # TODO: Add proper rendering html
    return render(request, 'postings/test.html', {'postForm': post_form, 'formset': formset})
