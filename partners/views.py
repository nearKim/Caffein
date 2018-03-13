import datetime

from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q
from django.forms import modelformset_factory
from django.http import HttpResponse
from django.shortcuts import render
from django.views.generic import ListView

from accounts.models import ActiveUser, User
from partners.forms import PartnerMeetingForm
from postings.forms import PostForm
from postings.models import Photo
from .models import Partners
from core.models import OperationScheme

# TODO: Register this variable
PARTNER_MEETING_SCORE = 2


class PartnerList(LoginRequiredMixin, ListView):

    def get_template_names(self):
        """
        If queryset returned by below function is None, it means No active user or partner connected to 'pk' exists.
        Else if Partner's current semester and year is equal to latest os scheme return details.
        Else, they are not equal to latest os scheme, it means new os scheme for the next semester is registered.
        Clearly the case which current partners are expired.
        """
        queryset = self.get_queryset()
        if queryset.count() == 0:
            return ['partners/partners_not_yet.html']

        current_year, current_semester = queryset.first().partner_year, queryset.first().partner_semester
        latest_scheme = OperationScheme.objects.latest('id')
        if latest_scheme.current_semester == current_semester and latest_scheme.current_year == current_year:
            if latest_scheme.partner_close_date > datetime.date.today():
                return ['partners/partners_list.html']
            else:
                return ['partners/partners_not_yet.html']
        else:
            return ['partners/partners_not_yet.html']

    def get_queryset(self):
        try:
            self.requested_member = ActiveUser.objects.get(user_id__exact=self.kwargs['pk'])
            if not self.requested_member.is_new:
                self.current_old_partner = self.requested_member
                self.partner = Partners.objects.filter(old_partner__user_id=self.current_old_partner.user.id).first()
            else:
                self.partner = Partners.objects.get(new_partner__user_id=self.kwargs['pk'])
                self.current_old_partner = self.partner.old_partner
        except(ActiveUser.DoesNotExist, Partners.DoesNotExist):
            return None
        else:
            return Partners.objects.all().filter(old_partner=self.current_old_partner)

    def get_context_data(self, **kwargs):
        try:
            context = super().get_context_data(**kwargs)
            context['now'] = datetime.datetime.now()
            context['score'] = self.partner.score
            context['old_user'] = self.current_old_partner.user
        except AttributeError:
            # In case context is none
            context = None
        return context


def partner_return(pk):
    """
    returns Partner objects based on passed parameter pk
    """
    objs = Partners.objects.select_related('old_partner').filter(old_partner__user_id=pk)
    if not objs.count() == 0:
        return objs
    else:
        old_pk = Partners.objects.get(new_partner__user_id=pk).old_partner.user_id
        return partner_return(old_pk)


def extract_every_member(queryset):
    """
    Extracts every member from given Partner queryset
    """
    return queryset.values_list('new_partner', flat=True).union(
        queryset.values_list('old_partner', flat=True))


def update_score(queryset):
    for partner in queryset:
        partner.score += PARTNER_MEETING_SCORE

@login_required()
def register_meeting(request, pk):
    # Initialize variables
    photo_formset = modelformset_factory(Photo, fields=('photo',), extra=2)
    partners_queryset = partner_return(pk)
    target = extract_every_member(partners_queryset)
    all_member_qs = ActiveUser.objects.select_related('user').filter(id__in=target)

    old_partner = all_member_qs.get(is_new=False)
    new_partners = all_member_qs.filter(is_new=True)

    if request.method == 'POST':
        formset = photo_formset(request.POST, request.FILES, queryset=Photo.objects.none())
        # No need to pass old_partner query to PartnerMeetingForm.
        partner_form = PartnerMeetingForm(new_partners, request.POST)

        if partner_form.is_valid() and formset.is_valid():
            meeting = partner_form.save(commit=False)
            meeting.people_number = len(request.POST.getlist('participants'))
            meeting.author = User.objects.get(id=pk)
            meeting.old_partner = old_partner
            meeting.save()
            # https://stackoverflow.com/questions/5612991/saving-many-to-many-data-via-a-modelform-in-django
            partner_form.save_m2m()

            for form in formset.cleaned_data:
                try:
                    photo = form['photo']
                except:
                    continue
                temp_photo = Photo(post=meeting, photo=photo)
                temp_photo.save()
            #     TODO: Go to Partner list
            return HttpResponse("fuck")
    else:
        partner_form = PartnerMeetingForm(all_member_qs.filter(is_new=True), partner=partners_queryset)
        formset = photo_formset(queryset=Photo.objects.none())
    return render(request, 'partners/partner_form.html', {'form': partner_form, 'formset': formset, 'old': old_partner})
