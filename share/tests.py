"""
This file demonstrates writing tests using the unittest module. These will pass
when you run "manage.py test".

Replace this with more appropriate tests for your application.
"""

from Oedu import share
from Oedu.share.models import Share
from django.test import TestCase
from django.test.client import Client
import json
import unittest

class shareCRUDTest(unittest.TestCase):
    def setUp(self):
        self.client = Client()
        self.client.login(username="oops", password="oops")
        
    def test_share_detail(self):
        put = { 'comment'   :   "test",
                'url'       :   "/status/crud/1",
                'type'      :   "status"
               }

        response = self.client.put("/share/crud/", json.dumps(put), "text")
        share = Share.objects.filter(comment="test")[0]
        self.assertEqual(share.url, "/status/crud/1")
        
        post = {'comment' : "test2"}
        response = self.client.post("/share/crud/%d" % share.pk, json.dumps(post), "text")
        share = Share.objects.filter(url="/status/crud/1")[0]
        self.assertEqual(response.content, '"success"')
        self.assertEqual(share.comment, "test2")    
        
        response = self.client.get("/share/crud/%d" % share.pk)
        s = json.loads(response.content)[0]
        self.assertEqual("test2", s["fields"]["comment"])
        
        response = self.client.delete("/share/crud/%d" % share.pk)
        share = Share.objects.filter(comment="test2")
        self.assertEqual(response.content, '"success"')
        self.assertEqual(0, len(share))
        