# -*- coding: utf8 -*-
from django.db import models


class Person(models.Model):
    first_name = models.CharField("Имя", max_length=64)
    last_name = models.CharField("Фамилия", max_length=64)
    about = models.TextField("Краткая информация", blank=True)
    photo = models.ImageField("Фотография", upload_to='photos/persons', blank=True)
    email = models.EmailField("Email", max_length=64, blank=True)
    twitter = models.CharField("Аккаунт в Twitter", max_length=32, blank=True)
    site = models.URLField("Адрес сайта", blank=True)
    organization = models.ForeignKey("Organization", blank=True)

    class Meta:
        verbose_name = 'Персона'
        verbose_name_plural = 'Персоны'

    def __unicode__(self):
        return u"%2s %2s" % (self.first_name, self.last_name)


class Organization(models.Model):
    name = models.CharField("Название", max_length=255)
    logo = models.ImageField("Логотип", upload_to="logotypes", blank=True)
    site = models.URLField("Адрес сайта", blank=True)
    facebook = models.URLField("Страница в Facebook", blank=True)

    class Meta:
        verbose_name = 'Организация'
        verbose_name_plural = 'Организации'

    def __unicode__(self):
        return self.name


class Lecture(models.Model):
    title = models.CharField("Название доклада", max_length=255)
    speaker = models.ManyToManyField('Person', related_name='Докладчик')
    description = models.TextField("Описание доклада", blank=True)
    thesises = models.TextField("Тезисы доклада", blank=True)
    presentation = models.FileField("Презентация", upload_to='presentations/%Y', blank=True)
    slideshare_link = models.URLField("Ссылка на Slideshare", blank=True)

    class Meta:
        verbose_name = 'Доклад'
        verbose_name_plural = 'Доклады'

    def __unicode__(self):
        return u"%2s (%2s)" % (self.title, self.speaker)
