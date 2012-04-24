#-*- coding: utf8 -*-
from django.contrib import admin
from conference.models import *


class ParticipantAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'last_name', 'email', 'phone', 'is_public', 'allow_news')
    list_filter = ('is_public', 'allow_news')
    list_display_links = ('first_name', 'last_name')
    ordering = ['last_name', 'first_name']


class PartnerAdmin(admin.ModelAdmin):
    list_display = ('organization', 'partner_type', 'weight')
    list_filter = ('partner_type',)
    list_editable = ('partner_type', 'weight')


admin.site.register(Person)
admin.site.register(Lecture)
admin.site.register(Organization)
admin.site.register(Category)
admin.site.register(ScheduleSection)
admin.site.register(Speaker)
admin.site.register(Partner, PartnerAdmin)
admin.site.register(Participant, ParticipantAdmin)
admin.site.register(Menu)
admin.site.register(PartnerStatus)
