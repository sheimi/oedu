# Create your views here.
from Oedu.schedule.models import Schedule
from django.contrib.auth.decorators import login_required
from django.core import serializers
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from django.contrib.auth.models import User
import json

@login_required
def index(request):
    '''
    url:      /schedule/
    @return: the partial page to set up an schedule 
    '''
    return HttpResponse("this is the index page")

@login_required
def get_schedule_list(request, teacher_id=0):
    '''
    url:    /schedule/schedule_list/
    @return: a list of schedule, use fullcalendar api
    '''
    if teacher_id == 0:
        u = request.user
    else:
        u = get_object_or_404(User, pk=teacher_id)
    s_list = u.schedule_set.all()
    render = []
    for s in s_list :
        r = {}
        r["id"] = s.pk
        r["title"] = s.content
        r["start"] = s.starttime.__str__()
        r["end"] = s.endtime.__str__()
        render.append(r)
    return HttpResponse(json.dumps(render), mimetype="application/json")

class schedule_detail:
    '''
    url:    /schedule/crud/{schedule_id}
    restful interface of a certain schedule
    '''
    
    def __call__(self, request, schedule_id = 0):
        self.request, self.user, self.build_absolute_uri, self.get_full_path = \
            request, request.user, request.build_absolute_uri, request.get_full_path
        self.schedule_id = schedule_id
        try:
            callback = getattr(self, "do_%s" % request.method)
        except AttributeError:
            pass
        return callback()
    
    @login_required  
    def do_GET(self):
        '''
        http method: GET
        @return: a dictionary of a certain schedule 
            type:    json
            list of a dic:    
            sample:   [{
                        "pk": 1, 
                        "model": "schedule.schedule", 
                        "fields": {
                            "content": "work", 
                            "teacher": 1, 
                            "startime": "2011-04-28 14:14:55"
                            "endtime" : ""
                        }
                    }]
        '''
        s = get_object_or_404(Schedule, pk=self.schedule_id)
        return HttpResponse(serializers.serialize("json", [s]), mimetype="application/json")
    
    @login_required
    def do_POST(self):
        '''
        http method: POST
        to update a certain schedule
        type:    json
        @param content:  content of the schedule (optional)
        @return: success or failed(a dictionary)
        '''
        s = get_object_or_404(Schedule, pk=self.schedule_id)
        post = json.loads(self.request.raw_post_data)
        try:
            s.content = post.has_key('content') and post['content'] or s.content
            s.save()
        except:
            return HttpResponse("failed", mimetype="application/json")
        return HttpResponse(json.dumps("success"), mimetype="application/json")
    
    @login_required  
    def do_PUT(self):
        '''
        http method: PUT
        to create a certain schedule
        type:    json
        @param content:  content of the schedule
        @param starttime:
        @param endtime:
        @return: success or failed(a dictionary)
        '''
        post = json.loads(self.request.raw_post_data)
        s = self.request.user.schedule_set.create(content=post['content'],
                        starttime=post['starttime'], endtime=post['endtime'])
        return HttpResponse(json.dumps(s.pk), mimetype="application/json")
                                             
    @login_required  
    def do_DELETE(self):
        '''
        http method: DELETE
        to delete a certain schedule
        @return: success or failed(a dictionary)
        '''
        s = get_object_or_404(Schedule, pk=self.schedule_id)
        try:
            s.delete()
        except:
            return HttpResponse("failed", mimetype="application/json")
        return HttpResponse(json.dumps("success"), mimetype="application/json")