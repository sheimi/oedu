'''
Created on Apr 17, 2011

@author: sheimi
'''
from Oedu.mail.views import mail_detail
from django.conf.urls.defaults import *

urlpatterns = patterns('Oedu.mail.views',
    (r'^$','index'),
    (r'^popup/?$', 'popup'),
    (r'^popup/(?P<mail_id>\d+)/(?P<receiver_id>\d+)/?$', 'popup'),
    (r'^crud/?$', mail_detail()),
    (r'^crud/(?P<mail_id>\d+)/?$', mail_detail()),
    (r'^send/mul/?$', 'send_mail_mul'),
)