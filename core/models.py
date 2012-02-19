from django.contrib.auth.models import User
from django.db import models

# Create your models here.

def group_names(self):
    groupnames = [group.name for group in self.groups.all()]
    return groupnames

User.groupnames = group_names        

class UserProfile(models.Model):
    name = models.CharField(max_length=15)
    nju_id = models.CharField(max_length=10)
    grade = models.IntegerField()
    address = models.CharField(max_length=40, null=True, blank=True)
    mobile = models.CharField(max_length=11, null=True, blank=True)
    qq = models.CharField(max_length=15, null=True, blank=True)
    msn = models.CharField(max_length=40, null=True, blank=True)
    research_field = models.CharField(max_length=50, null=True, blank=True)
    interested_in = models.TextField(max_length=300, null=True, blank=True)
    description = models.TextField(max_length=300, null=True, blank=True)
    location = models.CharField(max_length=10, null=True, blank=True)
    user = models.ForeignKey(User, unique=True)
    img = models.URLField(null=True, blank=True)
    
    def __unicode__(self):
        return self.user.username

class Tag(models.Model):
    description = models.CharField(max_length=40)
    users = models.ManyToManyField(User)
    
    def __unicode__(self):
        return self.description
    
class UserGroup(models.Model):
    description = models.CharField(max_length=40)
    owner = models.ForeignKey(User, related_name='groups_set')
    users = models.ManyToManyField(User, related_name='group_belong')
    
    def __unicode__(self):
        return self.description
    
class Paper(models.Model):
    title = models.CharField(max_length=40)
    description = models.TextField(max_length=300, null=True, blank=True)
    url = models.URLField(null=True, blank=True)
    users = models.ManyToManyField(User)
    
    def __unicode__(self):
        return self.title    