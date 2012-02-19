from django.db import models
from django.contrib.auth.models import User
# Create your models here.

class Application(models.Model):
    applicants = models.ForeignKey(User, related_name="applications_own")
    title = models.CharField(max_length=40)
    content = models.TextField(max_length=1000)
    datetime = models.DateTimeField()
    to_teacher = models.ForeignKey(User, related_name="applications_to")
    is_approved = models.BooleanField()
    is_processed = models.BooleanField()