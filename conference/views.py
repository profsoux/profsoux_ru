# Create your views here.

from django.shortcuts import render_to_response

from conference.models import *


def index(request):
    return render_to_response('index.html', {})


def speakers(request):
    speakers = list(Speaker.objects.all())
    for speaker in speakers:
        speaker.lectures = []
        try:
            lectures = Lecture.objects.filter(speaker=speaker.id)
            print lectures
        except:
            pass
        else:
            speaker.lectures = lectures
    return render_to_response('speakers.html', {'speakers': speakers})
