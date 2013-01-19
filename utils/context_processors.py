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
    registration_state = "waiting"
    if event.registration_end and event.registration_start:
        if now > event.registration_end:
            registration_state = "closed"
        if event.registration_start <= now <= event.registration_end:
            registration_state = "active"

    return {
        'now': now,
        'event': event,
        'site_title': u"ПрофсоUX",
        'site_name': event.description,
        'dates': {
            'registration_end': event.registration_end,
            'conference_day': event.date
        },
        'states': {
            'registration': registration_state,
            'conference_ended': event.date < now,
            'show_tweets': (event.date + two_weeks) > now >= event.date,
        },
        'counts': {
            'speakers': len(speakers),
            'participants': len(participants),
            'lectures': len(lectures),
        }
    }
