from django.db import models
from django.contrib.auth.models import User
# Create your models here.

class Feedback(models.Model):
    publisher = models.ForeignKey(User, related_name='feedback_publish')
    receiver = models.ForeignKey(User, related_name='feedback_receive')
    title = models.CharField(max_length=40)
    content = models.TextField(max_length=400)
    isRead = models.BooleanField()
    publish_time = models.DateTimeField()
    
    def __unicode__(self):
        return self.title