from django.contrib.auth.models import User
from django.db import models

# Create your models here.

class Message(models.Model):
    from_user = models.ForeignKey(User, related_name="message_sent")
    to_user = models.ForeignKey(User, related_name="message_received")
    message = models.TextField()
    sent_time = models.DateTimeField()
    is_read = models.BooleanField()
    
    def __unicode__(self):
        return self.message