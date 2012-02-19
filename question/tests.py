"""
This file demonstrates writing tests using the unittest module. These will pass
when you run "manage.py test".

Replace this with more appropriate tests for your application.
"""

from Oedu.question.models import Question, Answer
from django.test import TestCase
from django.test.client import Client
import json
import unittest

class QuestionCRUDTest(unittest.TestCase):
    def setUp(self):
        self.client = Client()
        self.client.login(username="oops", password="oops")
        
    def test_index(self):
        pass
        
    def test_question_detail(self):
        put = { 'title'     :   "test",
                'content'   :   "test",
                'receiver'     :  1,
               }
        
        response = self.client.put("/qa/crud/", json.dumps(put), "text")
        question = Question.objects.filter(title="test")[0]
        self.assertEqual(question.content, "test")
        
        post = {'content' : "test2"}
        response = self.client.post("/qa/crud/%d" % question.pk, json.dumps(post), "text")
        question = Question.objects.filter(title="test")[0]
        self.assertEqual(response.content, '"success"')
        self.assertEqual(question.content, "test2")
        
        response = self.client.get("/qa/crud/%d" % question.pk)
        f = json.loads(response.content)[0]
        self.assertEqual("test", f["fields"]["title"])
        
        response = self.client.delete("/qa/crud/%d" % question.pk)
        questions = Question.objects.filter(title="test")
        self.assertEqual(response.content, '"success"')
        self.assertEqual(0, len(questions))
        
 
class AnswerCRUDTest(unittest.TestCase):
    def setUp(self):
        self.client = Client()
        self.client.login(username="oops", password="oops")
        
    def test_answer_detail(self):
        put = { 'content'       :   "test",
                'question_id'  :   1,
               }
        
        response = self.client.put("/qa/answer/crud/", json.dumps(put), "text")
        answer = Answer.objects.filter(content="test")
        self.assertEqual(1, len(answer))
   
        post = {'content' : "test2"}
        response = self.client.post("/qa/answer/crud/%d" % answer[0].pk, json.dumps(post), "text")
        answer = Answer.objects.filter(content="test2")
        self.assertEqual(response.content, '"success"')
        self.assertEqual(answer[0].content, "test2")
       
        response = self.client.get("/qa/answer/crud/%d" % answer[0].pk)
        a = json.loads(response.content)[0]
        self.assertEqual("test2", a["fields"]["content"])
     
        response = self.client.delete("/qa/answer/crud/%d" % answer[0].pk)
        questions = Answer.objects.filter(content="test2")
        self.assertEqual(response.content, '"success"')
        self.assertEqual(0, len(questions))   