'''
Created on Apr 17, 2011

@author: sheimi
'''

from Oedu.share.models import Share
from django.contrib import admin

# Re-register UserAdmin
admin.site.register(Share)