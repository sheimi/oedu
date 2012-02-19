'''
Created on Apr 17, 2011

@author: sheimi
'''
from Oedu.message.views import message_detail
from django.conf.urls.defaults import *

urlpatterns = patterns('Oedu.message.views',
    (r'^crud/?$', message_detail()),
    (r'^crud/(?P<message_id>\d+)/?$', message_detail()),
)