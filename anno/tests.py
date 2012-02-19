"""
This file demonstrates writing tests using the unittest module. These will pass
when you run "manage.py test".

Replace this with more appropriate tests for your application.
"""

from Oedu.anno.models import Announcement, AnnouncementReply
from django.core import serializers
from django.shortcuts import get_object_or_404
from django.test import TestCase
from django.test.client import Client
import json
import unittest

class AnnouncementCRUDTest(unittest.TestCase):
    def setUp(self):
        self.client = Client()
        self.client.login(username="oops", password="oops")
        
    def test_index(self):
        pass
        
    def test_anno_detail(self):
        put = { 'title'     :   "test",
                'content'   :   "test",
                'grade'     :   2011,
               }
        
        response = self.client.put("/anno/crud/", json.dumps(put), "text")
        self.assertEqual(response.content, "2")
        anno = Announcement.objects.filter(title="test")[0]
        self.assertEqual(anno.content, "test")
        
        post = {'content' : "test2"}
        response = self.client.post("/anno/crud/%d" % anno.pk, json.dumps(post), "text")
        anno = Announcement.objects.filter(title="test")[0]
        self.assertEqual(response.content, '"success"')
        self.assertEqual(anno.content, "test2")
        
        response = self.client.get("/anno/crud/%d" % anno.pk)
        a = json.loads(response.content)[0]
        self.assertEqual("test", a["fields"]["title"])
        
        response = self.client.delete("/anno/crud/%d" % anno.pk)
        annos = Announcement.objects.filter(title="test")
        self.assertEqual(response.content, '"success"')
        self.assertEqual(0, len(annos))
        
    
class ReplyCRUDTest(unittest.TestCase):
    def setUp(self):
        self.client = Client()
        self.client.login(username="oops", password="oops")
        
    def test_get_reply_list(self):
        response = self.client.get("/anno/replylist/anno/1/")
        self.assertEqual(200, response.status_code)
        anno = Announcement.objects.get(pk=1)
        render = anno.announcementreply_set.all()
        self.assertEqual(serializers.serialize("json", render), response.content)
        
    def test_index_reply(self):
        pass
    
    def test_reply_detail(self):
        put = { 'content'       :   "test",
                'announcement'  :   1,
               }
        
        response = self.client.put("/anno/reply/crud/", json.dumps(put), "text")
        self.assertEqual(response.content, "2")
        reply = AnnouncementReply.objects.filter(content="test")
        self.assertEqual(1, len(reply))
        
        post = {'content' : "test2"}
        response = self.client.post("/anno/reply/crud/%d" % reply[0].pk, json.dumps(post), "text")
        reply = AnnouncementReply.objects.filter(content="test2")
        self.assertEqual(response.content, '"success"')
        self.assertEqual(reply[0].content, "test2")
        
        response = self.client.get("/anno/reply/crud/%d" % reply[0].pk)
        r = json.loads(response.content)[0]
        self.assertEqual("test2", r["fields"]["content"])
        
        response = self.client.delete("/anno/reply/crud/%d" % reply[0].pk)
        annos = Announcement.objects.filter(content="test2")
        self.assertEqual(response.content, '"success"')
        self.assertEqual(0, len(annos))
        
    