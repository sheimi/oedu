'''
Created on Apr 17, 2011

@author: sheimi
'''

from Oedu.rent.models import Application
from django.contrib import admin
# Re-register UserAdmin
admin.site.register(Application)