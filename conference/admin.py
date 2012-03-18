#-*- coding: utf8 -*-
from django.contrib import admin
from conference.models import *

admin.site.register(Person)
admin.site.register(Lecture)
admin.site.register(Organization)
admin.site.register(Category)
admin.site.register(ScheduleSection)