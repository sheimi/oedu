'''
Created on Apr 17, 2011

@author: sheimi
'''

from Oedu.feedback.models import Feedback
from django.contrib import admin

# Re-register UserAdmin
admin.site.register(Feedback)