'''
Created on Apr 17, 2011

@author: sheimi
'''
from django.conf.urls.defaults import *

urlpatterns = patterns('Oedu.search.views',
    (r'^/?$', 'index'),
    (r'^general/?$', 'search_general'),
    (r'^tag/?$', 'search_tag'),
    (r'^user/?$', 'search_user'),
    (r'^user_info/?$', 'search_user_info'),
    (r'^user/tag/(?P<tag_id>\d+)/?$', 'get_users_by_tag'),
    (r'^user/all/?$', 'search_user_all'),
    (r'^usergroup/?$', 'search_usergroup'),
)