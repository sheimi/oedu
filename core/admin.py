'''
Created on Apr 17, 2011

@author: sheimi
'''
from Oedu.core.models import UserProfile, UserGroup, Tag
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User

# Define an inline admin descriptor for UserProfile model
class UserProfileInline(admin.TabularInline):
    model = UserProfile
    fk_name = 'user'
    max_num = 1

# Define a new UserAdmin class
class MyUserAdmin(UserAdmin):
    inlines = [UserProfileInline, ]

# Re-register UserAdmin
admin.site.unregister(User)
admin.site.register(User, MyUserAdmin)
admin.site.register(Tag)
admin.site.register(UserGroup)