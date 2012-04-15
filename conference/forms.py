# -*- coding: utf8 -*-
from django import forms

from conference.models import Participant, Contacts


class ParticipantForm(forms.ModelForm):
    class Meta:
        model = Participant


class ContactsForm(forms.ModelForm):
    class Meta:
        model = Contacts
