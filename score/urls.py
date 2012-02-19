'''
Created on Apr 17, 2011

@author: sheimi
'''
from Oedu.score.views import score_detail, course_detail
from django.conf.urls.defaults import *

urlpatterns = patterns('Oedu.score.views',
    (r'^/?$', 'index'),
    (r'^manager/?$', 'score_manager'),
    (r'^crud/?$', score_detail()),
    (r'^crud/(?P<score_id>\d+)/?$', score_detail()),
    
    (r'^course/(?P<course_id>\d+)/?$', 'get_course_score'),
    (r'^course/(?P<course_id>\d+)/scores/?$', 'get_course_score_json'),
    (r'^course/crud/?$', course_detail()),
    (r'^course/crud/(?P<course_id>\d+)/?$', course_detail()),
    
    (r'user/(?P<user_id>\d+)/scores/?$', 'get_user_score_json'),
    (r'user/(?P<user_id>\d+)/?$', 'get_user_score'),
    (r'user/(?P<user_id>\d+)/courses/?$', 'get_user_course'),
    (r'user/scores/?$', 'get_user_score'),
    (r'user/courses/?$', 'get_user_course'),
    
    (r'course_list/all/?$', 'get_course_list'),
    
    (r'upload_xlrd/?$', 'upload_score')
)