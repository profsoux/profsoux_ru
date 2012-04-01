# -*- coding: utf8 -*-
from django import forms

from conference.models import Participant


class ParticipantForm(forms.ModelForm):
    class Meta:
        model = Participant
