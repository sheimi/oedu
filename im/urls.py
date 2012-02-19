'''
Created on Apr 17, 2011

@author: sheimi
'''
from django.conf.urls.defaults import *

urlpatterns = patterns('Oedu.im.views',
    (r'^test/?$', 'test'),
    (r'^update/?$', 'update'),
    (r'^newmessage/?$', 'new_im'),
    (r'^newmessage/tag/?$', 'new_im_by_tag'),
    (r'^online_user/?$', 'online_list')
)