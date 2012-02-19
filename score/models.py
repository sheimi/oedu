#the ScoreEncoder to be filled
from django.db import models
from django.contrib.auth.models import User
   
class Course(models.Model):
    name = models.CharField(max_length=40)
    description = models.TextField(max_length=400)
    grade_point = models.IntegerField()
    grade = models.IntegerField()
    user = models.ManyToManyField(User, through="Score")
    
    def __unicode__(self):
        return self.name
    
class Score(models.Model):
    score = models.IntegerField()
    course = models.ForeignKey(Course)
    student = models.ForeignKey(User)
    
    def __unicode__(self):
        return self.student.username + "'s score in " + self.course.name
    
class UserGPA(models.Model):
    user = models.OneToOneField(User)
    gpa = models.DecimalField(max_digits=4, decimal_places=3)
    
def cal_gpa(self):
    try:
        gpa = self.usergpa
    except:
        gpa = None
    if not gpa:
        gpa = UserGPA.objects.create(user=self, gpa=0)
    scores = self.score_set.all()
    grade = 0
    grade_point = 0
    for score in scores:
        grade += score.score * score.course.grade_point
        grade_point += score.course.grade_point
    if grade_point:
        gpa.gpa = grade * 1.0 / grade_point / 20
    gpa.save()
    return gpa.gpa

User.cal_gpa = cal_gpa
  