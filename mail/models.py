from django.contrib.auth.models import User
from django.db import models

# Create your models here.

class Mail(models.Model):
    from_user = models.ForeignKey(User, related_name="mail_sent")
    to_user = models.ForeignKey(User, related_name="mail_received")
    title = models.CharField(max_length=40)
    message = models.TextField()
    sent_time = models.DateTimeField()
    is_read = models.BooleanField()
    
    def __unicode__(self):
        return self.title