# Create your views here.

from Oedu.im.views import IMChannel
from Oedu.status.models import Status, StatusReply
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User, Group
from django.core import serializers
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
import datetime
import json

@login_required
def index(request):
    '''
    url:      /status/
    '''
    return HttpResponse("this is the index page")


@login_required
def get_status_list(request, user_id=0):
    '''
    url:    /status/statuslist/{user_id}
    http method: GET
    '''
    if user_id == 0:
        u = request.user
    else:
        u = get_object_or_404(User, pk=user_id)
    s = u.status_set.all().order_by('-publish_time')[:50]
    return HttpResponse(serializers.serialize("json", s), mimetype="application/json")

@login_required
def get_status_list_all(request):
    '''
    url:    /status/statuslist/all
    http method: GET
    '''
    s = Status.objects.all().order_by('-publish_time')
    if len(s) > 50:
        s = s[:50]
    return HttpResponse(serializers.serialize("json", s), mimetype="application/json")

@login_required
def get_reply_list(request, status_id):
    '''
    url:    /status/replylist/{status_id}
    http method: GET
    '''
    status = get_object_or_404(Status, pk=status_id)
    r = status.statusreply_set.all().order_by('-publish_time')
    return HttpResponse(serializers.serialize("json", r), mimetype="application/json")

@login_required
def get_status_of_special_groups(request):
    '''
    url:    /status/statuslist/special
    http method: GET
    '''
    status = Status.objects.filter(publisher__groups__id=6).order_by('-publish_time')
    return HttpResponse(serializers.serialize("json", status), mimetype="application/json")

    

class status_detail:
    '''
    url:    /status/crud/{status_id}
    restful interface of a certain status
    '''
    
    def __call__(self, request, status_id = 0):
        self.request, self.user, self.build_absolute_uri, self.get_full_path = \
            request, request.user, request.build_absolute_uri, request.get_full_path
        self.status_id = status_id
        try:
            callback = getattr(self, "do_%s" % request.method)
        except AttributeError:
            pass
        return callback()
    
    @login_required  
    def do_GET(self):
        '''
        http method: GET
        @return: a dictionary of a certain status 
            type:    json
            list of a dic:    
            sample:   [{
                        "pk": 1, 
                        "model": "status.status", 
                        "fields": {
                            "content": "hello world", 
                            "publisher": 1, 
                            "publish_time": "2011-04-27 17:17:26"
                        }
                    }]
        '''
        s = get_object_or_404(Status, pk=self.status_id)
        return HttpResponse(serializers.serialize("json", [s]), mimetype="application/json")
    
    @login_required
    def do_POST(self):
        '''
        http method: POST
        to update a certain status
        type:    json
        @param content:  content of the status (optional)
        @return: success or failed(a dictionary)
        '''
        s = get_object_or_404(Status, pk=self.status_id)
        post = json.loads(self.request.raw_post_data)
        try:
            s.content = post.has_key("content") and post["content"] or s.content
            s.save()
        except:
            return HttpResponse("failed", mimetype="application/json")
        return HttpResponse(json.dumps("success"), mimetype="application/json")
    
    @login_required  
    def do_PUT(self):
        '''
        http method: PUT
        to create a certain status
        type:    json
        @param content:  content of the status
        @return: s.pk or failed(a dictionary)
        '''
        put = json.loads(self.request.raw_post_data)
        try:
            status = self.user.status_set.create(content=put["content"],
                                        publish_time=datetime.datetime.now())
        except:
            return HttpResponse("failed", mimetype="application/json")
        return HttpResponse(json.dumps(status.pk), mimetype="application/json")
    
    @login_required  
    def do_DELETE(self):
        '''
        http method: DELETE
        to delete a certain status
        @return: success or failed(a dictionary)
        '''
        s = get_object_or_404(Status, pk=self.status_id)
        try:
            s.delete()
        except:
            return HttpResponse("failed", mimetype="application/json")
        return HttpResponse(json.dumps("success"), mimetype="application/json")
    
@login_required
def index_reply(request):
    '''
    url:      /reply/
    @return: the partial page to set up an reply
    '''
    return HttpResponse("this is the index page")

class reply_detail:
    '''
    url:    /reply/crud/{status_id}
    restful interface of a certain reply
    '''
    
    def __call__(self, request, reply_id = 0):
        self.request, self.user, self.build_absolute_uri, self.get_full_path = \
            request, request.user, request.build_absolute_uri, request.get_full_path
        self.reply_id = reply_id
        try:
            callback = getattr(self, "do_%s" % request.method)
        except AttributeError:
            pass
        return callback()
    
    @login_required  
    def do_GET(self):
        '''
        http method: GET
        @return: a dictionary of a certain reply 
            type:    json
            list of a dic:     
            sample:    [{
                            "pk": 1,
                            "model": "status.statusreply", 
                            "fields": {
                                "content": "hello", 
                                "publisher": 2, 
                                "publish_time": "2011-04-27 17:18:12", 
                                "status": 1
                            }
                        }]
        '''
        r = get_object_or_404(StatusReply, pk=self.reply_id)
        return HttpResponse(serializers.serialize("json", [r]), mimetype="application/json")
    
    @login_required
    def do_POST(self):
        '''
        http method: POST
        to update a certain reply
        type:    json
        @param content: the content of a reply (optional)
        @return: success or failed(a dictionary)
        '''
        r = get_object_or_404(StatusReply, pk=self.reply_id)
        post = json.loads(self.request.raw_post_data)
        try:
            r.content = post.has_key("content") and post["content"] or r.content
            r.save()
        except:
            return HttpResponse("failed", mimetype="application/json")
        return HttpResponse(json.dumps("success"), mimetype="application/json")
    
    
    @login_required  
    def do_PUT(self):
        '''
        http method: PUT
        to create a certain reply
        type:    json
        @param content: the content of a reply
        @param status: the id of the status
        @return: r.pk or failed(a dictionary)
        '''
        put = json.loads(self.request.raw_post_data)
        try:
            status = get_object_or_404(Status, pk=put["status"])
            r = status.statusreply_set.create(content=put["content"],
                                   publisher=self.user,
                                   publish_time=datetime.datetime.now())
        except:
            return HttpResponse("failed", mimetype="application/json")
        return HttpResponse(json.dumps(r.pk), mimetype="application/json")
    
    @login_required  
    def do_DELETE(self):
        '''
        http method: DELETE
        to delete a certain reply
        @return: success or failed(a dictionary)
        '''
        r = get_object_or_404(StatusReply, pk=self.reply_id)
        try:
            r.delete()
        except:
            return HttpResponse("failed", mimetype="application/json")
        return HttpResponse(json.dumps("success"), mimetype="application/json")
