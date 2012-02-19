# Create your views here.
from Oedu.rent.models import Application
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
    url:      /rent/
    '''
    applications = Application.objects.filter(is_approved=True).order_by("-datetime")
    return render_to_response('rent/index.html', {'user' : request.user,'applications': applications})

@login_required
def popup(request): 
    '''
    url:    /rent/popup
    @return:  a popup page to create a application
    '''
    return render_to_response('rent/popup.html')

@login_required
def get_rent_by_teacher(request, teacher_id=0):
    '''
    url: /rent/teacher/{teacher_id}
    method: GET
    '''
    if teacher_id:
        user = get_object_or_404(User, pk=teacher_id)
    else:
        user = request.user
    applications = user.applications_to.filter(is_approved=False).order_by("-datetime")
    return HttpResponse(serializers.serialize("json", applications), mimetype="application/json")


@login_required
def get_application_list(request):
    '''
    url:    /rent/application_list
    @param isAll: 
    @param after:
    @return: a list of application 
    '''
    after = request.POST.get("after", None)
    a_list = Application.objects.all()
    if after:
        after = (datetime.datetime)(after)
        a_list = a_list.filter(datetime_gte=after)
    return HttpResponse(serializers.serialize("json", a_list), mimetype="application/json")

class rent_detail:
    '''
    url:    /rent/crud/{rent_id}
    restful interface of a certain rent
    '''
    def __call__(self, request, rent_id = 0):
        self.request, self.user, self.build_absolute_uri, self.get_full_path = \
            request, request.user, request.build_absolute_uri, request.get_full_path
        self.rent_id = rent_id
        try:
            callback = getattr(self, "do_%s" % request.method)
        except AttributeError:
            pass
        return callback()
    
    @login_required  
    def do_GET(self):
        '''
        http method: GET
        @return: a dictionary of a certain rent 
            type:    json
            list of a dic:    
            sample:   [{
                        "pk": 1, 
                        "model": "rent.application", 
                        "fields": {
                            "is_approved": false, 
                            "to_teacher": 1, 
                            "title": "title", 
                            "datetime": "2011-04-28 14:25:37", 
                            "content": "123", 
                            "applicants": 2
                        }
                    }]
        '''
        a = get_object_or_404(Application, pk=self.rent_id)
        return HttpResponse(serializers.serialize("json", [a]), mimetype="application/json")
    
    @login_required
    def do_POST(self):
        '''
        http method: POST
        to update a certain application
        type:    json
        @param title:    title of the application (optional)
        @param content:  content of the application (optional)
        @param is_approved: whether the application is approved (optional)
        @return: success or failed(a dictionary)
        '''
        a = get_object_or_404(Application, pk=self.rent_id)
        post = json.loads(self.request.raw_post_data)
        try:
            a.title = post.has_key("title") and post["title"] or a.title
            a.content = post.has_key("content") and post["content"] or a.content
            a.is_approved = post.has_key("is_approved") and post["is_approved"] or a.is_approved
            a.is_processed = True
            a.save()
        except:
            return HttpResponse("failed", mimetype="application/json")
        return HttpResponse(json.dumps("success"), mimetype="application/json")
    
    @login_required  
    def do_PUT(self):
        '''
        http method: PUT
        to create a certain application
        type:    json
        @param title:    title of the application
        @param content:  content of the application
        @param to_teacher: the id of the teacher
        @return: r.pk or failed(a dictionary)
        '''
        
        put = json.loads(self.request.raw_post_data)
        u = get_object_or_404(User, pk=put["to_teacher"])
        try:
            r = self.user.applications_own.create(    title=put["title"],
                                                      content=put["content"],
                                                      is_approved=False,
                                                      datetime=datetime.datetime.now(),
                                                      to_teacher=u,
                                                      is_processed=False,
                                                )
        except:
            return HttpResponse("failed", mimetype="application/json")
        return HttpResponse(json.dumps(r.pk), mimetype="application/json")
    
    @login_required  
    def do_DELETE(self):
        '''
        http method: DELETE
        to delete a certain application
        @return: success or failed(a dictionary)
        '''
        r = get_object_or_404(Application, pk=self.rent_id)
        try:
            r.delete()
        except:
            return HttpResponse("failed", mimetype="application/json")
        return HttpResponse(json.dumps("success"), mimetype="application/json")