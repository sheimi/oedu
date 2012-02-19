"""
This file demonstrates writing tests using the unittest module. These will pass
when you run "manage.py test".

Replace this with more appropriate tests for your application.
"""

from Oedu.message.models import Message
from django.test import TestCase
from django.test.client import Client
import json
import unittest

class MessageCRUDTest(unittest.TestCase):
    def setUp(self):
        self.client = Client()
        a = self.client.login(username="oops", password="oops")
        
    def test_get_message_list(self):
        pass
        
    def test_message_detail(self):
        put = { 'message'   :   "test",
                'to_user'  :   1,
               }
        
        response = self.client.put("/message/crud/", json.dumps(put), "text")
        self.assertEqual(response.content, '1')
        message = Message.objects.filter(message="test")[0]
        self.assertEqual(message.to_user.pk, 1)
        
        post = {'message' : "test2"}
        response = self.client.post("/message/crud/%d" % message.pk, json.dumps(post), "text")
        message = Message.objects.filter(message="test2")[0]
        self.assertEqual(response.content, '"success"')
        self.assertEqual(message.message, "test2")
        
        
        response = self.client.get("/message/crud/%d" % message.pk)
        f = json.loads(response.content)[0]
        self.assertEqual("test2", f["fields"]["message"])
        
        response = self.client.delete("/message/crud/%d" % message.pk)
        message = Message.objects.filter(pk=message.pk)
        self.assertEqual(response.content, '"success"')
        self.assertEqual(0, len(message))
        