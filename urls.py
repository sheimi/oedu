from django.conf.urls.defaults import patterns, include, url
from django.contrib import admin

# Uncomment the next two lines to enable the admin:
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'Oedu.views.home', name='home'),
    # url(r'^Oedu/', include('Oedu.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    #url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
    
    (r'^core/', include('core.urls')),
    (r'^im/', include('im.urls')),
    (r'^im2/', include('im.urls2')),
    (r'^mail/', include('mail.urls')),
    (r'^qa/', include('question.urls')),
    (r'^anno/', include('anno.urls')),
    (r'^feedback/', include('feedback.urls')),
    (r'^status/', include('status.urls')),
    (r'^share/', include('share.urls')),
    (r'^schedule/', include('schedule.urls')),
    (r'^rent/', include('rent.urls')),
    (r'^search/', include('search.urls')),
    (r'^score/', include('score.urls')),
    (r'^message/', include('message.urls')),
    (r'^image/', include('image.urls')),
    (r'^upload/?', 'Oedu.share.views.upload'),
    
    (r'^signin', 'Oedu.core.views.signin'),
    (r'^signout', 'Oedu.core.views.signout'),
    
    (r'^favicon\.ico$', 'django.views.generic.simple.redirect_to', {'url': '/static/images/favicon.ico'}),
    
    (r'^404', 'Oedu.core.error.oops404'),
    (r'^profile/?$', 'Oedu.core.views.profile'),
    (r'^profile/(?P<user_id>\d+)', 'Oedu.core.views.profile'),
    (r'^$', 'Oedu.core.views.index'),
)
#handler error
from django.conf.urls.defaults import *
handler404 = 'Oedu.core.error.oops404'
