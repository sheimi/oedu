from django.contrib.auth.models import User
from django.db import models

# Create your models here.

class Announcement(models.Model):
    publisher = models.ForeignKey(User)
    title = models.CharField(max_length=40)
    content = models.TextField(max_length=400)
    grade = models.IntegerField()
    publish_time = models.DateTimeField()
    user = models.ManyToManyField(User, through="AnnouncementReceiver", related_name="anno_received")
    
    def __unicode__(self):
        return self.title
    
    def statistics(self):
        anno_res = self.announcementreceiver_set.all()
        all = len(anno_res)
        read = 0
        for ar in anno_res:
            if ar.isRead:
                read += 1
        return {'read' : read, 'total' : all}
    
    def get_unread_users(self):
        anno_res = self.announcementreceiver_set.filter(isRead=False)
        render = [re.user for re in anno_res]
        return render
    
class AnnouncementReply(models.Model):
    publisher = models.ForeignKey(User)
    content = models.TextField(max_length=140)
    announcement = models.ForeignKey(Announcement)
    publish_time = models.DateTimeField()
    
    def __unicode__(self):
        return 'Re: ' + self.announcement.title
    
class AnnouncementReceiver(models.Model):
    announcement = models.ForeignKey(Announcement)
    user = models.ForeignKey(User)
    isRead = models.BooleanField()
    publish_time = models.DateTimeField()
    
    def __unicode__(self):
        return self.announcement.title