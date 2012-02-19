"""
This file demonstrates writing tests using the unittest module. These will pass
when you run "manage.py test".

Replace this with more appropriate tests for your application.
"""

from Oedu.rent.models import Application
from django.test import TestCase
from django.test.client import Client
import json
import unittest

class rentCRUDTest(unittest.TestCase):
    def setUp(self):
        self.client = Client()
        self.client.login(username="oops", password="oops")
        
    def test_rent_detail(self):
        put = { 'title'     :   "test",
                'content'   :   "test",
                'to_teacher':   1,
               }
 
        response = self.client.put("/rent/crud/", json.dumps(put), "text")
        rent = Application.objects.filter(title="test")[0]
        self.assertEqual(rent.content, "test")
        
        post = {'content' : "test2"}
        response = self.client.post("/rent/crud/%d" % rent.pk, json.dumps(post), "text")
        rent = Application.objects.filter(title="test")[0]
        self.assertEqual(response.content, '"success"')
        self.assertEqual(rent.content, "test2")
        
        
        response = self.client.get("/rent/crud/%d" % rent.pk)
        a = json.loads(response.content)[0]
        self.assertEqual("test", a["fields"]["title"])
        
        response = self.client.delete("/rent/crud/%d" % rent.pk)
        rents = Application.objects.filter(title="test")
        self.assertEqual(response.content, '"success"')
        self.assertEqual(0, len(rents))