# -*- coding: utf8 -*-
# Create your views here.

import datetime
from icalendar import Calendar, Event

from django.shortcuts import render
from django.core.context_processors import csrf
from django.views.generic import ListView
from django.db.models import Count
from django.http import HttpResponse

from conference.models import *
from conference.forms import ParticipantForm, ContactsForm

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
    speakers = list(Speaker.objects.order_by('person__last_name'))

    speakers = [i.get_speaker() for i in speakers]
    return render(request,
        'speakers.html',
        {'speakers': speakers}
        )


def partners(request):
    partners = Partner.objects.filter(partner_type__gt=1).order_by('partner_type__weight', 'weight')
    return render(request,
        'companies.html',
        {
        'title': 'Партнёры',
        'companies': partners
        })


def organizers(request):
    orgs = Partner.objects.filter(partner_type=1).order_by('weight')
    return render(request,
        'companies.html',
        {
        'title': 'Организаторы',
        'companies': orgs
        })


def speaker(request, speaker_id):
    speaker = Speaker.objects.get(id=speaker_id).get_speaker()
    return render(request,
        'speaker.html',
        {'speaker': speaker})


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


def ical(request):
    events = ScheduleSection.objects.all()

    cal = Calendar()
    cal.add('prodid', u'-//Расписание конференции Profsoux//profsoux.ru//')
    cal.add('version', '2.0')

    for event in events:
        ical_event = Event()
        title = event.title or u""

        if event.lecture:
            speakers = event.lecture.get_speakers()

            ical_event.add('summary', u"%s%s «%s»" % (title, speakers, event.lecture.title))
        ical_event.add('dtstart', datetime.datetime.strptime('19.05.2012 %s' % str(event.start_time), '%d.%m.%Y %H:%M:%S'))
        ical_event.add('duration', datetime.timedelta(minutes=event.duration))

        cal.add_component(ical_event)

    response = HttpResponse(cal.to_ical(), mimetype="text/calendar")
    response['Content-Disposition'] = 'attachment; filename=%s.ics' % 'profsoux'

    return response


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

            subject = u'Регистрация на конференцию ProfsoUX'
            message = u'''Добрый день!

            Мы получили вашу заявку на участие в конференции UX-специалистов «ПрофсоUX».

            До встречи 19 мая 2012 в ИТМО!'''
            sender = 'robot@profsoux.ru'
            recipients = [form.cleaned_data['email']]

            from django.core.mail import send_mail
            send_mail(subject, message, sender, recipients)

            c = {
                'state': 'thanks',
                'form': ParticipantForm()
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

            subject = u'Сообщения с сайта profsoux.ru'
            message = u'''Имя: %s
                email: %s
                Сайт: %s
                Сообщение: %s''' % (form.cleaned_data['name'],
                    form.cleaned_data['email'],
                    form.cleaned_data['site'],
                    form.cleaned_data['comment'])
            sender = 'robot@profsoux.ru'
            recipients = ['contact@ux-spb.ru']

            from django.core.mail import send_mail
            send_mail(subject, message, sender, recipients)

            c = {
                'state': 'thanks',
                'form': ContactsForm()
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
    else:
        abc = [
            unichr(ord(u'а') + i) for i in xrange(0, 6)] + [u'ё'] + [
            unichr(ord(u'а') + i) for i in xrange(6, 32)
            ]

    persons = {}

    for i in abc:
        persons[i] = []

    for person in people_q:
        try:
            persons[person.first_name.lower()[0]].append(person)
        except:
            try:
                persons_en[person.first_name.lower()[0]].append(person)
            except:
                pass

    people = [{i: persons[i]} for i in abc]

    block_1_end_letter = people_q[len(people_q) / 3].first_name.lower()[0]
    block_2_end_letter = people_q[len(people_q) / 3 * 2].first_name.lower()[0]

    block_1_end = abc.index(block_1_end_letter)
    block_2_end = abc.index(block_2_end_letter)

    return render(request, 'people.html', {
            'abc': abc,
            'people': people,
            'count': total['first_name__count'],
            'anonimous': total['first_name__count'] - len(people_q),
            'block_1_end': (block_1_end + 1),
            'block_2_end': (block_2_end + 1)
        })


def map(request):
    return render(request, 'map.html', {})
