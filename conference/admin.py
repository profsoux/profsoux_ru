#-*- coding: utf8 -*-
from hashlib import md5

from django.contrib import admin
from conference.models import *


class ParticipantAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'last_name', 'email', 'phone', 'is_public', 'allow_news', 'confirmed')
    list_filter = ('is_public', 'allow_news', 'confirmed')
    list_display_links = ('first_name', 'last_name')
    ordering = ['last_name', 'first_name']
    actions = ['send_mail', 'send_another_mail']

    def send_mail(self, request, queryset):
        from django.core import mail

        emails = []

        subject = u'Конференция ПрофсоUX // 19 мая (суббота), начало регистрации в 11:30'
        sender = u'Оргкомитет конференции ПрофсоUX <contact@profsoux.ru>'
        reply = 'no-reply@profsoux.ru'
        text = u"""Здравствуйте, %s!

мы ждем вас на конференции ПрофсоUX завтра, 19 мая (суббота).
11:30 - начало регистрации и приветственный кофе с печеньками.

Место проведения:
ИТМО, Кронверкский пр., 49, вход с ул. Сытнинской (www.profsoux.ru/location)
Ст. метро Горьковская.

Программа: www.profsoux.ru/schedule
Оnline-трансляция будет доступна бесплатно всем желающим на сайте www.profsoux.ru.

Вопросы присылайте, пожалуйста, в twitter #profsoux.

С уважением,
Юлия Крючкова
www.profsoUX.ru
"""
        for participant in queryset:
            m = md5()
            m.update(participant.email)
            code = m.hexdigest()
            recipients = [participant.email]

            message = text % (participant.first_name,
                participant.id,
                code,
                participant.id,
                code
                )

            emails.append(
                mail.EmailMessage(subject, message, sender, recipients,
                    headers={'Reply-To': reply})
                )

        connection = mail.get_connection()
        connection.open()

        connection.send_messages(emails)

        connection.close()

    send_mail.short_description = u"Разослать письмо О дате и месте"

    def send_another_mail(self, request, queryset):
        from django.core import mail

        emails = []

        subject = u'Online-трансляция конференции «ПрофсоUX» (www.profsoux.ru) // 19 мая (суббота) 12:30'
        sender = u'Оргкомитет конференции ПрофсоUX <contact@profsoux.ru>'
        reply = 'no-reply@profsoux.ru'
        text = u"""Здравствуйте, %s!

В рамках первой петербургской конференции по usability и user experience
на сайте www.profsoux.ru организована online-трансляция докладов и панельных дискуссий.

Доступ к трансляции бесплатен. Приглашаются все желающие.
Начало трансляции: 12:30, 19 мая 2012 года (суббота).

После окончания конференции на сайте будут опубликованы видеозаписи докладов.
Доступ к ним также будет бесплатен.

Вопросы по online-трансляции, как и в целом по конференции, присылайте, пожалуйста, в twitter (#profsoux).

С уважением,
Оргкомитет конференции ПрофсоUX
www.profsoUX.ru
"""
        for participant in queryset:
            m = md5()
            m.update(participant.email)
            code = m.hexdigest()
            recipients = [participant.email]

            message = text % (participant.first_name,
                participant.id,
                code,
                participant.id,
                code
                )

            emails.append(
                mail.EmailMessage(subject, message, sender, recipients,
                    headers={'Reply-To': reply})
                )

        connection = mail.get_connection()
        connection.open()

        connection.send_messages(emails)

        connection.close()

    send_another_mail.short_description = u"Разослать письмо о трансляции"


class PartnerAdmin(admin.ModelAdmin):
    list_display = ('organization', 'partner_type', 'weight')
    list_filter = ('partner_type',)
    list_editable = ('partner_type', 'weight')


class ScheduleAdmin(admin.ModelAdmin):
    list_display = ('start_time', 'duration', 'title', 'lecture', 'category')
    list_display_links = ('title', 'lecture')
    list_filter = ('category',)
    list_editable = ('start_time', 'duration', 'category')
    ordering = ['start_time']


admin.site.register(Person)
admin.site.register(Lecture)
admin.site.register(Organization)
admin.site.register(Category)
admin.site.register(ScheduleSection, ScheduleAdmin)
admin.site.register(Speaker)
admin.site.register(Partner, PartnerAdmin)
admin.site.register(Participant, ParticipantAdmin)
admin.site.register(Menu)
admin.site.register(PartnerStatus)
