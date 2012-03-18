from django import template

register = template.Library()


@register.inclusion_tag('list.html')
def category_list():
    pass


@register.inclusion_tag('list.html')
def speakers_list():
    pass


@register.inclusion_tag('list.html')
def partners_list():
    pass
