# -*- coding: utf-8 -*-
from datetime import datetime

from django.db import models
from django.db.models import Q
from django.core.exceptions import ObjectDoesNotExist, MultipleObjectsReturned


class Menu(models.Model):
    name = models.CharField("Имя", max_length=64)
    link = models.CharField("Ссылка", max_length=64)
    weight = models.IntegerField('Порядок вывода')
    event = models.ForeignKey('Event')

    class Meta:
        verbose_name = 'Пункт меню'
        verbose_name_plural = 'Пункты меню'

    def __unicode__(self):
        return u'%s (%s)' % (self.name, self.link)


class EventManager(models.Manager):
    def get_current_event(self, request):
        try:
            event = self.get(domain=request.META['HTTP_HOST'])
        except ObjectDoesNotExist:
            event = self.get_default_event()
        return event

    def get_default_event(self):
        try:
            event = self.get(default=True)
        except ObjectDoesNotExist:
            event = (self.order_by('date') or [None])[0]
        except MultipleObjectsReturned:
            event = self.filter(default=True)[0]
        return event

    def get_registration_url(self, request):
        event = self.get_default_event()
        if event is None:
            return
        domain = event.domain if event != self.get_current_event(request) else None
        if event.get_registration_state() != 'waiting':
            path = '/registration/'
        else:
            path = '/registration/future/'
        return 'http://%s%s' % (domain, path) if domain else path


class Event(models.Model):
    objects = EventManager()
    domain = models.CharField('Доменное имя', max_length=64)
    short_name = models.CharField('Краткое назание', max_length=8)
    default = models.BooleanField('Активная конферениция', default=False)
    show_programm = models.BooleanField('Показывать программу', default=False)
    title = models.CharField('Название', max_length=256)
    description = models.TextField('Описание', null=True, blank=True)
    date = models.DateField('Дата проведения')
    registration_start = models.DateField('Дата начала приёма заявок', null=True, blank=True)
    registration_end = models.DateField('Дата окончания приёма заявок', null=True, blank=True)
    city = models.CharField('Город проведения', max_length=64)
    place = models.CharField('Место проведения', max_length=64, null=True, blank=True)
    address = models.TextField('Адрес места проведения', null=True, blank=True)
    coordinates = models.CharField('Координтаты места проведения', max_length=24, null=True, blank=True)
    place_note = models.TextField('Дополнительная информация о месте проведения', null=True, blank=True)
    use_sections = models.BooleanField('Доклады делятся по секциям', default=False)
    use_flows = models.BooleanField('Конференция в несколько потоков', default=False)

    class Meta:
        verbose_name = 'Событие'
        verbose_name_plural = 'События'

    def get_registration_state(self):
        now = datetime.now().date()
        state = 'waiting'
        registration_end = self.registration_end if self.registration_end else self.date
        if self.registration_start:
            if now > registration_end:
                state = "closed"
            if self.registration_start <= now <= registration_end:
                state = "active"
        return state

    def get_state(self):
        now = datetime.now().date()
        state = 'in_progress'
        if now < self.date:
            state = 'waiting'
        if now > self.date:
            state = 'ended'
        return state

    def is_ended(self):
        return self.date < datetime.now().date()

    def __unicode__(self):
        return self.domain


class Person(models.Model):
    first_name = models.CharField("Имя", max_length=64)
    last_name = models.CharField("Фамилия", max_length=64)
    about = models.TextField("Краткая информация", blank=True)
    photo = models.ImageField("Фотография", upload_to='photos/persons', blank=True)
    email = models.EmailField("Email", max_length=64, blank=True)
    twitter = models.CharField("Аккаунт в Twitter", max_length=32, blank=True)
    site = models.URLField("Адрес сайта", blank=True)
    organization = models.ForeignKey("Organization", blank=True, null=True)

    class Meta:
        verbose_name = 'Персона'
        verbose_name_plural = 'Персоны'

    def __unicode__(self):
        return u"%2s %2s" % (self.first_name, self.last_name)

    def get_absolute_url(self):
        return '/persons/%s/' % self.id


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
    partner_type = models.ForeignKey('PartnerStatus', verbose_name='Категория партнёрства')
    status = models.CharField('Статус партнёра', max_length=32, blank=True, null=True)
    weight = models.IntegerField('Порядок вывода', blank=True, null=True)
    event = models.ForeignKey(Event)

    class Meta:
        verbose_name = 'Партнёр'
        verbose_name_plural = 'Партнёры конференции'

    def __unicode__(self):
        return self.organization.name


class PartnerStatus(models.Model):
    title = models.CharField('Тип партнёрства', max_length=255)
    title_plural = models.CharField('Тип партнёрства (множ. число)', max_length=255)
    weight = models.IntegerField('«Вес» партнёрства')
    show_always = models.BooleanField('Показывать на всех страницах')

    class Meta:
        verbose_name = 'Тип партнёрства'
        verbose_name_plural = 'Типы партнёрства'

    def __unicode__(self):
        return self.title


class Lecture(models.Model):
    title = models.CharField("Название доклада", max_length=255)
    speaker = models.ManyToManyField('Speaker', verbose_name='Докладчик')
    category = models.ForeignKey('Category', verbose_name='Категория доклада', blank=True, null=True)
    timing = models.IntegerField('Предполагаемая длительность, мин.', blank=True, null=True)
    description = models.TextField("Описание доклада", blank=True)
    thesises = models.TextField("Тезисы доклада", blank=True)
    presentation = models.FileField("Презентация", upload_to='presentations/%Y', blank=True)
    slideshare_link = models.TextField("Ссылка на Slideshare", blank=True)
    vimeo_id = models.CharField("ID ролика на Vimeo", max_length=64, blank=True, null=True,
        help_text="Последовательность символов в URL после https://vimeo.com/")
    event = models.ForeignKey(Event)

    def get_speakers(self):
        result = ", ".join([unicode(i) for i in list(self.speaker.all())])
        return result

    def __unicode__(self):
        return u"%2s" % (self.title)

    def get_absolute_url(self):
        return '/papers/%s/' % self.id

    @property
    def start_time(self):
        return self.schedule.all()[0].start_time

    class Meta:
        verbose_name = 'Доклад'
        verbose_name_plural = 'Доклады'


class Speaker(models.Model):
    person = models.ForeignKey('Person', verbose_name='Личность')
    event = models.ForeignKey(Event)

    class Meta:
        verbose_name = 'Докладчик'
        verbose_name_plural = 'Докладчики'

    def get_lectures_dict(self):
        try:
            lectures = Lecture.objects.filter(speaker=self.id)
        except:
            lectures = {}
        return lectures

    def __unicode__(self):
        return self.person.__unicode__()

    def get_absolute_url(self):
        return '/speakers/%s/' % self.id


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
    lecture = models.ForeignKey('Lecture', verbose_name='Доклад', blank=True, null=True, related_name='schedule')
    flow = models.ManyToManyField('ScheduleFlow', blank=True, null=True,
                                  verbose_name="Поток",
                                  help_text="Можно выбрать несколько потоков одновременно")
    flow_slot = models.IntegerField('Номер слота', blank=True, null=True,
                                    help_text="Используется для нескольких докладов, идущих подряд")
    event = models.ForeignKey(Event)

    class Meta:
        verbose_name = 'Секция расписания'
        verbose_name_plural = 'Секции расписания'

    def get_title(self):
        return self.lecture.title if self.lecture is not None else self.title

    def get_absolute_url(self):
        return self.lecture.get_absolute_url() if self.lecture is not None else None

    def get_speakers(self):
        return self.lecture.get_speakers() if self.lecture is not None else None

    def __unicode__(self):
        if self.title:
            return u"%2s. %2s" % (self.start_time, self.title)
        else:
            return u"%2s. %2s" % (self.start_time, self.category)


class ScheduleFlow(models.Model):
    title = models.CharField('Название', max_length=64)
    start_time = models.TimeField('Время начала первого доклада')
    event = models.ForeignKey(Event)

    class Meta:
        verbose_name = 'Поток'
        verbose_name_plural = 'Потоки'

    def __unicode__(self):
        return self.title


class Participant(models.Model):
    first_name = models.CharField("Имя", max_length=64)
    last_name = models.CharField("Фамилия", max_length=64)
    phone = models.CharField("Телефон", max_length=24, blank=True, null=True)
    email = models.EmailField("Email", blank=True, null=True)
    company_name = models.CharField("Компания", max_length=128, blank=True, null=True)
    position = models.CharField("Должность", max_length=64, blank=True, null=True)
    comment = models.TextField("Ваши предложения и пожелания", blank=True, null=True)
    allow_news = models.BooleanField("Новости конференции", default=True)
    is_public = models.BooleanField("Публикация профиля", default=True)
    confirmed = models.CharField("Подтверждение участия", max_length=3,
        choices=(('yes', 'Пойду'), ('no', 'Не пойду'), ('u', 'Неизвестно')),
        blank=True, default='u')
    event = models.ForeignKey(Event)

    class Meta:
        verbose_name = 'Участник'
        verbose_name_plural = 'Участники'
        unique_together = ("first_name", "last_name", "email")

    def __unicode__(self):
        return u"%2s %2s" % (self.first_name, self.last_name)

    def filled_result(self):
        return Result.objects.get(participant=self.id)


class ParticipantFuture(models.Model):
    first_name = models.CharField("Имя", max_length=64)
    last_name = models.CharField("Фамилия", max_length=64)
    email = models.EmailField("Email")
    company_name = models.CharField("Компания", max_length=128, blank=True, null=True)
    position = models.CharField("Должность", max_length=64, blank=True, null=True)
    event = models.ForeignKey(Event)

    class Meta:
        verbose_name = 'Заявка'
        verbose_name_plural = 'Заявки на будущее'
        unique_together = ("first_name", "last_name", "email")

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

    def __unicode__(self):
        return u"%s (%s)" % (self.name, self.email)


class Result(models.Model):
    participant = models.ForeignKey('Participant', unique=True)
    email = models.EmailField('Email', null=True, blank=True)
    company_size = models.CharField('Размер организации', max_length=3,
        choices=(
            ('1', '1-10'), ('2', '11-50'), ('3', '51-200'), ('4', '201-500'), ('5', 'более 500')
        ), null=True, blank=True)
    position = models.CharField('Должность', max_length=3,
        choices=(
            ('1', u'UX/юзабилити специалист'),
            ('2', u'Дизайнер'),
            ('3', u'Руководитель проекта/группы'),
            ('4', u'Директор/владелец бизнеса'),
            ('5', u'Тестировщик/специалист по качеству'),
            ('6', u'Аналитик'),
            ('7', u'Программист'),
            ('8', u'Маркетолог'),
            ('9', u'Студент')
        ), null=True, blank=True)
    position_custom = models.CharField('Другое', max_length=32, null=True, blank=True)
    site = models.CharField('Адрес сайта', max_length=64, null=True, blank=True)
    conf_rate_1 = models.CharField('Уровень конференции в целом', max_length=2, null=True, blank=True)
    conf_rate_2 = models.CharField('Количество новой полезной информации', max_length=2, null=True, blank=True)
    conf_rate_3 = models.CharField('Качество организации', max_length=2, null=True, blank=True)
    conf_rate_4 = models.CharField('Уровень докладов', max_length=2, null=True, blank=True)
    resume_1 = models.TextField('Общее впечатление', null=True, blank=True)
    resume_2 = models.TextField('Можно улучшить', null=True, blank=True)
    is_public = models.BooleanField("Согласен на публикацию на сайте", default=False)
    allow_partners = models.BooleanField("Разрешаю передачу партнёрам", default=False)

    class Meta:
        verbose_name = 'Итоги конференции'
        verbose_name_plural = 'Итоги конференции'

    def __unicode__(self):
        return u"%s" % self.participant


class AddressBook(models.Model):
    participant = models.ForeignKey('Result')
    moikrug = models.CharField('Мой круг', max_length=64, null=True, blank=True)
    twitter = models.CharField('Твиттер', max_length=64, null=True, blank=True)
    fb = models.CharField('Facebook', max_length=64, null=True, blank=True)
    vk = models.CharField('ВКонтакте', max_length=64, null=True, blank=True)
    habr = models.CharField('Хабр', max_length=64, null=True, blank=True)
    site = models.CharField('Личный сайт', max_length=64, null=True, blank=True)

    know_design = models.BooleanField('Проектировать интерфейсы', blank=True)
    know_research = models.BooleanField('Исследовать пользователей', blank=True)
    know_testing = models.BooleanField('Юзабилти-тестирование', blank=True)

    work_pm = models.BooleanField('Веду проекты', blank=True)
    work_programmer = models.BooleanField('Программирую', blank=True)
    work_clientside = models.BooleanField('Верстаю', blank=True)
    work_manager = models.BooleanField('Рулю командой', blank=True)
    work_director = models.BooleanField('Управляю бизнесом', blank=True)
    work_sale = models.BooleanField('Продаю', blank=True)
    work_tester = models.BooleanField('Тестирую', blank=True)
    work_teacher = models.BooleanField('Преподаю', blank=True)
    work_writer = models.BooleanField('Пишу тексты', blank=True)
    work_student = models.BooleanField('Учусь (студент)', blank=True)
    work_designer = models.BooleanField('Рисую картинки', blank=True)

    no_book = models.BooleanField('Не включать в адресную книгу', blank=True)
    no_group = models.BooleanField('Не добавлять в UX.SPb', blank=True)
    no_invite = models.BooleanField('Не приглашать на следующую конференцию', blank=True)

    def __unicode__(self):
        return u"%s" % self.participant


class LectureRate(models.Model):
    participant = models.ForeignKey('Result')
    lecture = models.ForeignKey('Lecture')
    theme_rate = models.CharField('Тема доклада', max_length=2, null=True, blank=True)
    total_rate = models.CharField('Общее впечатление', max_length=2, null=True, blank=True)
    favorite = models.BooleanField("Понравился", default=False)
