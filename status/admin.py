'''
Created on Apr 17, 2011

@author: sheimi
'''

from Oedu.status.models import Status, StatusReply
from django.contrib import admin
# Re-register UserAdmin
admin.site.register(Status)
admin.site.register(StatusReply)