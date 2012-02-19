"""
This file demonstrates writing tests using the unittest module. These will pass
when you run "manage.py test".

Replace this with more appropriate tests for your application.
"""

from Oedu.feedback.models import Feedback
from django.test import TestCase
from django.test.client import Client
import json
import unittest

class FeedbackCRUDTest(unittest.TestCase):
    def setUp(self):
        self.client = Client()
        a = self.client.login(username="oops", password="oops")
        
    def test_get_feedback_list(self):
        pass
        
    def test_feedback_detail(self):
        put = { 'title'     :   "test",
                'content'   :   "test",
                'receiver'  :   1,
               }
        
        response = self.client.put("/feedback/crud/", json.dumps(put), "text")
        feedback = Feedback.objects.filter(title="test")[0]
        self.assertEqual(feedback.content, "test")
        
        post = {'content' : "test2"}
        response = self.client.post("/feedback/crud/%d" % feedback.pk, json.dumps(post), "text")
        feedback = Feedback.objects.filter(title="test")[0]
        self.assertEqual(response.content, '"success"')
        self.assertEqual(feedback.content, "test2")
        
        
        response = self.client.get("/feedback/crud/%d" % feedback.pk)
        f = json.loads(response.content)[0]
        self.assertEqual("test", f["fields"]["title"])
        
        response = self.client.delete("/feedback/crud/%d" % feedback.pk)
        feedback = Feedback.objects.filter(title="test")
        self.assertEqual(response.content, '"success"')
        self.assertEqual(0, len(feedback))