# coding = utf-8

from django.db.models import Q
from conference.models import Event
from django.core.exceptions import ObjectDoesNotExist, MultipleObjectsReturned


class EventMiddleware():
    def process_request(self, request):
        try:
            request.event = Event.objects.get(Q(domain=request.META['HTTP_HOST']) | Q(default=True))
        except ObjectDoesNotExist:
            request.event = Event.objects.all()[0]
        except MultipleObjectsReturned:
            request.event = Event.objects.all()[0]
