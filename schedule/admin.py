'''
Created on Apr 17, 2011

@author: sheimi
'''

from Oedu.schedule.models import Schedule
from django.contrib import admin

# Re-register UserAdmin
admin.site.register(Schedule)