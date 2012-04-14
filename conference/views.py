# Create your views here.

import datetime

from django.shortcuts import render
from django.core.context_processors import csrf
from django.views.generic import ListView

from conference.models import *
from conference.forms import ParticipantForm

conf_start = datetime.datetime(2012, 5, 29, 10, 00)


class Papers(ListView):
    model = Lecture
    context_object_name = 'papers'
    template_name = 'papers.html'


def index(request):
    people_count = Participant.objects.count()
    return render(request,
        'index.html',
        {'people_count': people_count}
        )


def speakers(request):
    speakers = list(Speaker.objects.all())
    for speaker in speakers:
        speaker.lectures = get_speakers_lectures(speaker)
    return render(request,
        'speakers.html',
        {'speakers': speakers}
        )


def speaker(request, speaker_id):
    speaker = Speaker.objects.get(id=speaker_id).person
    speaker.lectures = get_speakers_lectures(speaker)
    return render(request,
        'speaker.html',
        {'speaker': speaker})


def get_speakers_lectures(speaker):
    try:
        lectures = Lecture.objects.filter(speaker=speaker.id)
    except:
        lectures = {}
    return lectures


def schedule(request):
    sections = ScheduleSection.objects.order_by('start_time')
    items = []
    for item in sections:
        start_dt = datetime.datetime(2012, 5, 19,
            item.start_time.hour,
            item.start_time.minute)
        items.append({
            'section': item,
            'offset': (start_dt - conf_start).seconds / 60 / 15
            })
    return render(request,
        'schedule.html',
        {'items': items})


def paper(request, paper_id):
    paper = Lecture.objects.get(id=paper_id)
    return render(request,
        'paper.html',
        {'paper': paper})


def registration(request):
    if request.method == 'POST':
        form = ParticipantForm(request.POST)
        if form.is_valid():
            form.save()
            c = {
                'state': 'thanks'
                }
        else:
            c = {
            'state': 'default',
            'form': form
            }
    else:
        form = ParticipantForm()
        c = {
            'state': 'default',
            'form': form
            }
    c.update(csrf(request))
    return render(request,
        'registration.html',
        c)


def people(request):
    people_q = Participant.objects.filter(is_public=True).order_by('first_name')
    l = len(people_q)
    people = [
            people_q[0:l / 3],
            people_q[l / 3:l / 3 * 2],
            people_q[l / 3 * 2:]
        ]

    return render(request, 'people.html', {
            'people': people
        })
