# coding=utf-8
from django.db import models
from conference.models import Event


class Item(models.Model):
    title = models.CharField('Тип билета', max_length=255)
    event = models.ForeignKey(Event, verbose_name='Событие')
    weight = models.IntegerField('Порядок сортировки', null=True, blank=True)

    class Meta:
        verbose_name = u'Тип билета'
        verbose_name_plural = u'Типы билетов'
        ordering = ['weight']

    def __unicode__(self):
        return u'{} на {}'.format(self.title, self.event)


class ItemPrice(models.Model):
    item = models.ForeignKey('Item', verbose_name='Тип билета')
    value = models.IntegerField('Стоимость')
    available_from = models.DateField('Доступно с')
    available_to = models.DateField('Доступно до')
    is_cancelled = models.BooleanField('Недоступно к продаже', default=False)

    class Meta:
        verbose_name = u'Стоимость билета'
        verbose_name_plural = u'Стоимость билета'
        ordering = ['available_from']

    def __unicode__(self):
        return u'{} ({} c {} до {})'.format(self.value, self.item, self.available_from, self.available_to)
