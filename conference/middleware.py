# coding = utf-8

from conference.models import Event


class EventMiddleware():
    def process_request(self, request):
        request.event = Event.objects.get_current_event(request)
