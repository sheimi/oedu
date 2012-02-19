# Create your views here.
from Oedu import settings, prefix
from Oedu.core.models import UserGroup
from Oedu.im.views import IMChannel
from Oedu.share.models import Share
from Oedu.status.models import Status
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.core import serializers
from django.core.servers.basehttp import FileWrapper
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, render_to_response, redirect
import datetime
import json
import os
import stat



class ConvertShares:
    
    def __call__(self, shares):
        render = []
        shares_render = json.loads(serializers.serialize("json", shares))
        for share in shares_render:
            if share["fields"]["type"]:
                callback = getattr(self, "convert_%s" % share["fields"]["type"])
                render.append(callback(share))
        return render
    
    def convert_status(self, share):
        url = share["fields"]["url"].split('/')
        id = url[-1]
        status = Status.objects.get(pk=int(id))
        status_render = json.loads(serializers.serialize("json", [status]))[0]
        share["share_object"] = status_render
        return share
    
    def convert_link(self, share):
        share["share_object"] = share["fields"]["url"]
        return share
    
    def convert_file (self, share):
        share["share_object"] = share["fields"]["url"]
        return share
    
convert_shares = ConvertShares()

@login_required
def index(request):
    '''
    url:      /share/
    @return: the partial page to set up an share 
    '''
    return render_to_response("share/upload.html", {'user': request.user})

@login_required
def get_share_list(request, user_id=0):
    '''
    url:    /share/share_list/
    @list: the list of shares of user
    '''
    if user_id == 0:
        u = request.user
    else:
        u = get_object_or_404(User, pk=user_id)
    shares = u.share_set.all().order_by('-publish_time')
    render = convert_shares(shares)
    return HttpResponse(json.dumps(render), mimetype="application/json")

@login_required
def get_share_list_all(request):
    '''
    url:    /share/share_list/all/
    @list: the list of shares of user
    '''
    shares = Share.objects.all().order_by('-publish_time')
    render = convert_shares(shares)
    return HttpResponse(json.dumps(render), mimetype="application/json")

@login_required
def get_share_list_by_user(request):
    '''
    url:    /share/share_list/user
    @return: 
    '''
    user = request.user
    groups = request.user.group_belong.all()
    shares = Share.objects.all().order_by('-publish_time')
    shares_render = []
    for share in shares:
        gs = share.share_to.all()
        for g in groups:
            if g in gs:
                shares_render.append(share)
                break
            
    render = convert_shares(shares_render)
    return HttpResponse(json.dumps(render), mimetype="application/json")
    

@login_required
def set_share_to(request, share_id):
    '''
    http method: POST
    type:    json
    @param operation: update or add or delete(change the users)
    @param groups: a list of group id (type json)
    @return: success or failed(a dictionary)
    '''
    share = get_object_or_404(Share, pk=share_id)
    post = json.loads(request.raw_post_data)
    try:
        operation = post.has_key("operation") and post["operation"] or None
        groups_id = post.has_key("groups") and post["groups"] or None
            
        def convert_id(group_id):
            return UserGroup.objects.get(pk=group_id)
        if groups_id:        
            groups = map(convert_id, groups_id)
        else:
            groups = []
        if operation == "update":
            share.share_to.clear()
            if groups:
                share.share_to.add(*groups)
        elif operation == "add":
            share.share_to.add(*groups)
        elif operation == "delete":
            share.share_to.remove(*groups)
        share.save()
    except:
        return HttpResponse("failed", mimetype="application/json")
    return HttpResponse(json.dumps("success"), mimetype="application/json")
    
class share_detail:
    '''
    url:    /share/crud/{anno_id}
    restful interface of a certain share
    '''
    
    def __call__(self, request, share_id = 0):
        self.request, self.user, self.build_absolute_uri, self.get_full_path = \
            request, request.user, request.build_absolute_uri, request.get_full_path
        self.share_id = share_id
        try:
            callback = getattr(self, "do_%s" % request.method)
        except AttributeError:
            pass
        return callback()
    
    @login_required  
    def do_GET(self):
        '''
        http method: GET
        @return: a dictionary of a certain share 
            type:    json
            list of a dic:    
            sample: [{
                        "pk": 1, 
                        "model": "share.share", 
                        "fields": {
                            "comment": "hello", 
                            "url": "http://google.com/", 
                            "publish_time": "2011-05-01 21:07:40", 
                            "publisher": 1
                        }
                    }] 
        '''
        s = get_object_or_404(Share, pk=self.share_id)
        render = convert_shares([s])
        return HttpResponse(json.dumps(render), mimetype="application/json")
    
    @login_required
    def do_POST(self):
        '''
        http method: POST
        to update a certain share
        type:    json
        @param comment:    comment of the share (optional)
        @param url:  url of the share (optional)
        @param type: type of the share
        @return: success or failed(a dictionary)
        '''
        s = get_object_or_404(Share, pk=self.share_id)
        post = json.loads(self.request.raw_post_data)
        try:
            s.comment = post.has_key("comment") and post["comment"] or s.comment
            s.url = post.has_key("url") and post["url"] or s.url
            s.type = post.has_key("type") and post["type"] or s.type
            s.save()
        except:
            return HttpResponse("failed", mimetype="application/json")
        return HttpResponse(json.dumps("success"), mimetype="application/json")
    
    @login_required  
    def do_PUT(self):
        '''
        http method: PUT
        to create a certain share
        type:    json
        @param comment:    comment of the share
        @param url:  url of the share
        @param publisher:    the id of publisher
        @param type: the type of...
        @return: success or failed(a dictionary)
        '''
        put = json.loads(self.request.raw_post_data)
        try:
            share= self.user.share_set.create(comment=put["comment"],
                                        publish_time=datetime.datetime.now(),
                                        url = put["url"], type=put["type"])
        except:
            return HttpResponse("failed", mimetype="application/json")
        return HttpResponse(json.dumps(share.pk), mimetype="application/json")
    
    @login_required  
    def do_DELETE(self):
        '''
        http method: DELETE
        to delete a certain share
        @return: success or failed(a dictionary)
        '''
        s = get_object_or_404(Share, pk=self.share_id)
        try:
            s.delete()
        except:
            return HttpResponse("failed", mimetype="application/json")
        return HttpResponse(json.dumps("success"), mimetype="application/json")


@login_required
def upload(request):
    if request.method == 'GET':
        return render_to_response("core/uploadfile_popup.html")
    else:
        
        file_name = request.POST.get("file.name", None)
        file_path = request.POST.get("file.path", None)
        file_path = file_path.split("/")[-1]
        url = "/static/files/" + file_path
        share = request.user.share_set.create(comment=file_name, publish_time=datetime.datetime.now(),
                                              url=url, type="file")
        path = prefix.DIR_PRE + 'Oedu/assets/files/' + share.url.split('/')[-1]
        os.chmod(path, stat.S_IMODE(os.stat(path)[stat.ST_MODE]) | stat.S_IRGRP | stat.S_IROTH | stat.S_IROTH) 
        return HttpResponse(json.dumps([share.url]), mimetype="application/json")

    
@login_required
def get_share_of_special_groups(request):
    '''
    url:    /share/statuslist/special
    http method: GET
    '''
    shares = Share.objects.filter(publisher__groups__id=6).order_by('-publish_time')
    render = convert_shares(shares)
    return HttpResponse(serializers.serialize("json", render), mimetype="application/json")

@login_required
def share_status(request, status_id):
    '''
    url:    /share/status/{status_id}
    '''
    url = '/status/crud/%s' % status_id
    share = request.user.share_set.create(comment='',
                                        publish_time=datetime.datetime.now(),
                                        url = url, type='status')
    return render_to_response("share/share_status_popup.html", {'share': share,
                                                                'user': request.user})
    
@login_required
def share_link(request):
    '''
    url: /stare/link/
    '''
    return render_to_response("share/share_link_popup.html", {'user': request.user})

@login_required
def share_pre(request, share_id):
    '''
    url:    /share/pre/{share_id}
    '''
    share = get_object_or_404(Share, pk=share_id)
    shared = share.share_to.all()
    shared_id = [shared_s.pk for shared_s in shared]
    all = request.user.groups_set.all()
    not_shared = []
    for g in all:
        if g.id not in shared_id:
            not_shared.append(g)
    return render_to_response("share/share_popup.html", {'share': share,
                                                         'user': request.user,
                                                         'not_shared': not_shared})
    
def download(request, share_id):
    '''
    url:    /share/downloads/{share_id}
    '''
    share = get_object_or_404(Share, pk=share_id)
    path = prefix.DIR_PRE + 'Oedu/assets/files/' + share.url.split('/')[-1]
    f = open(path, 'rb')
    response = HttpResponse(FileWrapper(f), mimetype = 'application/force-download')
    response['Content-Disposition'] = "attacment; filename = %s" % share.comment
    return response
    response['Content-Length'] = os.path.getsize(path)