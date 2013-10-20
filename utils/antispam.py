# coding=utf-8

from akismet import Akismet, AkismetError
from django.core.mail import send_mail
from profsoux.settings import AKISMET_KEY, ADMINS

akismet = Akismet(AKISMET_KEY)


def check_spam(comment, request):
    data = {
        'user_ip': request.META['REMOTE_ADDR'],
        'user_agent': request.META['HTTP_USER_AGENT'],
    }
    try:
        return akismet.comment_check(comment.encode('ascii', 'ignore'), data=data)
    except AkismetError, e:
        subject = '[profsoux]: Akismet Error'
        message = e.message
        sender = 'robot@profsoux.ru'
        send_mail(subject, message, sender, ADMINS)
        return False
