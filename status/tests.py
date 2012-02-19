"""
This file demonstrates writing tests using the unittest module. These will pass
when you run "manage.py test".

Replace this with more appropriate tests for your application.
"""

from Oedu.status.models import Status, StatusReply
from django.test import TestCase
from django.test.client import Client
import json
import unittest

class statusCRUDTest(unittest.TestCase):
    def setUp(self):
        self.client = Client()
        self.client.login(username="oops", password="oops")
        
    def test_status_detail(self):
        put = { 'content'   :   "test",
               }

        response = self.client.put("/status/crud/", json.dumps(put), "text")
        status = Status.objects.filter(content="test")[0]
        self.assertEqual(status.content, "test")
     
        post = {'content' : "test2"}
        response = self.client.post("/status/crud/%d" % status.pk, json.dumps(post), "text")
        status = Status.objects.filter(content="test2")[0]
        self.assertEqual(response.content, '"success"')
        self.assertEqual(status.content, "test2")    
     
        response = self.client.get("/status/crud/%d" % status.pk)
        s = json.loads(response.content)[0]
        self.assertEqual("test2", s["fields"]["content"])
     
        response = self.client.delete("/status/crud/%d" % status.pk)
        status = Status.objects.filter(content="test2")
        self.assertEqual(response.content, '"success"')
        self.assertEqual(0, len(status))


class replyCRUDTest(unittest.TestCase):
    def setUp(self):
        self.client = Client()
        self.client.login(username="oops", password="oops")
        
    def test_reply_detail(self):
        put = { 'content'   :   "test",
                'status'    :   1,
               }

        response = self.client.put("/status/reply/crud/", json.dumps(put), "text")
        reply = StatusReply.objects.filter(content="test")[0]
        self.assertEqual(reply.content, "test")
        
        post = {'content' : "test2"}
        response = self.client.post("/status/reply/crud/%d" % reply.pk, json.dumps(post), "text")
        reply = StatusReply.objects.filter(content="test2")[0]
        self.assertEqual(response.content, '"success"')
        self.assertEqual(reply.content, "test2")
        
        response = self.client.get("/status/reply/crud/%d" % reply.pk)
        r = json.loads(response.content)[0]
        self.assertEqual("test2", r["fields"]["content"])
        
        response = self.client.delete("/status/reply/crud/%d" % reply.pk)
        reply = StatusReply.objects.filter(content="test2")
        self.assertEqual(response.content, '"success"')
        self.assertEqual(0, len(reply))