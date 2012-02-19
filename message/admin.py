'''
Created on Apr 17, 2011

@author: sheimi
'''
from Oedu.message.models import Message
from django.contrib import admin

# Re-register UserAdmin
admin.site.register(Message)