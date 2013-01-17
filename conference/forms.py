# -*- coding: utf8 -*-
from django import forms

from conference.models import Participant, ParticipantFuture, Contacts, Result, LectureRate, Lecture


class ParticipantForm(forms.ModelForm):
    first_name = forms.RegexField(
        label="Имя",
        regex=u'^([А-яЁё \-]|\s)+$',
        widget=forms.TextInput(
            attrs={
            'class': 'span4',
            'required': 'required',
            'maxlength': 64,
            'placeholder': 'Введите ваше имя'})
        )
    last_name = forms.RegexField(
        label="Фамилия",
        regex=u'^([А-яЁё \-]|\s)+$',
        widget=forms.TextInput(
            attrs={
            'class': 'span4',
            'required': 'required',
            'maxlength': 64,
            'placeholder': 'Введите вашу фамилию'})
        )
    phone = forms.RegexField(
        label="Контактный телефон",
        regex=u'^(([0-9]|\+[0-9])[\- ]?)?(\(?\d{3}\)?[\- ]?)?[\d\- ]{7,10}$',
        widget=forms.TextInput(
            attrs={
            'class': 'span4',
            'required': 'required',
            'maxlength': 64,
            'placeholder': 'Введите номер телефона'})
        )
    email = forms.CharField(
        label="Email",
        widget=forms.TextInput(
            attrs={
            'class': 'span4',
            'required': 'required',
            'maxlength': 64,
            'placeholder': 'Введите ваш email'})
        )
    company_name = forms.CharField(
        label="Компания",
        required=False,
        widget=forms.TextInput(
            attrs={
            'class': 'span4',
            'maxlength': 64,
            'placeholder': 'Место работы или учёбы'})
        )
    position = forms.CharField(
        label="Должность",
        required=False,
        widget=forms.TextInput(
            attrs={
            'class': 'span4',
            'maxlength': 64,
            'placeholder': 'Чем вы занимаетесь'})
        )
    comment = forms.CharField(
        label="Ваши пожелания и предложения",
        required=False,
        widget=forms.Textarea(
            attrs={
            'class': 'span6',
            'maxlength': 512,
            'rows': 5})
        )
    confirmed = forms.CharField(
        initial='u',
        widget=forms.HiddenInput()
        )

    class Meta:
        model = Participant


class FutureForm(forms.ModelForm):
    first_name = forms.RegexField(
        label="Имя",
        regex=u'^([А-яЁё \-]|\s)+$',
        widget=forms.TextInput(
            attrs={
            'class': 'span4',
            'required': 'required',
            'maxlength': 64,
            'placeholder': 'Введите ваше имя'})
        )
    last_name = forms.RegexField(
        label="Фамилия",
        regex=u'^([А-яЁё \-]|\s)+$',
        widget=forms.TextInput(
            attrs={
            'class': 'span4',
            'required': 'required',
            'maxlength': 64,
            'placeholder': 'Введите вашу фамилию'})
        )
    email = forms.CharField(
        label="Email",
        widget=forms.TextInput(
            attrs={
            'class': 'span4',
            'required': 'required',
            'maxlength': 64,
            'placeholder': 'Введите ваш email'})
        )
    company_name = forms.CharField(
        label="Компания",
        required=False,
        widget=forms.TextInput(
            attrs={
            'class': 'span4',
            'maxlength': 64,
            'placeholder': 'Место работы или учёбы'})
        )
    position = forms.CharField(
        label="Должность",
        required=False,
        widget=forms.TextInput(
            attrs={
            'class': 'span4',
            'maxlength': 64,
            'placeholder': 'Чем вы занимаетесь'})
        )

    class Meta:
        model = ParticipantFuture


class ContactsForm(forms.ModelForm):
    name = forms.CharField(
        label="Имя",
        widget=forms.TextInput(
            attrs={
            'class': 'span4',
            'required': 'required',
            'maxlength': 64,
            'placeholder': 'Введите ваше имя'})
        )
    email = forms.EmailField(
        label="Email",
        widget=forms.TextInput(
            attrs={
            'class': 'span4',
            'required': 'required',
            'maxlength': 64,
            'placeholder': 'Введите ваш email'})
        )
    site = forms.CharField(
        label="Сайт",
        required=False,
        widget=forms.TextInput(
            attrs={
            'maxlength': 64,
            'class': 'span4'})
        )
    comment = forms.CharField(
        label="Сообщение",
        widget=forms.Textarea(
            attrs={
            'class': 'span6',
            'maxlength': 512,
            'required': 'required',
            'rows': 5})
        )

    class Meta:
        model = Contacts


def rate_field(label):
    return forms.ChoiceField(
        label=label,
        choices=[('', '-----')] + [(x, x) for x in range(5, 0, -1)],
        required=False,
        widget=forms.Select(
            attrs={
            'class': 'rate'
            })
        )


class ResultForm(forms.ModelForm):
    conf_rate_1 = rate_field('Уровень конференции в целом')
    conf_rate_2 = rate_field('Количество новой полезной информации')
    conf_rate_3 = rate_field('Качество организации')
    conf_rate_4 = rate_field('Уровень докладов')

    class Meta:
        model = Result


class LectureRateForm(forms.ModelForm):
    theme_rate = rate_field('Тема доклада')
    total_rate = rate_field('Общее впечатление')

    class Meta:
        model = LectureRate


class ConfirmForm(forms.Form):
    id = forms.IntegerField(
        widget=forms.HiddenInput()
        )
    code = forms.CharField(
        widget=forms.HiddenInput()
        )
    action = forms.CharField(
        widget=forms.HiddenInput()
        )
