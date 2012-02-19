from Oedu.core.models import UserGroup
from django.contrib.auth.models import User
from django.db import models
# Create your models here.

class Share(models.Model):
    comment = models.TextField(max_length=140)
    publish_time = models.DateTimeField()
    share_to = models.ManyToManyField(UserGroup)
    url = models.CharField(max_length=80)
    publisher = models.ForeignKey(User)
    type = models.CharField(max_length=340)
    
    def __unicode__(self):
        return self.url
    