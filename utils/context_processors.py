#-*- coding: utf-8 -*-
from datetime import datetime, timedelta

from conference.models import Speaker, Participant, Lecture, Event


def site_globals(request):
    event = request.event
    two_weeks = timedelta(weeks=2)
    now = datetime.now().date()
    speakers = Speaker.objects.filter(event=event)
    participants = Participant.objects.filter(event=event)
    lectures = Lecture.objects.filter(event=event)

    return {
        'now': now,
        'event': event,
        'registration_url': Event.objects.get_registration_url(request),
        'site_title': u"ПрофсоUX",
        'site_name': event.description,
        'dates': {
            'registration_end': event.registration_end,
            'conference_day': event.date
        },
        'states': {
            'registration': event.get_registration_state(),
            'conference': event.get_state(),
            'conference_ended': event.date < now,
            'show_tweets': (event.date + two_weeks) > now >= event.date,
        },
        'counts': {
            'speakers': len(speakers),
            'participants': len(participants),
            'lectures': len(lectures),
        }
    }
