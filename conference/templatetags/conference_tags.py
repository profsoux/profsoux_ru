import os
import Image

from django import template

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


@register.inclusion_tag('tags/partners_list.html')
def partners_list():
    orgs = Partner.objects.filter(partner_type=0)
    partners = Partner.objects.filter(partner_type=1)
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
        image.thumbnail([x, y], Image.ANTIALIAS)
        try:
            image.save(miniature_filename, image.format, quality=90, optimize=1)
        except:
            image.save(miniature_filename, image.format, quality=90)

    return miniature_url


@register.filter
def multiply(value, arg):
    return int(value) * int(arg)
