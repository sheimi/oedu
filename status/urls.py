'''
Created on Apr 17, 2011

@author: sheimi
'''
from Oedu.status.views import status_detail, reply_detail
from django.conf.urls.defaults import *

urlpatterns = patterns('Oedu.status.views',
    (r'^$','index'),
    (r'^reply/crud/?$', reply_detail()),
    (r'^reply/crud/(?P<reply_id>\d+)/?$', reply_detail()),
    (r'^crud/?$', status_detail()),
    (r'^crud/(?P<status_id>\d+)/?$', status_detail()),
    
    (r'^statuslist/?$', 'get_status_list'),
    (r'^statuslist/(?P<user_id>\d+)/?$', 'get_status_list'),
    (r'^statuslist/all/?$', 'get_status_list_all'),
    (r'^statuslist/special/?$', 'get_status_of_special_groups'),
    (r'^replylist/(?P<status_id>\d+)/?$', 'get_reply_list'),
)
