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
        from django.core import mail

        emails = []

        subject = u'Осталось 4 дня до конференции ПрофсоUX (СПб, 19 мая 2012, суббота)'
        sender = u'Оргкомитет конференции ПрофсоUX <contact@profsoux.ru>'
        reply = 'no-reply@profsoux.ru'
        text = u"""Здравствуйте, %s!

Хочу уточнить, придете ли вы на конференцию ПрофсоЮкс 19 мая, в субботу, 12.00, НИУ ИТМО (http://profsoux.ru/location).
Нам хотелось бы понять, сколько нужно программок, сувениров и кофе с печеньками.

Если вы придете, нажмите "Я пойду" вот здесь:
http://profsoux.ru/registration/confirm/?id=%s&code=%s&action=yes

Если не сможете прийти, нажмите "Не пойду" здесь:
http://profsoux.ru/registration/confirm/?id=%s&code=%s&action=no
(У вас будет шанс посмотреть онлайн трансляцию конференции на www.ProfsoUX.ru).


Если у вас есть вопросы или вы не доверяете длинным ссылкам, пишите, звоните, мои контакты ниже.

С уважением,

Юлия Крючкова,
Председатель оргкомитета www.ProfsoUX.ru

Email: contact@ux-spb.ru
Тел. офис: +7 (812) 336 93 44, моб.: +7 (921) 741 48 23
Skype: julvk70
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
