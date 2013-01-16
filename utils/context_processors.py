#-*- coding: utf8 -*-
from datetime import datetime, timedelta

from conference.models import Speaker, Participant, Lecture


def site_globals(request):
    event = request.event
    two_weeks = timedelta(weeks=2)
    now = datetime.now().date()
    speakers = Speaker.objects.filter(event=event)
    participants = Participant.objects.filter(event=event)
    lectures = Lecture.objects.filter(event=event)

    return {
        'event': event,
        'site_title': u"ПрофсоUX",
        'site_name': event.description,
        'dates': {
            'registration_end': event.registration_end,
            'conference_day': event.date
        },
        'states': {
            'registration_is_active': event.registration_end > now if event.registration_end else None,
            'conference_ended': event.date < now,
            'show_tweets': (event.date + two_weeks) > now,
        },
        'counts': {
            'speakers': len(speakers),
            'participants': len(participants),
            'lectures': len(lectures),
        }
    }
