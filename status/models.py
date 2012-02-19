from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Status(models.Model):
    publisher = models.ForeignKey(User)
    content = models.CharField(max_length=140)
    publish_time = models.DateTimeField()
    
    def __unicode__(self):
        return self.publisher.username + " says " + self.content
    
class StatusReply(models.Model):
    publisher = models.ForeignKey(User)
    content = models.CharField(max_length=140)
    publish_time = models.DateTimeField()
    status = models.ForeignKey(Status)
    
    def __unicode__(self):
        return self.publisher.username + " replies " + self.content 
    