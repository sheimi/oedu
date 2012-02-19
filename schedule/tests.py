"""
This file demonstrates writing tests using the unittest module. These will pass
when you run "manage.py test".

Replace this with more appropriate tests for your application.
"""

from Oedu.schedule.models import Schedule
from django.test import TestCase
from django.test.client import Client
import json
import unittest

class scheduleCRUDTest(unittest.TestCase):
    def setUp(self):
        self.client = Client()
        self.client.login(username="oops", password="oops")
        
    def test_rent_detail(self):
        put = { 'content'   :   "test",
                'starttime' : '2009-1-1',
                'endtime': '2010-1-1',
               }
        
        response = self.client.put("/schedule/crud/", json.dumps(put), "text")
        schedule = Schedule.objects.get(pk=int(response.content))
        self.assertEqual(schedule.content, "test")
        
        post = {'content' : "test2"}
        response = self.client.post("/schedule/crud/%d" % schedule.pk, json.dumps(post), "text")
        schedule = Schedule.objects.get(pk=schedule.pk)
        self.assertEqual(response.content, '"success"')
        self.assertEqual(schedule.content, "test2")
        
        
        response = self.client.get("/schedule/crud/%d" % schedule.pk)
        a = json.loads(response.content)[0]
        self.assertEqual("test2", a["fields"]["content"])
        
        i = schedule.pk
        response = self.client.delete("/schedule/crud/%d" % i)
        rents = Schedule.objects.filter(pk=i)
        self.assertEqual(response.content, '"success"')
        self.assertEqual(0, len(rents))