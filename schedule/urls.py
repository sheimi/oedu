'''
Created on Apr 17, 2011

@author: sheimi
'''
from Oedu.schedule.views import schedule_detail
from django.conf.urls.defaults import *

urlpatterns = patterns('Oedu.schedule.views',
    (r'^$','index'),
    (r'^crud/?$', schedule_detail()),
    (r'^crud/(?P<schedule_id>\d+)/?$', schedule_detail()),
    
    (r'^schedule_list/(?P<teacher_id>\d+)/?$', 'get_schedule_list'),
    (r'^schedule_list/?$', 'get_schedule_list'),
)