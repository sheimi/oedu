"""
This file demonstrates writing tests using the unittest module. These will pass
when you run "manage.py test".

Replace this with more appropriate tests for your application.
"""

from Oedu.score.models import *
from django.test import TestCase
from django.test.client import Client
import json
import unittest

class CourseCRUDTest(unittest.TestCase):
    def setUp(self):
        self.client = Client()
        self.client.login(username="oops", password="oops")
        
    def test_course_detail(self):
        put = { 'name'   :   "test",
                'description': 'test',
                'grade' : 2009,
                'grade_point': 5,
               }
        
        response = self.client.put("/score/course/crud/", json.dumps(put), "text")
        self.assertEqual(response.content, '1')
        course = Course.objects.get(pk=1)
        self.assertEqual(course.description, "test")
        
        post = {'name' : "test2"}
        response = self.client.post("/score/course/crud/%d" % course.pk, json.dumps(post), "text")
        self.assertEqual(response.content, '"success"')
        course = Course.objects.filter(name="test2")[0]
        self.assertEqual(course.description, "test")    
        
        response = self.client.get("/score/course/crud/%d" % course.pk)
        s = json.loads(response.content)[0]
        self.assertEqual("test2", s["fields"]["name"])
        
        response = self.client.delete("/score/course/crud/%d" % course.pk)
        course = Course.objects.filter(name="test2")
        self.assertEqual(response.content, '"success"')
        self.assertEqual(0, len(course))


class ScoreCRUDTest(unittest.TestCase):
    def setUp(self):
        self.client = Client()
        self.client.login(username="oops", password="oops")
        
    def test_score_detail(self):
        put = { 'name'   :   "test",
                'description': 'test',
                'grade' : 2009,
                'grade_point': 5,
               }
        response = self.client.put("/score/course/crud/", json.dumps(put), "text")
        self.assertEqual(response.content, '1')
        course = Course.objects.get(pk=1)
        self.assertEqual(course.description, "test")
        
        put = { 'score'   :   9,
                'course': 1,
                'user': 1,
               }
        
        response = self.client.put("/score/crud/", json.dumps(put), "text")
        self.assertEqual(response.content, '1')
        score = Score.objects.get(pk=1)
        self.assertEqual(score.score, 9)
        
        post = {'score' : 10}
        response = self.client.post("/score/crud/%d" % score.pk, json.dumps(post), "text")
        self.assertEqual(response.content, '"success"')
        score = Score.objects.get(pk=score.pk)
        self.assertEqual(score.score, 10)    
        
        response = self.client.get("/score/crud/%d" % score.pk)
        s = json.loads(response.content)[0]
        self.assertEqual(10, s["fields"]["score"])
        
        response = self.client.delete("/score/crud/%d" % score.pk)
        s = Score.objects.all()
        self.assertEqual(response.content, '"success"')
        self.assertEqual(0, len(s))
        