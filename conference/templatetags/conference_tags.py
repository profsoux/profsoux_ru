import os
import Image
import re

from django import template
from django.utils.safestring import mark_safe

from conference.models import *
from conference.views import get_speakers_lectures

register = template.Library()


@register.inclusion_tag('tags/category_list.html')
def category_list():
    categories = Category.objects.all()
    return {'items': categories}


@register.inclusion_tag('tags/speakers_list.html')
def speakers_list():
    speakers = Speaker.objects.order_by('?')[:3]
    for speaker in speakers:
        speaker.lectures = get_speakers_lectures(speaker)
    return {'items': speakers}


@register.inclusion_tag('tags/partners_list.html', takes_context=True)
def partners_list(context):
    if context['request'].path == '/':
        partners = Partner.objects.filter(partner_type__gt=1).order_by('partner_type__weight', 'weight')
    else:
        partners = Partner.objects.filter(partner_type__gt=1, partner_type__show_always=True).order_by('partner_type__weight', 'weight')
    orgs = Partner.objects.filter(partner_type=1).order_by('weight')
    return {
        'items': {
            'orgs': orgs,
            'partners': partners
            }
        }


@register.inclusion_tag('tags/nav.html', takes_context=True)
def main_menu(context):
    items = Menu.objects.order_by('weight')
    path = context['request'].path
    return {
        'items': items,
        'path': path
    }


@register.filter
def thumbnail(file, size='104x104'):
    # defining the size
    x, y = [int(x) for x in size.split('x')]
    # defining the filename and the miniature filename
    filehead, filetail = os.path.split(file.path)
    basename, format = os.path.splitext(filetail)
    miniature = basename + '_' + size + format
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
        size = image.size
        if format == 'GIF':
            transparency = image.info['transparency']

        if size[0] > x and size[1] > y:
            image.thumbnail([x, y], Image.ANTIALIAS)
        else:
            delta_x = (x - size[0]) / 2
            delta_y = (y - size[1]) / 2

            image = image.crop((-delta_x, -delta_y, size[0] + delta_x, size[1] + delta_y))
            image.thumbnail([x, y], Image.ANTIALIAS)

        if format == 'GIF':
            image.save(miniature_filename, format, transparency=transparency)
        if format == 'PNG':
            image.save(miniature_filename, format, optimize=1)
        if format == 'JPEG':
            image.save(miniature_filename, format, quality=90)

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
