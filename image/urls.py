'''
Created on Apr 17, 2011

@author: sheimi
'''
from Oedu.mail.views import mail_detail
from django.conf.urls.defaults import *

urlpatterns = patterns('Oedu.image.views',
    (r'^(?P<user_id>\d+)/?$','index'),
    (r'^$','index'),
    (r'^upload/?$', 'upload'),
    (r'^delete/(?P<image_id>\d+)/?$', 'delete'),
    (r'^active_all/?$', 'active_all'),
    (r'^share/(?P<image_id>\d+)/json?$', 'set_share_json'),
    (r'^share/(?P<image_id>\d+)/popup?$', 'set_share_popup'),
)