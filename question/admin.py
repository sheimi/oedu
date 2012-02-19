'''
Created on Apr 17, 2011

@author: sheimi
'''
from Oedu.question.models import Question, Answer
from django.contrib import admin

# Re-register UserAdmin
admin.site.register(Question)
admin.site.register(Answer)