'''
Created on Apr 17, 2011

@author: sheimi
'''
from Oedu.share.views import share_detail
from django.conf.urls.defaults import *

urlpatterns = patterns('Oedu.share.views',
    (r'^$','index'),
    (r'^crud/?$', share_detail()),
    (r'^crud/(?P<share_id>\d+)/?$', share_detail()),
    
    (r'^share_list/?$', 'get_share_list'),
    (r'^share_list/(?P<user_id>\d+)/?$', 'get_share_list'),
    (r'^share_list/all/?$', 'get_share_list_all'),
    (r'^share_list/user/?$', 'get_share_list_by_user'),
    
    (r'^set_share_to/(?P<share_id>\d+)/?$', 'set_share_to'),
    
    (r'^sharelist/special/?$', 'get_share_of_special_groups'),
    
    (r'^upload/?$', 'upload'),
    
    
    (r'^status/(?P<status_id>\d+)/?$', 'share_status'),
    (r'^link/?$', 'share_link'),
    (r'^pre/(?P<share_id>\d+)/?$', 'share_pre'),
    (r'^downloads/(?P<share_id>\d+)/?', 'download')
)