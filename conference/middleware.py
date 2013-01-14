# coding = utf-8

from django.db.models import Q
from conference.models import Event

class SiteMiddleware():
    def process_request(self, request):
        request.domain = Event.objects.get(Q(domain=request.META['HTTP_HOST']) | Q(default=True))
