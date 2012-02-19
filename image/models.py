from Oedu.core.models import UserGroup
from django.contrib.auth.models import User
from django.db import models

# Create your models here.

class ImageInfo(models.Model):
    owner = models.ForeignKey(User)
    path = models.CharField(max_length=40, null=True, blank=True)
    upload_time = models.DateTimeField()
    share_to = models.ManyToManyField(UserGroup, null=True, blank=True)
    active = models.BooleanField()
    title = models.CharField(max_length=40, null=True, blank=True)
    description = models.TextField(max_length=400, null=True, blank=True)
    
    def __unicode__(self):
        return self.path