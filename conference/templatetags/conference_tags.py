import os
import Image
import re

from django import template
from django.utils.safestring import mark_safe

from conference.models import *

register = template.Library()


@register.inclusion_tag('tags/category_list.html', takes_context=True)
def category_list(context):
    sections = ScheduleSection.objects.filter(event=context['request'].event).order_by('category')

    categories = map(lambda x: x.category, sections)

    return {'items': [v for i,v in enumerate(categories) if v not in categories[:i]]}


@register.inclusion_tag('tags/speakers_list.html', takes_context=True)
def speakers_list(context):
    speakers = Speaker.objects.filter(event=context['request'].event).order_by('?')[:3]
    for speaker in speakers:
        speaker.lectures = speaker.get_lectures_dict()
    return {'items': speakers}


@register.inclusion_tag('tags/partners_list.html', takes_context=True)
def partners_list(context, lang="ru"):
    if context['request'].path == '/':
        partners = Partner.objects.filter(partner_type__gt=1,
                                          event=context['request'].event).order_by('partner_type__weight', 'weight')
    else:
        partners = Partner.objects.filter(partner_type__gt=1, event=context['request'].event,
                                          partner_type__show_always=True).order_by('partner_type__weight', 'weight')
    orgs = Partner.objects.filter(partner_type=1, event=context['request'].event).order_by('weight')
    return {
        'lang': lang,
        'items': {
            'orgs': orgs,
            'partners': partners,
        },
    }


@register.inclusion_tag('tags/nav.html', takes_context=True)
def main_menu(context):
    items = Menu.objects.filter(event=context['request'].event).order_by('weight')
    path = context['request'].path
    return {
        'items': items,
        'path': path
    }


@register.inclusion_tag('tags/years.html', takes_context=True)
def years_menu(context):
    events = Event.objects.order_by('-date')
    path = context['request'].path

    for event in events:
        event.is_active = event == context['event']

    return {
        'events': events,
        'path': path,
        'event': context['event']
    }


@register.filter
def thumbnail(file, size='104x104'):
    # defining the size
    x, y = [int(x) for x in size.split('x')]
    # defining the filename and the miniature filename
    if os.path.exists(file.path):
        filehead, filetail = os.path.split(file.path)
        basename, ext = os.path.splitext(filetail)
        ext = ext if ext.lower() != '.gif' else '.png'
        miniature = basename + '_' + size + ext
        filename = file.path
        miniature_filename = os.path.join(filehead, miniature)
        filehead, filetail = os.path.split(file.url)
        miniature_url = filehead + '/' + miniature
        if os.path.exists(miniature_filename) and os.path.getmtime(filename) > os.path.getmtime(miniature_filename):
            os.unlink(miniature_filename)
        # if the image wasn't already resized, resize it
        if not os.path.exists(miniature_filename):
            image = Image.open(filename)
            format = image.format
            if format == 'GIF':
                image = image.convert('RGBA')
                format = 'PNG'

            size = image.size

            if size[0] < x or size[1] < y:
                _x = x if x > size[1] else size[1]
                _y = y if y > size[0] else size[0]
                delta_x = (_x - size[0]) / 2 if size[0] < x else 0
                delta_y = (_y - size[1]) / 2 if size[1] < y else 0

                image = image.crop((-delta_x, -delta_y, size[0] + delta_x, size[1] + delta_y))

            image.thumbnail([x, y], Image.ANTIALIAS)

            if format == 'PNG':
                image.save(miniature_filename, format, optimize=1)
            if format == 'JPEG':
                image.save(miniature_filename, format, quality=90)
    else:
        miniature_url = 'http://placehold.it/%s' % size

    return miniature_url


@register.filter
def multiply(value, arg):
    return int(value) * int(arg)


@register.filter
def pretty_url(url):
    pattern = re.compile(u'^https?://(.*[^/])/?$')
    try:
        name = re.findall(pattern, url)[0]
    except:
        name = url

    return mark_safe(u'<a href="%s" rel="nofollow" target="_blank">%s</a>' % (url, name))
#pretty_url.needs_autoescape = True
