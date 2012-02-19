'''
Created on Apr 17, 2011

@author: sheimi
'''

from Oedu.score.models import Score, Course
from django.contrib import admin

# Re-register UserAdmin
admin.site.register(Score)
admin.site.register(Course)