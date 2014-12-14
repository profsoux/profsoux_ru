# coding=utf-8

from django import template
from django.utils.safestring import mark_safe

from registration.models import *

register = template.Library()
months_names = ['', 'январь', 'февраль', 'март', 'апрель', 'май', 'июнь', 'июль', 'август', 'сентябрь', 'октябрь',
                'ноябрь', 'декабрь',]

@register.inclusion_tag('tags/price_table.html', takes_context=True)
def price_table(context):
    items = Item.objects.filter(event=context['event'])
    price_items = []
    months = []
    for item in items:
        price_items.append({
            'title': item.title,
            'price': item.itemprice_set.all()
        })
    if len(items) == 0:
        return {
        'now': context['now'],
        'price_items': price_items,
        'months': months
    }

    for price_item in price_items[0]['price']:
        if price_item.available_from.month == price_item.available_to.month:
            months.append(months_names[price_item.available_from.month])
        else:
            months.append('{0}, {1}'.format(
                months_names[price_item.available_from.month],
                months_names[price_item.available_to.month]
            ))

    return {
        'now': context['now'],
        'price_items': price_items,
        'months': months
    }
