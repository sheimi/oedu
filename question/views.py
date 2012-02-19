# Create your views here.

from Oedu.im.views import IMChannel
from Oedu.question.models import Question, Answer
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.core import serializers
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, render_to_response
import datetime
import json

@login_required
def index(request):
    '''
    url:      /qa/
    '''
    return render_to_response("qa/index.html")

@login_required
def popup(request):
    '''
    url:    /qa/popup
    @return: a popup page to set up a question
    '''
    return render_to_response("qa/popup.html")

@login_required
def answer_popup(request):
    '''
    url:    /qa/answer/popup
    @return: a popup page to set up a answer
    '''
    return render_to_response("qa/answer_popup.html")

@login_required
def get_question_list(request, teacher_id=0):
    '''
    url:    /qa/question_list/{teacher_id}
    @retuan: a list of questions
    '''
    if teacher_id == 0:
        u = request.user
    else:
        u = get_object_or_404(User, pk=teacher_id)
    q_list = u.question_receive.all()
    return HttpResponse(serializers.serialize("json", q_list), mimetype="application/json")

 
@login_required
def index_answer(request):
    '''
    url:      /qa/answer/
    @return: the partial page to set up an answer
    '''
    return render_to_response("qa/answer.html")

def answer_list(request, question_id):
    '''
    usrl:    /qa/answerlist/{question_id}
    @return: a list of answers
    '''
    q = get_object_or_404(Question, pk=question_id)
    answers = q.answer_set.all()
    return HttpResponse(serializers.serialize("json", answers), mimetype="application/json")
  
class question_detail:
    '''
    url:    /qa/crud/{qestion_id}
    restful interface of a certain question
    '''
    
    def __call__(self, request, question_id=0):
        self.request, self.user, self.build_absolute_uri, self.get_full_path = \
            request, request.user, request.build_absolute_uri, request.get_full_path
        self.question_id = question_id
        try:
            callback = getattr(self, "do_%s" % request.method)
        except AttributeError:
            pass
        return callback()
    
    @login_required  
    def do_GET(self):
        '''
        http method: GET
        @return: a dictionary of a certain question
            type:    json
            list of a dic:    
            sample:   [{
                        "pk": 1, 
                        "model": "question.question", 
                        "fields": {
                            "publisher": 2, 
                            "publish_time": "2011-04-28 14:38:16", 
                            "title": "tit", 
                            "content": "tet", 
                            "isRead": false, 
                            "receiver": 1
                        }
                    }]
        '''
        q = get_object_or_404(Question, pk=self.question_id)
        return HttpResponse(serializers.serialize("json", [q]), mimetype="application/json")
    
    @login_required
    def do_POST(self):
        '''
        http method: POST
        to update a certain question
        type:    json
        @param title:    title of the question (optional)
        @param content:  content of the question (optional)
        @param isRead:  isRead of the question (optional)
        @return: success or failed(a dictionary)
        '''
        q = get_object_or_404(Question, pk=self.question_id)
        post = json.loads(self.request.raw_post_data)
        try:
            q.title = post.has_key("title") and post["title"] or q.title
            q.content = post.has_key("content") and post["content"] or q.content
            q.isRead = post.has_key("isRead") and post["isRead"] or q.isRead
            q .save()
        except:
            return HttpResponse("failed", mimetype="application/json")
        return HttpResponse(json.dumps("success"), mimetype="application/json")
    
    @login_required  
    def do_PUT(self):
        '''
        http method: PUT
        to create a certain question
        type:    json
        @param title:    title of the question
        @param content:  content of the question
        @param receiver:  the id of receiver of the question
        @return: q.pk or failed(a dictionary)
        '''
        put = json.loads(self.request.raw_post_data)
        try:
            q = self.request.user.question_publish.create(title=put["title"],
                                        content=put["content"],
                                        isRead=False,
                                        receiver=User.objects.get(pk=put["receiver"]),
                                        publish_time=datetime.datetime.now()
                                        )
        except:
            return HttpResponse("failed", mimetype="application/json")
        return HttpResponse(json.dumps(q.pk), mimetype="application/json")
    
    @login_required  
    def do_DELETE(self):
        '''
        http method: DELETE
        to delete a certain question
        @return: success or failed(a dictionary)
        '''
        q = get_object_or_404(Question, pk=self.question_id)
        try:
            q.delete()
        except:
            return HttpResponse("failed", mimetype="application/json")
        return HttpResponse(json.dumps("success"), mimetype="application/json")
  


class answer_detail:
    '''
    url:    /qa/answer/crud/{answer_id}
    restful interface of a certain answer
    '''
    
    def __call__(self, request, answer_id=0):
        self.request, self.user, self.build_absolute_uri, self.get_full_path = \
            request, request.user, request.build_absolute_uri, request.get_full_path
        self.answer_id = answer_id
        try:
            callback = getattr(self, "do_%s" % request.method)
        except AttributeError:
            pass
        return callback()
    
    @login_required  
    def do_GET(self):
        '''
        http method: GET
        @return: a dictionary of a certain answer
            type:    json
            list of a dic:    
            sample:   [{
                        "pk": 1, 
                        "model": "question.answer", 
                        "fields": {
                            "content": "title", 
                            "publisher": 2, 
                            "publish_time": "2011-04-28 14:38:36", 
                            "question": 1
                        }
                    }]
        '''
        a = get_object_or_404(Answer, pk=self.answer_id)
        return HttpResponse(serializers.serialize("json", [a]), mimetype="application/json")
    
    @login_required
    def do_POST(self):
        '''
        http method: POST
        to update a certain answer
        type:    json
        @param content:  content of the answer (optional)
        @return: success or failed(a dictionary)
        '''
        a = get_object_or_404(Answer, pk=self.answer_id)
        post = json.loads(self.request.raw_post_data)
        try:
            a.content = post.has_key("content") and post["content"] or a.content
            a.save()
        except:
            return HttpResponse("failed", mimetype="application/json")
        return HttpResponse(json.dumps("success"), mimetype="application/json")
    
    @login_required  
    def do_PUT(self):
        '''
        http method: PUT
        to create a certain answer
        type:    json
        @param content:  content of the answer
        @param question_id:  the id of question
        @return: a.pk or failed(a dictionary)
        '''
        put = json.loads(self.request.raw_post_data)
        try:
            a = self.request.user.answer_set.create(
                                        question=get_object_or_404(Question, pk=put["question_id"]),
                                        content=put["content"],
                                        publish_time=datetime.datetime.now(),
                                        )
        except:
            return HttpResponse("failed", mimetype="application/json")
        return HttpResponse(json.dumps(a.pk), mimetype="application/json")
    
    @login_required  
    def do_DELETE(self):
        '''
        http method: DELETE
        to delete a certain answer
        @return: success or failed(a dictionary)
        '''
        q = get_object_or_404(Answer, pk=self.answer_id)
        try:
            q.delete()
        except:
            return HttpResponse("failed", mimetype="application/json")
        return HttpResponse(json.dumps("success"), mimetype="application/json")
