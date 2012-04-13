from django import template
from conference.models import *
from conference.views import get_speakers_lectures

register = template.Library()


@register.inclusion_tag('category_list.html')
def category_list():
    categories = Category.objects.all()
    return {'items': categories}


@register.inclusion_tag('speakers_list.html')
def speakers_list():
    speakers = Speaker.objects.all()[:4]
    for speaker in speakers:
        speaker.lectures = get_speakers_lectures(speaker)
    return {'items': speakers}


@register.inclusion_tag('partners_list.html')
def partners_list():
    orgs = Partner.objects.filter(partner_type=0)
    partners = Partner.objects.filter(partner_type=1)
    return {
        'items': {
            'orgs': orgs,
            'partners': partners
            }
        }
