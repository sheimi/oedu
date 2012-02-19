from django.db import models
from django.contrib.auth.models import User
# Create your models here.

class Schedule(models.Model):
    teacher = models.ForeignKey(User)
    starttime = models.DateTimeField()
    endtime = models.DateTimeField()
    content = models.CharField(max_length=40)
    
    def __unicode__(self):
        return self.teacher.username + "  " + self.content
    