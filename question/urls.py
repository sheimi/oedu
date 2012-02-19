'''
Created on Apr 17, 2011

@author: sheimi
'''
from Oedu.question.views import answer_detail, question_detail
from django.conf.urls.defaults import *

urlpatterns = patterns('Oedu.question.views',
    (r'^/?$','index'),
    (r'^answer/?$', 'index_answer'),
    (r'^popup/?$', 'popup'),
    (r'^answer/popup/?$', 'answer_popup'),
    (r'^answer/crud/?$', answer_detail()),
    (r'^answer/crud/(?P<answer_id>\d+)/?$', answer_detail()),
    (r'^crud/?$', question_detail()),
    (r'^crud/(?P<question_id>\d+)/?$', question_detail()),
    
    (r'^question_list/?$', 'get_question_list'),
    (r'^question_list/(?P<teacher_id>\d+)/?$', 'get_question_list'),
    (r'^answer_list/(?P<question_id>\d+)/?$', 'answer_list'),
)