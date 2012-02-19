'''
Created on Apr 17, 2011

@author: sheimi
'''

from Oedu.anno.models import Announcement, AnnouncementReply, \
    AnnouncementReceiver
from django.contrib import admin

# Re-register UserAdmin
admin.site.register(Announcement)
admin.site.register(AnnouncementReply)
admin.site.register(AnnouncementReceiver)