import datetime

from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView

from accounts.models import ActiveUser
from .models import Partners
from core.models import OperationScheme


class PartnerDetail(LoginRequiredMixin, ListView):

    def get_template_names(self):
        """
        If queryset returned by below function is None, it means No active user or partner connected to 'pk' exists.
        Else if Partner's current semester and year is equal to latest os scheme return details.
        Else, they are not equal to latest os scheme, it means new os scheme for the next semester is registered.
        Clearly the case which current partners are expired.
        :return:
        """
        queryset = self.get_queryset()
        if queryset is None:
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
        context = super().get_context_data(**kwargs)
        context['now'] = datetime.datetime.now()
        context['score'] = self.partner.score
        context['old_user'] = self.current_old_partner.user
        print(context)
        return context


def register_meeting(request):
    pass
