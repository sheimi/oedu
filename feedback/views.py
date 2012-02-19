# Create your views here.
from Oedu.feedback.models import Feedback
from Oedu.im.views import IMChannel
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
    url:      /feedback/
    '''
    return render_to_response("feedback/index.html")

@login_required
def popup(request):
    '''
    url:    /feedback/popup/
    @return: a popup page to set up a feedback
    '''
    return render_to_response("feedback/popup.html")
    
@login_required
def get_feedback_list(request, teacher_id=0):
    '''
    url:    /feedback/feedbacklist/{teacher_id}
    @return: a list of feedbacks
    '''
    if teacher_id == 0:
        u = request.user
    else:
        u = get_object_or_404(User, pk=teacher_id)
    f_list = u.feedback_receive.all().order_by('-publish_time')
    return HttpResponse(serializers.serialize("json", f_list), mimetype="application/json")

class feedback_detail:
    '''
    url:    /feedback/crud/{feedback_id}
    restful interface of a certain feedback
    '''
    
    def __call__(self, request, feedback_id = 0):
        self.request, self.user, self.build_absolute_uri, self.get_full_path = \
            request, request.user, request.build_absolute_uri, request.get_full_path
        self.feedback_id = feedback_id
        try:
            callback = getattr(self, "do_%s" % request.method)
        except AttributeError:
            pass
        return callback()
    
    @login_required  
    def do_GET(self):
        '''
        http method: GET
        @return: a dictionary of a certain feedback 
            type:    json
            list of a dic:    
            sample:   [{
                        "pk": 1, 
                        "model": "feedback.feedback", 
                        "fields": {
                            "publisher": 2, 
                            "publish_time": "2011-04-28 14:04:01", 
                            "title": "hello", 
                            "content": "hello", 
                            "isRead": true, 
                            "receiver": 1
                        }
                    }]
        '''
        f = get_object_or_404(Feedback, pk=self.feedback_id)
        return HttpResponse(serializers.serialize("json", [f]), mimetype="application/json")
    
    @login_required
    def do_POST(self):
        '''
        http method: POST
        to update a certain feedback
        type:    json
        @param title:    title of the feedback (optional)
        @param content:  content of the feedback (optional)
        @param isRead:  mark the feedback read or not (optional)
        @return: success or failed(a dictionary)
        '''
        f = get_object_or_404(Feedback, pk=self.feedback_id)
        post = json.loads(self.request.raw_post_data)
        try:
            f.title = post.has_key("title") and post["title"] or f.title
            f.content = post.has_key("content") and post["content"] or f.content
            f.isRead = post.has_key("isRead") and post["isRead"] or f.isRead
            f.save()
        except:
            return HttpResponse("failed", mimetype="application/json")
        return HttpResponse(json.dumps("success"), mimetype="application/json")
    
    
    @login_required  
    def do_PUT(self):
        '''
        http method: PUT
        to create a certain feedback
        type:    json
        @param title:    title of the feedback
        @param content:  content of the feedback
        @param receiver: the id of the receiver of the feedback
        @return: feedback.pk or failed(a dictionary)
        '''
        put = json.loads(self.request.raw_post_data)
        try:
            f = self.request.user.feedback_publish.create(title=put["title"],
                                                     content=put["content"],
                                                     isRead=False,
                                                     receiver=User.objects.get(pk=put["receiver"]),
                                                     publish_time=datetime.datetime.now()
                                                )
        except:
            return HttpResponse("failed", mimetype="application/json")
        return HttpResponse(json.dumps(f.pk), mimetype="application/json")
    
    @login_required  
    def do_DELETE(self):
        '''
        http method: DELETE
        to delete a certain feedback
        @return: success or failed(a dictionary)
        '''
        f = get_object_or_404(Feedback, pk=self.feedback_id)
        try:
            f.delete()
        except:
            return HttpResponse("failed", mimetype="application/json")
        return HttpResponse(json.dumps("success"), mimetype="application/json")