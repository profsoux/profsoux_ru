# Create your views here.

from django.shortcuts import render_to_response
from django.core.context_processors import csrf
from django.views.generic import ListView

from conference.models import *
from conference.forms import ParticipantForm


class Papers(ListView):
    model = Lecture
    context_object_name = 'papers'
    template_name = 'papers.html'


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


def speaker(request, speaker_id):
    speaker = Speaker.objects.get(id=speaker_id).person
    try:
        lectures = Lecture.objects.filter(speaker=speaker.id)
    except:
        pass
    else:
        speaker.lectures = lectures
    return render_to_response('speaker.html', {'speaker': speaker})


def schedule(request):
    items = ScheduleSection.objects.order_by('start_time')
    print items
    return render_to_response('schedule.html', {'items': items})


def paper(request, paper_id):
    paper = Lecture.objects.get(id=paper_id)
    return render_to_response('paper.html', {'paper': paper})


def registration(request):
    if request.method == 'POST':
        form = ParticipantForm(request.POST)
        if form.is_valid():
            form.save()
            c = {
                'state': 'thanks'
                }
        else:
            c = {
            'state': 'default',
            'form': form
            }
    else:
        form = ParticipantForm()
        c = {
            'state': 'default',
            'form': form
            }
    c.update(csrf(request))
    return render_to_response('registration.html', c)
