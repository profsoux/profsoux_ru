# -*- coding: utf8 -*-
from django import forms

from conference.models import Participant, Contacts


class ParticipantForm(forms.ModelForm):
    first_name = forms.CharField(
        label="Имя",
        widget=forms.TextInput(
            attrs={
            'class': 'span4',
            'placeholder': 'Введите ваше имя'})
        )
    last_name = forms.CharField(
        label="Фамилия",
        widget=forms.TextInput(
            attrs={
            'class': 'span4',
            'placeholder': 'Введите вашу фамилию'})
        )
    phone = forms.CharField(
        label="Контактный телефон",
        widget=forms.TextInput(
            attrs={
            'class': 'span4',
            'placeholder': 'Введите номер телефона'})
        )
    email = forms.CharField(
        label="Email",
        widget=forms.TextInput(
            attrs={
            'class': 'span4',
            'placeholder': 'Введите ваш  email'})
        )
    company_name = forms.CharField(
        label="Компания",
        required=False,
        widget=forms.TextInput(
            attrs={
            'class': 'span4',
            'placeholder': 'Место работы или учёбы'})
        )
    position = forms.CharField(
        label="Должность",
        required=False,
        widget=forms.TextInput(
            attrs={
            'class': 'span4',
            'placeholder': 'Чем вы занимаетесь'})
        )
    comment = forms.CharField(
        label="Ваши пожелания и предложения",
        required=False,
        widget=forms.Textarea(
            attrs={
            'class': 'span6'})
        )

    class Meta:
        model = Participant


class ContactsForm(forms.ModelForm):
    name = forms.CharField(
        label="Имя",
        widget=forms.TextInput(
            attrs={
            'class': 'span4',
            'placeholder': 'Введите ваше имя'})
        )
    email = forms.EmailField(
        label="Email",
        widget=forms.TextInput(
            attrs={
            'class': 'span4',
            'placeholder': 'Введите ваш  email'})
        )
    site = forms.CharField(
        label="Сайт",
        required=False,
        widget=forms.TextInput(
            attrs={
            'class': 'span4'})
        )
    comment = forms.CharField(
        label="Сайт",
        widget=forms.Textarea(attrs={
        'class': 'span6'})
        )

    class Meta:
        model = Contacts
