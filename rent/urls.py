'''
Created on Apr 17, 2011

@author: sheimi
'''
from Oedu.rent.views import rent_detail
from django.conf.urls.defaults import *

urlpatterns = patterns('Oedu.rent.views',
    (r'^$','index'),
    (r'^popup/?$', 'popup'),
    (r'^crud/?$', rent_detail()),
    (r'^crud/(?P<rent_id>\d+)/?$', rent_detail()),
    (r'^teacher/?$', 'get_rent_by_teacher'),
    (r'^teacher/(?P<teacher_id>\d+)/?$', 'get_rent_by_teacher'),
)