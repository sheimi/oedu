'''
Created on Apr 17, 2011

@author: sheimi
'''
from Oedu.image.models import ImageInfo
from Oedu.mail.models import Mail
from django.contrib import admin

# Re-register UserAdmin
admin.site.register(ImageInfo)