'''
Created on Apr 17, 2011

@author: sheimi
'''
from django.conf.urls.defaults import *
from Oedu.anno.views import *

urlpatterns = patterns('Oedu.anno.views',
    (r'^$','index'),
    (r'^popup/?', 'popup'),
    (r'^(?P<anno_id>\d+)/read/?', 'read_anno'),
    (r'^reply/?$', 'index_reply'),
    (r'^reply/popup/?', 'reply_popup'),
    (r'^crud/?$', announcement_detail()),
    (r'^crud/(?P<anno_id>\d+)/?$', announcement_detail()),
    (r'^reply/crud/?$', reply_detail()),
    (r'^reply/crud/(?P<reply_id>\d+)/?$', reply_detail()),
    (r'^replylist/anno/(?P<anno_id>\d+)/?$', 'get_reply_list'),
    (r'^annolist/?$', 'get_anno_list'),
    (r'^annolist/(?P<user_id>\d+)/?$', 'get_anno_list'),
    (r'^pub_anno/?$', 'pub_anno'),
)