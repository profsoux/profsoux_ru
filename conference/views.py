# -*- coding: utf8 -*-
# Create your views here.

import datetime

from django.shortcuts import render
from django.core.context_processors import csrf
from django.views.generic import ListView
from django.db.models import Count

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


def contacts(request):
    if request.method == 'POST':
        form = ContactsForm(request.POST)
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
        form = ContactsForm()
        c = {
            'state': 'default',
            'form': form
            }
    c.update(csrf(request))
    return render(request,
        'contacts.html',
        c)


def people(request):
    total = Participant.objects.all().aggregate(Count('first_name'))
    people_q = Participant.objects.filter(is_public=True).order_by('first_name')

    if ord(people_q[0].first_name.lower()[0]) < 1072:
        abc = [
            unichr(ord(u'a') + i) for i in xrange(0, 26)] + [
            unichr(ord(u'а') + i) for i in xrange(0, 6)] + [u'ё'] + [
            unichr(ord(u'а') + i) for i in xrange(6, 32)
            ]

    persons = {i: [] for i in abc}

    for person in people_q:
        try:
            persons[person.first_name.lower()[0]].append(person)
        except:
            persons_en[person.first_name.lower()[0]].append(person)

    people = [{i: persons[i]} for i in abc]

    block_1_end_letter = people_q[len(people_q) / 3].first_name.lower()[0]
    block_2_end_letter = people_q[len(people_q) / 3 * 2].first_name.lower()[0]

    block_1_end = abc.index(block_1_end_letter)
    block_2_end = abc.index(block_2_end_letter)

    return render(request, 'people.html', {
            'abc': abc,
            'people': people,
            'count': total['first_name__count'],
            'block_1_end': block_1_end,
            'block_2_end': block_2_end
        })
