from django import forms
from .models import *


class MeetingForm(forms.ModelForm):
    class Meta:
        model = Meeting
        fields = ('author', 'title', 'content','participants', 'people_number', 'meeting_date')

#
# class ParticipantForm(forms.ModelForm):
#     class Meta:
#         model = Participants
#         fields = ('meeting', 'participant')
