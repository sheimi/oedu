'''
Created on Apr 17, 2011

@author: sheimi
'''
from Oedu.feedback.views import feedback_detail
from django.conf.urls.defaults import *

urlpatterns = patterns('Oedu.feedback.views',
    (r'^$','index'),
    (r'^popup/?', 'popup'),
    (r'^crud/?$', feedback_detail()),
    (r'^crud/(?P<feedback_id>\d+)/?$', feedback_detail()),
    (r'^feedback_list/(?P<teacher_id>\d+)/?$', 'get_feedback_list'),
    (r'^feedback_list/?$', 'get_feedback_list'),
)