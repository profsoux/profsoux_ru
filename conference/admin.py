#-*- coding: utf8 -*-
from hashlib import md5

from django.contrib import admin
from conference.models import *


class ParticipantAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'last_name', 'email', 'phone', 'is_public', 'allow_news', 'confirmed')
    list_filter = ('is_public', 'allow_news', 'confirmed')
    list_display_links = ('first_name', 'last_name')
    ordering = ['last_name', 'first_name']
    actions = ['send_mail']

    def send_mail(self, request, queryset):
        from django.core.mail import send_mail

        subject = u'Подтвердите участие в конференции ПрофсоЮкс 2012'
        sender = 'robot@profsoux.ru'
        text = u"""Здравствуйте, %s %s!

Вы зарегистрировались на конференцию ПрофсоЮкс 2012.

Нам необходимо уточнить количество участников, которые придут на
мероприятие лично.
(Онлайн трансляция будет доступна всем).

Пожалуйста, пройдите по ссылке для подтверждения участия:
http://uxspb.h404.ru/registration/confirm/?id=%s&code=%s&action=yes

Если вы передумали идти, огромная просьба также сообщить об этом:
http://uxspb.h404.ru/registration/confirm/?id=%s&code=%s&action=no
----------
Конференция по юзабилити
и проектированию взаимодействия «ProfsoUX»

Email: contact@ux-spb.ru
Телефон: +7 (812) 336 93 44
"""
        total_emails = len(queryset)
        sent_emails = total_emails
        for participant in queryset:
            m = md5()
            m.update(participant.email)
            code = m.hexdigest()
            recipients = [participant.email]

            message = text % (participant.first_name,
                participant.last_name,
                participant.id,
                code,
                participant.id,
                code
                )
            try:
                send_mail(subject, message, sender, recipients)
            except:
                sent_emails = sent_emails - 1

        self.message_user(request, "Разослано %s из %s писем" % (sent_emails, total_emails))

    send_mail.short_description = u"Разослать письмо с подтверждением"


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
