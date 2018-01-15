from django.conf.urls import patterns, include, url
from django.conf.urls.static import static
from django.conf import settings
from django.contrib import admin
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

from xrp.userprofile.forms import UserProfileForm
from xrp.userprofile.views import index, registration

admin.autodiscover()

urlpatterns = patterns('',
    url(r'^admin/', include(admin.site.urls)),

    url(r'^accounts/register/$', registration, {'template_name': 'registration/registration_form.html'}, name='registration_register'),

    url(r'^accounts/', include('registration.backends.simple.urls')),

    url(r'^comments/', include('django.contrib.comments.urls')),

    url( r'^$', index, { 'template_name': 'index.html' }, name = 'index' ),

    url(r'^accounts/', include('xrp.account.urls')),

    url(r'^profile/', include('xrp.userprofile.urls')),

    url(r'^course/', include('xrp.course.urls')),

    url(r'^faucet/', include('xrp.faucet.urls')),

    url(r'^quiz/', include('xrp.quiz.urls')),

    url(r'^tracking/', include('tracking.urls')),

    url(r'^django-session-idle-timeout/', include('django-session-idle-timeout.urls')),
)

urlpatterns += staticfiles_urlpatterns()

urlpatterns += patterns('',
    url(r'^media/(?P<path>.*)$', 'django.views.static.serve',
        {'document_root': settings.MEDIA_ROOT, 'show_indexes': True}),

    url(r'^adminmedia/(?P<path>.*)$', 'django.views.static.serve',
        {'document_root': settings.STATIC_ROOT + '/admin', 'show_indexes': True}),
)

handler404 = 'xrp.account.views.handler404'
handler500 = 'xrp.account.views.handler500'
