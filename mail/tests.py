"""
This file demonstrates writing tests using the unittest module. These will pass
when you run "manage.py test".

Replace this with more appropriate tests for your application.
"""

from Oedu.mail.models import Mail
from django.test import TestCase
from django.test.client import Client
import json
import unittest

class MailCRUDTest(unittest.TestCase):
    def setUp(self):
        self.client = Client()
        a = self.client.login(username="oops", password="oops")
        
    def test_get_mail_list(self):
        pass
        
    def test_mail_detail(self):
        put = { 'title'     :   "testt",
                'message'   :   "test",
                'to_user'  :   1,
               }
        
        response = self.client.put("/mail/crud/", json.dumps(put), "text")
        mail = Mail.objects.filter(title="testt")[0]
        self.assertEqual(mail.message, "test")
        
        post = {'message' : "test2"}
        response = self.client.post("/mail/crud/%d" % mail.pk, json.dumps(post), "text")
        mail = Mail.objects.filter(title="testt")[0]
        self.assertEqual(response.content, '"success"')
        self.assertEqual(mail.message, "test2")
        
        
        response = self.client.get("/mail/crud/%d" % mail.pk)
        f = json.loads(response.content)[0]
        self.assertEqual("testt", f["fields"]["title"])
        
        response = self.client.delete("/mail/crud/%d" % mail.pk)
        mail = Mail.objects.filter(title="testt")
        self.assertEqual(response.content, '"success"')
        self.assertEqual(0, len(mail))