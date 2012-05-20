#-*- coding: utf8 -*-
from datetime import datetime


def site_globals(request):
    registration_end = datetime(2012, 5, 16, 23, 59)
    conference_day = datetime(2012, 5, 19)
    now = datetime.now()

    return {
        'site_title': u"ПрофсоUX",
        'site_name': u"Конференция по юзабилити и проектированию взаимодействия",
        'dates': {
            'registration_end': registration_end,
            'conference_day': conference_day
        },
        'states': {
            'registration_is_active': registration_end > now,
            'conference_ended': conference_day < now,
        }
    }
