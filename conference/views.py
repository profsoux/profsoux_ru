# -*- coding: utf8 -*-
# Create your views here.

import datetime
from hashlib import md5

import xlwt
from icalendar import Calendar, Event
import pytz
import vobject

from django.shortcuts import render
from django.core.context_processors import csrf
from django.views.generic import ListView
from django.db.models import Count, Min, Max
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required

from conference.models import *
from conference.forms import ParticipantForm, ContactsForm, ConfirmForm
from settings import MEDIA_ROOT, STATIC_ROOT, PROJECT_ROOT


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
    conf_start = datetime.datetime(2012, 5, 19, sections[0].start_time.hour)
    last_section_start = sections.order_by('-start_time')[0].start_time
    last_section = datetime.datetime(2012, 5, 19, last_section_start.hour, last_section_start.minute)
    conf_end = (last_section + datetime.timedelta(minutes=sections.order_by('-start_time')[0].duration))
    if conf_end.minute:
        captions = range(conf_start.hour, conf_end.hour + 2)
    else:
        captions = range(conf_start.hour, conf_end.hour + 1)
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
        {'items': items,
        'captions': captions})


def ical(request):
    CALENDAR_NAME = u'profsoux'
    CALENDAR_SHORT_NAME = u'profsoux.ru'
    events = ScheduleSection.objects.all()

    cal = Calendar()
    cal.add('prodid', u'-//%s//%s//' % (CALENDAR_NAME, CALENDAR_SHORT_NAME))
    cal.add('version', '2.0')
    cal.add('calscale', 'GREGORIAN')
    cal.add('X-ORIGINAL-URL', CALENDAR_SHORT_NAME)
    cal.add('method', 'PUBLISH')

    for event in events:
        ical_event = Event()
        ical_event.add('uid', str(event.id) + '@' + CALENDAR_SHORT_NAME)
        title = event.title or u""

        if event.lecture:
            speakers = event.lecture.get_speakers()
            ical_event.add('summary', u"%s%s «%s»" % (title, speakers, event.lecture.title))
        else:
            ical_event.add('summary', title)

        dtstart = datetime.datetime(2005, 4, 4, 8, 0, 0, tzinfo=pytz.utc)
        dtend = datetime.datetime(2005, 4, 4, 10, 0, 0, tzinfo=pytz.utc)
        ical_event.add('dtstart', dtstart)
        ical_event.add('dtend', dtend)
        ical_event.add('dtstamp', dtstart)

        cal.add_component(ical_event)

    response = HttpResponse(cal.to_ical(), mimetype="text/calendar")
    response['Content-Disposition'] = 'attachment; filename=%s.ics' % 'ical'

    return response


def ical2(request):
    CALENDAR_NAME = u'profsoux'
    CALENDAR_SHORT_NAME = u'profsoux.ru'
    events = ScheduleSection.objects.all()

    cal = vobject.iCalendar()
    cal.add('prodid').value = u'-//%s//%s//' % (CALENDAR_NAME, CALENDAR_SHORT_NAME)
    cal.add('method').value = 'PUBLISH'
    cal.add('version').value = '2.0'
    # cal.add('calscale', 'GREGORIAN')
    # cal.add('X-ORIGINAL-URL', CALENDAR_SHORT_NAME)

    for event in events:
        ical_event = cal.add('vevent')
        ical_event.add('uid').value = str(event.id) + '@' + CALENDAR_SHORT_NAME
        title = event.title or u""

        if event.lecture:
            speakers = event.lecture.get_speakers()
            ical_event.add('summary').value = u"%s%s «%s»" % (title, speakers, event.lecture.title)
        else:
            ical_event.add('summary').value = title

        dtstart = datetime.datetime.strptime('19.05.2012 %s' % str(event.start_time), '%d.%m.%Y %H:%M:%S')
        duration = datetime.timedelta(minutes=event.duration)
        dtend = dtstart + duration
        ical_event.add('dtstart').value = dtstart
        ical_event.add('dtend').value = dtend
        ical_event.add('dtstamp').value = dtstart

        # cal.add_component(ical_event)

    icalstream = cal.serialize()

    response = HttpResponse(icalstream, mimetype="text/calendar")
    # response['Content-Disposition'] = 'attachment; filename=%s.ics' % 'ical'

    return response


def pdf(request):
    from reportlab.lib.styles import getSampleStyleSheet
    from reportlab.lib.units import mm
    from reportlab.platypus import Paragraph, Table, TableStyle, SimpleDocTemplate, Image
    from reportlab.pdfbase import pdfmetrics
    from reportlab.pdfbase.ttfonts import TTFont

    events = ScheduleSection.objects.all()

    data = []

    for event in events:
        title = event.title or u""
        if event.lecture:
            speakers = event.lecture.get_speakers()
            title = u"%s%s «%s»" % (title, speakers, event.lecture.title)

        data.append([unicode(event.start_time), title])

    table = Table(data)

    pdfmetrics.registerFont(TTFont('font', PROJECT_ROOT + '/font.ttf'))

    styleSheet = getSampleStyleSheet()
    style = styleSheet['BodyText']
    style.fontName = 'font'
    style.spaceAfter = 10 * mm

    logo = Image(STATIC_ROOT + '/img/branding/logo.png')

    logo.drawHeight = 40 * mm * logo.drawHeight / logo.drawWidth
    logo.drawWidth = 40 * mm

    P = Paragraph('Конференция ProfsoUX', style)
    table.setStyle(TableStyle([('FONTNAME', (0, 0), (-1, -1), 'font')]))

    lst = []
    lst.append(logo)
    lst.append(P)
    lst.append(table)

    saved_file = MEDIA_ROOT + '/schedule.pdf'

    SimpleDocTemplate(saved_file, showBoundary=0).build(lst)

    f = open(saved_file)

    response = HttpResponse(f, mimetype='application/pdf')
    response['Content-Disposition'] = 'attachment; filename=ProfsoUX-2012-schedule.pdf'

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


def confirm(request):
    def check_participant(d):
        participant_id = d['id']
        participant = Participant.objects.get(id=participant_id)

        m = md5()
        m.update(participant.email)
        code = m.hexdigest()
        if code == d['code']:
            return participant
        else:
            return false

    if request.method == 'POST':
        participant = check_participant(request.POST)
        if participant:
            Participant.objects.filter(id=request.POST['id']).update(confirmed=request.POST['action'])
            c = {
                'state': 'thanks'
            }
        else:
            c = {
                'state': 'attack'
            }

    else:
        participant = check_participant(request.GET)

        if participant:
            try:
                action = request.GET['action'] or None
            except:
                action = None
            form = ConfirmForm({
                'id': participant.id,
                'code': request.GET['code'],
                'action': action
                })
            c = {
                'action': action,
                'form': form,
                'person': participant
            }
        else:
            c = {
                'state': 'attack'
            }

    c.update(csrf(request))
    return render(request,
        'confirm.html',
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
    total = Participant.objects.all().aggregate(Count('last_name'))
    people_q = Participant.objects.filter(is_public=True).order_by('last_name')

    if ord(people_q[0].last_name.lower()[0]) < 1072:
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
            persons[person.last_name.lower()[0]].append(person)
        except:
            try:
                persons[person.last_name.lower()[0]].append(person)
            except:
                pass

    people = [{i: persons[i]} for i in abc]

    block_1_end_letter = people_q[len(people_q) / 3].last_name.lower()[0]
    block_2_end_letter = people_q[len(people_q) / 3 * 2].last_name.lower()[0]

    block_1_end = abc.index(block_1_end_letter)
    block_2_end = abc.index(block_2_end_letter)

    return render(request, 'people.html', {
            'abc': abc,
            'people': people,
            'count': total['last_name__count'],
            'anonimous': total['last_name__count'] - len(people_q),
            'block_1_end': (block_1_end),
            'block_2_end': (block_2_end + 1)
        })


@login_required
def people_to_xls(request):
    font0 = xlwt.Font()
    font0.name = 'Arial'
    font0.colour_index = 0
    font0.bold = True

    font1 = xlwt.Font()
    font0.name = 'Arial'

    title_style = xlwt.XFStyle()
    title_style.font = font0

    data_style = xlwt.XFStyle()
    data_style.font = font1

    wb = xlwt.Workbook(encoding='utf8')
    ws = wb.add_sheet('Persons')

    ws.write(0, 0, 'Имя', title_style)
    ws.write(0, 1, 'Фамилия', title_style)
    ws.write(0, 2, 'Телефон', title_style)
    ws.write(0, 3, 'Email', title_style)
    ws.write(0, 4, 'Компания', title_style)
    ws.write(0, 5, 'Должность', title_style)
    ws.write(0, 6, 'Комментарии', title_style)
    ws.write(0, 7, 'Подтверждение участия', title_style)

    people = Participant.objects.order_by('id')

    i = 1
    for person in people:
        ws.write(i, 0, person.first_name, data_style)
        ws.write(i, 1, person.last_name, data_style)
        ws.write(i, 2, person.phone, data_style)
        ws.write(i, 3, person.email, data_style)
        ws.write(i, 4, person.company_name, data_style)
        ws.write(i, 5, person.position, data_style)
        ws.write(i, 6, person.comment, data_style)
        ws.write(i, 7, person.confirmed, data_style)
        i = i + 1

    filename = MEDIA_ROOT + '/persons.xls'
    wb.save(filename)

    f = open(filename)

    response = HttpResponse(f, mimetype='application/vnd.ms-excel')
    response['Content-Disposition'] = 'attachment; filename=ProfsoUX-2012.xls'

    return response


def map(request):
    return render(request, 'map.html', {})
