from datetime import datetime

from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render
from django.views.generic import DetailView

from accounts.models import ActiveUser, User
from .models import Partners


class PartnerDetail(LoginRequiredMixin, DetailView):
    model = Partners

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        new_partner_list = self.object.new_partner
        new_partner_objs = User.objects.filter(pk__in=new_partner_list)
        print(new_partner_objs)
        context['new_partners'] = new_partner_objs
        context['now'] = datetime.now
        return context


def register_meeting(request):
    pass
