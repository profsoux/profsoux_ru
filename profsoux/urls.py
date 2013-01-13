from django.conf.urls.defaults import patterns, include, url
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.conf.urls.static import static
from django.conf import settings

# from filebrowser.sites import site

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

from conference.views import Papers

urlpatterns = patterns('',

    url(r'^grappelli/', include('grappelli.urls')),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^login/$', 'django.contrib.auth.views.login', {'template_name': 'login.html'}),

    url(r'^media/(?P<path>.*)', 'django.views.static.serve', {'document_root': settings.MEDIA_ROOT}),

    url(r'^$', 'conference.views.index'),
    url(r'^people/$', 'conference.views.people'),
    url(r'^people/export/$', 'conference.views.people_to_xls'),
    url(r'^schedule/ical/$', 'conference.views.ical'),
    url(r'^speakers/$', 'conference.views.speakers'),
    url(r'^speakers/(?P<speaker_id>[0-9]+)/$', 'conference.views.speaker'),
    url(r'^papers/$', Papers.as_view()),
    url(r'^papers/(?P<paper_id>[0-9]+)/$', 'conference.views.paper'),
    url(r'^schedule/$', 'conference.views.schedule'),
    url(r'^schedule/ical.ics$', 'conference.views.ical2'),
    url(r'^schedule/pdf/$', 'conference.views.pdf'),
    url(r'^registration/$', 'conference.views.registration'),
    url(r'^registration/future/$', 'conference.views.registration_future'),
    url(r'^registration/confirm/$', 'conference.views.confirm'),
    url(r'^contacts/$', 'conference.views.contacts'),
    url(r'^partners/$', 'conference.views.partners'),
    url(r'^organizers/$', 'conference.views.organizers'),
    url(r'^map/$', 'conference.views.map'),
    url(r'^twitter/$', 'conference.views.twitter'),
    url(r'^results/$', 'conference.views.results'),
    url(r'^results/export/((?P<depht>all)/)?$', 'conference.views.results_to_xls'),
)

urlpatterns += staticfiles_urlpatterns()
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
