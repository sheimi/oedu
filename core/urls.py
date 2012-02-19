'''
Created on Apr 17, 2011

@author: sheimi
'''
from Oedu.core.views import user_detail, tag_detail, usergroup_detail
from django.conf.urls.defaults import *

urlpatterns = patterns('Oedu.core.views',
    (r'^profile/?$', 'profile'),
    (r'^profile/(?P<user_id>\d+)/?$', 'profile'),
    (r'^signin/?$', 'signin'),
    (r'^signout/?$', 'signout'),

    (r'^crud/?$', user_detail()),
    (r'^crud/(?P<user_id>\d+)/?$', user_detail()),

    (r'^tag/crud/?$', tag_detail()),
    (r'^tag/crud/(?P<tag_id>\d+)/?$', tag_detail()),
    (r'^taglist/all/?$', 'get_tag_list_all'),
    (r'^taglist/user/(?P<user_id>\d+)/?$', 'get_tag_list_user'),
    (r'^taglist/user/?$', 'get_tag_list_user'),

    (r'^usergroup/crud/?$', usergroup_detail()),
    (r'^usergroup/crud/(?P<usergroup_id>\d+)/?$', usergroup_detail()),
    (r'^usergroup/popup/?$', 'usergroup_popup'),
    (r'^usergroup/popup/(?P<usergroup_id>\d+)/?$', 'manage_user_group'),
    (r'^usergroup/popup/new/?$', 'new_user_group'),
    
    (r'^upload_image/?$', 'upload_image'),
    (r'^index/?$','index'),
    (r'^$','index'),
    
    (r'^init/?$', 'upload'),
)

urlpatterns += patterns('Oedu.core.test_upload',
    (r'^test$', 'upload_image_test'),
    (r'^test_upload$', 'upload_drop_test'),
)
