from django import forms

from accounts.models import ActiveUser
from .models import (
    Partners
)
from partners.models import PartnerMeeting


class PartnerForm(forms.ModelForm):
    class Meta:
        model = Partners
        fields = '__all__'


class PartnerMeetingForm(forms.ModelForm):
    meeting_date = forms.DateField(
        widget=forms.TextInput(
            attrs={'type': 'date'}
        )
    )

    def __init__(self, queryset=None, *args, **kwargs):
        # Utilizing ModelMultipleChoiceField()
        # https://stackoverflow.com/questions/5367818/django-forms-and-modelmultiplechoicefield-when-working-with-existing-records
        self.partner = kwargs.pop('partner', None)
        super(PartnerMeetingForm, self).__init__(*args, **kwargs)
        if queryset:
            self.fields['participants'] = forms.ModelMultipleChoiceField(queryset=queryset,
                                                                         widget=forms.CheckboxSelectMultiple())

    class Meta:
        model = PartnerMeeting
        fields = ['title', 'content', 'participants', 'meeting_date']
