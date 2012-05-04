from django.conf.urls.defaults import patterns, include, url
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.conf.urls.static import static
from django.conf import settings

from conference.views import Papers

# from filebrowser.sites import site

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'uxspb_site.views.home', name='home'),
    # url(r'^uxspb_site/', include('uxspb_site.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^grappelli/', include('grappelli.urls')),
#    url(r'^admin/filebrowser/', include(site.urls)),
    #url(r'^admin/filebrowser/', include('filebrowser.urls')),
    url(r'^admin/', include(admin.site.urls)),

    url(r'^media/(?P<path>.*)', 'django.views.static.serve', {'document_root': settings.MEDIA_ROOT}),

    url(r'^$', 'conference.views.index'),
    url(r'^people/$', 'conference.views.people'),
    url(r'^people/export/$', 'conference.views.people_to_xls'),
    url(r'^schedule/ical/$', 'conference.views.ical'),
    url(r'^speakers/$', 'conference.views.speakers'),
    url(r'^speakers/(?P<speaker_id>[0-9]+)/$', 'conference.views.speaker'),
    url(r'^papers/(?P<paper_id>[0-9]+)/$', 'conference.views.paper'),
    url(r'^schedule/$', 'conference.views.schedule'),
    url(r'^schedule/ical/$', 'conference.views.ical'),
    url(r'^registration/$', 'conference.views.registration'),
    url(r'^contacts/$', 'conference.views.contacts'),
    url(r'^partners/$', 'conference.views.partners'),
    url(r'^organizers/$', 'conference.views.organizers'),
    url(r'^map/$', 'conference.views.map'),
)

urlpatterns += staticfiles_urlpatterns()
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
