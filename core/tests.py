"""
This file demonstrates writing tests using the unittest module. These will pass
when you run "manage.py test".

Replace this with more appropriate tests for your application.
"""

from Oedu.core.models import Tag, UserGroup
from django.contrib.auth.models import User
from django.test import TestCase
from django.test.client import Client
from django.utils import unittest
import json

class CoreTestWithoutLogin(unittest.TestCase):
    def setUp(self):
        self.client = Client()
        
    def test_signin(self):
        pass
    
    def test_signout(self):
        pass
    
    def test_home(self):
        pass
    
    def test_index(self):
        pass

class CoreTestAfterLogin(unittest.TestCase):
    def setUp(self):
        self.client = Client()
        a = self.client.login(username="oops", password="oops")
        
    def test_signin(self):
        pass
    
    def test_signout(self):
        pass
    
    def test_home(self):
        pass
    
    def test_index(self):
        pass

class UserCRUDTest(unittest.TestCase):
    def setUp(self):
        self.client = Client()
        a = self.client.login(username="oops", password="oops")
     
    def test_user_detail_c(self):
        
        response = self.client.get("/core/crud/1")
        r = json.loads(response.content)[0]
        self.assertEqual("oops", r["username"])
        
        
        post = {'name' : "sheimi"}
        response = self.client.post("/core/crud/2", json.dumps(post), "text")
        u = User.objects.get(pk=2)
        self.assertEqual(response.content, '"success"')
        self.assertEqual(u.get_profile().name, "sheimi")
        
        
class TagCRUDTest(unittest.TestCase):
    def setUp(self):
        self.client = Client()
        a = self.client.login(username="oops", password="oops")
        
    def test_get_tag_list(self):
        pass
        
    def test_tag_detail_c(self):
        put = { 'description'       :   "test",
               }
        response = self.client.put("/core/tag/crud/", json.dumps(put), "text")
        tag = Tag.objects.filter(description="test")
        self.assertEqual(1, len(tag))
        
        post = {'operation' : "add", 'users' : [1, 2]}
        response = self.client.post("/core/tag/crud/%d" % tag[0].pk, json.dumps(post), "text")
        tag = Tag.objects.filter(description="test")
        self.assertEqual(response.content, '"success"')
        self.assertEqual(tag[0].users.all()[0].username, "oops")
        
        post = {'operation' : "update", 'users' : [2, 3]}
        response = self.client.post("/core/tag/crud/%d" % tag[0].pk, json.dumps(post), "text")
        tag = Tag.objects.filter(description="test")
        self.assertEqual(response.content, '"success"')
        self.assertEqual(tag[0].users.all()[0].username, "zrz")
        
        post = {'operation' : "delete", 'users' : [2, 3]}
        response = self.client.post("/core/tag/crud/%d" % tag[0].pk, json.dumps(post), "text")
        tag = Tag.objects.filter(description="test")
        self.assertEqual(response.content, '"success"')
        self.assertEqual(len(tag[0].users.all()), 0)
        
        
        response = self.client.get("/core/tag/crud/%d" % tag[0].pk)
        r = json.loads(response.content)[0]
        self.assertEqual("test", r["fields"]["description"])
        
        response = self.client.delete("/core/tag/crud/%d" % tag[0].pk)
        tag = Tag.objects.filter(description="test")
        self.assertEqual(response.content, '"success"')
        self.assertEqual(0, len(tag))
        
class UserGroupCRUDTest(unittest.TestCase):
    def setUp(self):
        self.client = Client()
        a = self.client.login(username="oops", password="oops")
        
    def test_usergroup_detail_c(self):
        put = { 'description'       :   "test",
               }
        response = self.client.put("/core/usergroup/crud/", json.dumps(put), "text")
        ug = UserGroup.objects.filter(description="test")
        self.assertEqual(1, len(ug))
        
        post = {'operation' : "add", 'users' : [1, 2]}
        response = self.client.post("/core/usergroup/crud/%d" % ug[0].pk, json.dumps(post), "text")
        ug = UserGroup.objects.filter(description="test")
        self.assertEqual(response.content, '"success"')
        self.assertEqual(ug[0].users.all()[0].username, "oops")
        
        post = {'operation' : "update", 'users' : [2, 3]}
        response = self.client.post("/core/usergroup/crud/%d" % ug[0].pk, json.dumps(post), "text")
        ug = UserGroup.objects.filter(description="test")
        self.assertEqual(response.content, '"success"')
        self.assertEqual(ug[0].users.all()[0].pk, 2)
        
        post = {'operation' : "delete", 'users' : [2, 3]}
        response = self.client.post("/core/usergroup/crud/%d" % ug[0].pk, json.dumps(post), "text")
        ug = UserGroup.objects.filter(description="test")
        self.assertEqual(response.content, '"success"')
        self.assertEqual(len(ug[0].users.all()), 0)
        
        response = self.client.get("/core/usergroup/crud/%d" % ug[0].pk)
        r = json.loads(response.content)[0]
        self.assertEqual("test", r["fields"]["description"])
        
        response = self.client.delete("/core/usergroup/crud/%d" % ug[0].pk)
        ug = UserGroup.objects.filter(description="test")
        self.assertEqual(response.content, '"success"')
        self.assertEqual(0, len(ug))