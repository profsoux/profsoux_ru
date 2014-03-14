#-*- coding: utf-8 -*-
from hashlib import md5

from django.contrib import admin
from conference.models import *


class EventMixin(admin.ModelAdmin):
    def changelist_view(self, request, extra_context=None):
        ref = request.META.get('HTTP_REFERER', '')
        path = request.META.get('PATH_INFO', '')

        if not ref.split(path)[-1].startswith('?'):
            q = request.GET.copy()
            q['event__id__exact'] = request.event.id
            request.GET = q
            request.META['QUERY_STRING'] = request.GET.urlencode()

        return super(EventMixin, self).changelist_view(request, extra_context=extra_context)

    def formfield_for_foreignkey(self, db_field, request=None, **kwargs):
        if db_field.name == "event":
            kwargs['initial'] = request.event
        return super(EventMixin, self).formfield_for_foreignkey(db_field, request, **kwargs)


class ParticipantAdmin(EventMixin, admin.ModelAdmin):
    list_display = ('first_name', 'last_name', 'email', 'phone', 'is_public', 'allow_news', 'confirmed')
    list_filter = ('is_public', 'allow_news', 'confirmed')
    list_display_links = ('first_name', 'last_name')
    ordering = ['last_name', 'first_name']
    actions = ['send_mail', 'send_another_mail', 'to_results']

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
            # code = m.hexdigest()
            recipients = [participant.email]

            message = text % (participant.first_name)

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
            # code = m.hexdigest()
            recipients = [participant.email]

            message = text % (participant.first_name)

            emails.append(
                mail.EmailMessage(subject, message, sender, recipients,
                    headers={'Reply-To': reply})
                )

        connection = mail.get_connection()
        connection.open()

        connection.send_messages(emails)

        connection.close()

    send_another_mail.short_description = u"Разослать письмо о трансляции"

    def to_results(self, request, queryset):
        lectures_list = [1, 6, 5, 7, 18, 8, 11, 9, 4, 13, 14, 12, 16, 15, 3, 17]
        for participant in queryset:
            Result.objects.filter(participant=participant.id).delete()
            result = Result(participant=participant,
                email=participant.email)
            result.save()
            for lecture_id in lectures_list:
                lecture = Lecture.objects.get(id=lecture_id)
                rate = LectureRate(participant=result,
                    lecture=lecture)
                rate.save()


class PartnerAdmin(EventMixin, admin.ModelAdmin):
    list_display = ('organization', 'partner_type', 'weight')
    list_filter = ('partner_type',)
    list_editable = ('partner_type', 'weight')


class ScheduleAdmin(EventMixin, admin.ModelAdmin):
    list_display = ('start_time', 'duration', 'title', 'lecture',)
    list_display_links = ('title', 'lecture')
    # list_filter = ('')
    list_editable = ('start_time', 'duration')
    ordering = ['start_time']


from conference.forms import ResultForm, LectureRateForm


class LectureRateIline(admin.TabularInline):
    extra = 0
    form = LectureRateForm
    model = LectureRate
    verbose_name = 'Оценка доклада'
    verbose_name_plural = 'Оценки докладов'


class AddressBookInline(admin.StackedInline):
    extra = 1
    max_num = 1
    model = AddressBook

    fieldsets = (
        (u'Контакты', {
            'fields': (
                'moikrug',
                'twitter',
                'fb',
                'vk',
                'habr',
                'site')
        }),
        ('Я умею', {
            'fields': (
                'know_design',
                'know_research',
                'know_testing')
        }),
        ('На работе я', {
            'fields': (
                'work_pm',
                'work_programmer',
                'work_clientside',
                'work_manager',
                'work_director',
                'work_sale',
                'work_tester',
                'work_teacher',
                'work_writer',
                'work_student',
                'work_designer',
                )
        }),
        ('Я параноик?', {
            'fields': (
                'no_book',
                'no_group',
                'no_invite')
        }),
    )

    verbose_name = 'Карточка ProfsoUX'
    verbose_name_plural = 'Адресная книга'


class ResultAdmin(admin.ModelAdmin):
    form = ResultForm
    inlines = [
        AddressBookInline,
        LectureRateIline,
    ]

    def first_name(self):
        return self.participant.first_name

    def last_name(self):
        return self.participant.last_name

    def confirmed(self):
        return self.participant.confirmed

    list_display = [last_name, first_name, confirmed]
    list_display_links = [first_name, last_name]
    # list_filter = [confirmed]
    ordering = ['-participant__confirmed', 'participant__first_name']
    search_fields = ['participant__first_name', 'participant__last_name']


class MenuAdmin(EventMixin, admin.ModelAdmin):
    list_display = ["name", "link"]

class EventAdmin(admin.ModelAdmin):
    list_display = ['domain', 'default']


admin.site.register(Person)
admin.site.register(Lecture, EventMixin)
admin.site.register(Organization)
admin.site.register(Category)
admin.site.register(ScheduleSection, ScheduleAdmin)
admin.site.register(Speaker, EventMixin)
admin.site.register(Partner, PartnerAdmin)
admin.site.register(Participant, ParticipantAdmin)
admin.site.register(Menu, MenuAdmin)
admin.site.register(PartnerStatus)
admin.site.register(Result, ResultAdmin)
admin.site.register(LectureRate)
admin.site.register(AddressBook)
admin.site.register(Event, EventAdmin)
admin.site.register(ScheduleFlow)
