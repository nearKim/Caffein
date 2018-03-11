from django import forms
from .models import (
    Partners,
    Partner_Meeting
)


class PartnerForm(forms.ModelForm):
    class Meta:
        model = Partners
        fields='__all__'


class PartnerMeetingForm(forms.ModelForm):
    class Meta:
        model = Partner_Meeting
        fields='__all__'
