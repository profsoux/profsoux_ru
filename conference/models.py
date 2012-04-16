# -*- coding: utf8 -*-
from django.db import models

PARTNER_TYPE_CHOISES = (
    (0, 'Организаторы'),
    (1, 'Партнёры')
    )


class Menu(models.Model):
    name = models.CharField("Имя", max_length=64)
    link = models.CharField("Ссылка", max_length=64)
    weight = models.IntegerField('Порядок вывода')

    class Meta:
        verbose_name = 'Пункт меню'
        verbose_name_plural = 'Пункты меню'

    def __unicode__(self):
        return u'%s (%s)' % (self.name, self.link)


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
    description = models.TextField("Дополнительная информация", blank=True)

    class Meta:
        verbose_name = 'Организация'
        verbose_name_plural = 'Организации'

    def __unicode__(self):
        return self.name


class Partner(models.Model):
    organization = models.ForeignKey('Organization', verbose_name='Название')
    partner_type = models.IntegerField('Категория партнёрства', choices=PARTNER_TYPE_CHOISES)

    class Meta:
        verbose_name = 'Партнёр'
        verbose_name_plural = 'Партнёры конференции'

    def __unicode__(self):
        return self.organization.name


class Lecture(models.Model):
    title = models.CharField("Название доклада", max_length=255)
    speaker = models.ManyToManyField('Speaker', verbose_name='Докладчик')
    category = models.ForeignKey('Category', verbose_name='Категория доклада')
    timing = models.IntegerField('Предполагаемая длительность, мин.', blank=True, null=True)
    description = models.TextField("Описание доклада", blank=True)
    thesises = models.TextField("Тезисы доклада", blank=True)
    presentation = models.FileField("Презентация", upload_to='presentations/%Y', blank=True)
    slideshare_link = models.TextField("Ссылка на Slideshare", blank=True)

    class Meta:
        verbose_name = 'Доклад'
        verbose_name_plural = 'Доклады'

    def __unicode__(self):
        return u"%2s" % (self.title)


class Speaker(models.Model):
    person = models.ForeignKey('Person', verbose_name='Личность')

    class Meta:
        verbose_name = 'Докладчик'
        verbose_name_plural = 'Докладчики'

    def __unicode__(self):
        return self.person.__unicode__()


class Category(models.Model):
    title = models.CharField('Название категории', max_length=255)
    description = models.TextField('Описание', blank=True)
    class_name = models.CharField('CSS-класс', max_length=255)

    class Meta:
        verbose_name = 'Категория докладов'
        verbose_name_plural = 'Категории докладов'

    def __unicode__(self):
        return self.title


class ScheduleSection(models.Model):
    start_time = models.TimeField('Время начала секции')
    duration = models.IntegerField('Длительность, мин.', default=15)
    title = models.CharField('Название', max_length=64, blank=True)
    category = models.ForeignKey('Category', verbose_name='Категория', blank=True, null=True)
    lecture = models.ForeignKey('Lecture', verbose_name='Доклад', blank=True, null=True)

    class Meta:
        verbose_name = 'Секция расписания'
        verbose_name_plural = 'Секции расписания'

    def __unicode__(self):
        if self.title:
            return u"%2s. %2s" % (self.start_time, self.title)
        else:
            return u"%2s. %2s" % (self.start_time, self.category)


class Participant(models.Model):
    first_name = models.CharField("Имя", max_length=64)
    last_name = models.CharField("Фамилия", max_length=64)
    phone = models.CharField("Телефон", max_length=16)
    email = models.EmailField("Email")
    company_name = models.CharField("Компания", max_length=128, blank=True, null=True)
    position = models.CharField("Должность", max_length=64, blank=True, null=True)
    comment = models.TextField("Ваши предложения и пожелания", blank=True, null=True)
    allow_news = models.BooleanField("Новости конференции", default=True)
    is_public = models.BooleanField("Публикация профиля", default=True)

    class Meta:
        verbose_name = 'Участник'
        verbose_name_plural = 'Участники'

    def __unicode__(self):
        return u"%2s %2s" % (self.first_name, self.last_name)


class Contacts(models.Model):
    name = models.CharField("Имя", max_length=64)
    email = models.EmailField("Email")
    site = models.CharField("Сайт", max_length=64, blank=True, null=True)
    comment = models.TextField("Сообщение")

    class Meta:
        verbose_name = 'Сообщение в форме'
        verbose_name_plural = 'Сообщения в форме'

    def __unicods__(self):
        return u"%s (%s)" % (self.name, self.email)
