'''
Created on Apr 17, 2011

@author: sheimi
'''
from django.conf.urls.defaults import *

urlpatterns = patterns('Oedu.im.views2',
    (r'^update/?$', 'update'),
    (r'^new_session/?$', 'new_session'),
    (r'^new_message/?$', 'new_im'),
    (r'^add_user/?$', 'add_user'),
    (r'^quit/?$', 'quit'),
    (r'^online_user/?$', 'online_list')
)