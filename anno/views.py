# -*- coding: utf-8 -*- 
'''
@author: sheimi
04/30/2011
'''
from Oedu.anno.models import Announcement, AnnouncementReply, \
    AnnouncementReceiver
from Oedu.core.models import UserProfile
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.core import serializers
from django.http import HttpResponse, QueryDict
from django.shortcuts import render_to_response, get_object_or_404
import datetime
import json

@login_required
def index(request):
    '''
    url:      /anno/
    @return:
    '''
    if u'学生' not in request.user.groupnames():
        annos = request.user.announcement_set.all()
    else:   
        ar_set = request.user.announcementreceiver_set.order_by("-publish_time")
        annos = [ar.announcement for ar in ar_set]
    return render_to_response('anno/index.html', {'annos': annos})

@login_required
def popup(request):
    '''
    url:    /anno/popup/
    @return: a popup page of announcement
    '''
    return render_to_response('anno/popup.html')

@login_required
def read_anno(request, anno_id):
    '''
    url:    /anno/anno_id/read
    @return: a page of reading an announcement 
    '''
    anno = Announcement.objects.get(pk=anno_id)
    try:
        anno_receiver = AnnouncementReceiver.objects.get(user__pk=request.user.pk, announcement__pk=anno.pk)
        anno_receiver.isRead = True
        anno_receiver.save()
    except:
        pass
    return render_to_response('anno/read_anno.html', {'anno' : anno, 'user': request.user})

@login_required
def get_unread_statistics(request, anno_id):
    '''
    url:    /anno/anno_id/unread
    @return: a page
    '''
    anno = Announcement.objects.get(pk=anno_id)
    return render_to_response('anno/anno_unread.html', {'user' : request.user, 'anno' : anno})

@login_required
def get_anno_list(request, user_id=0):
    '''
    url:    /anno/annolist/{user_id}
    http method: GET
    @param isAll: if it == true, return all the objects(option), or return those no read
    '''
    if user_id == 0:
        u = request.user
    else:
        u = get_object_or_404(User, pk=user_id)
    ar_set = u.announcementreceiver_set.filter(isRead=False).order_by("-publish_time")
    a_set = [ar.announcement for ar in ar_set]
    return HttpResponse(serializers.serialize("json", a_set), mimetype="application/json")

@login_required        
def index_reply(request):
    '''
    url:/anno/reply/
    @param anno_id: 
    @return:
    '''
    return render_to_response('anno/reply.html', {"anno_id" : request.POST.get('anno_id', None)})

@login_required
def reply_popup(request):
    '''
    url:/anno/reply/popup
    @param anno_id:
    @return: a popup page to create a reply
    '''
    return render_to_response('anno/reply_popup.html', {"anno_id" : request.POST.get('anno_id', None)})

@login_required
def get_reply_list(request, anno_id):
    '''
    url:    /anno/replylist/anno/{anno_id}/
    http method: GET
    @return: a list of replies
    '''
    anno = get_object_or_404(Announcement, pk=anno_id)
    render = anno.announcementreply_set.all().order_by('publish_time')
    return HttpResponse(serializers.serialize("json", render), mimetype="application/json")

@login_required
def pub_anno(request):
    '''
    url:    /anno/pub_anno
    http method: PUT
    @param users: a list of users
    @param title:
    @param content:
    '''
    put = json.loads(request.raw_post_data)
    anno = request.user.announcement_set.create(title=put["title"],
                                              content=put["content"],
                                              grade=0,
                                              publish_time=datetime.datetime.now()) 
    time = anno.publish_time
    us = put["users"]
    users = [User.objects.get(pk=u) for u in us]
    for user in users:
        re = anno.announcementreceiver_set.create(isRead=False, publish_time=time, user=user)
    anno.save()
    return HttpResponse(json.dumps(anno.pk), mimetype="application/json")

class announcement_detail:
    '''
    url:    /anno/crud/{anno_id}
    restful interface of a certain announcement
    '''
    def __call__(self, request, anno_id = 0):
        self.request, self.user, self.build_absolute_uri, self.get_full_path = \
            request, request.user, request.build_absolute_uri, request.get_full_path
        self.anno_id = anno_id
        try:
            callback = getattr(self, "do_%s" % request.method)
        except AttributeError:
            pass
        return callback()
    
    @login_required  
    def do_GET(self):
        '''
        http method: GET
        @return: a dictionary of a certain announcement 
            type:    json
            list of a dic:    
            sample:   [{
                    "pk": 1, 
                    "model": "anno.announcement", 
                    "fields": {
                        "content": "hello world", 
                        "publisher": 1, 
                        "publish_time": "2011-04-28 11:26:33", 
                        "grade": 10, 
                        "title": "hello"
                        }
                }]
        '''
        a = get_object_or_404(Announcement, pk=self.anno_id)
        return HttpResponse(serializers.serialize("json", [a]), mimetype="application/json")
    
    @login_required
    def do_POST(self):
        '''
        http method: POST
        to update a certain announcement
        type:    json
        @param title:    title of the announcement (optional)
        @param content:  content of the announcement (optional)
        @param grade:    the grade to receive the announcement (optional)
        @return: success or failed(a dictionary)
        '''
        a = get_object_or_404(Announcement, pk=self.anno_id)
        post = json.loads(self.request.raw_post_data)
        try:
            a.title = post.has_key("title") and post["title"] or a.title
            a.content = post.has_key("content") and post["content"] or a.content
            a.grade = post.has_key("grade") and post["grade"] or a.grade
            a.save()
        except:
            return HttpResponse("failed", mimetype="application/json")
        return HttpResponse(json.dumps("success"), mimetype="application/json")
    
    @login_required 
    def do_PUT(self):
        '''
        http method: PUT
        to create a certain announcement
        type:    json
        @param title:    title of the announcement
        @param content:  content of the announcement
        @param grade:    the grade to receive the announcement 
        @return: id or failed(a dictionary)
        '''
        put = json.loads(self.request.raw_post_data)
        try:
            anno = self.user.announcement_set.create(title=put["title"],
                                              content=put["content"],
                                              grade=put["grade"],
                                              publish_time=datetime.datetime.now()) 
            profiles = UserProfile.objects.filter(grade=anno.grade)
            users = [p.user for p in profiles]
            time = anno.publish_time
            for user in users:
                re = anno.announcementreceiver_set.create(isRead=False, publish_time=time, user=user)
            anno.save()
        except:
            return HttpResponse("failed", mimetype="application/json")
        return HttpResponse(json.dumps(anno.pk), mimetype="application/json")
    
    @login_required  
    def do_DELETE(self):
        '''
        http method: DELETE
        to delete a certain announcement
        @return: success or failed(a dictionary)
        '''
        a = get_object_or_404(Announcement, pk=self.anno_id)
        try:
            a.delete()
        except:
            return HttpResponse("failed", mimetype="application/json")
        return HttpResponse(json.dumps("success"), mimetype="application/json")
 
class reply_detail:
    '''
    url:    /anno/reply/crud/{reply_id}/
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
                    "model": "anno.announcementreply", 
                    "fields": {
                        "content": "hello", 
                        "publisher": 2, 
                        "publish_time": "2011-04-28 11:27:00", 
                        "announcement": 1 (id)
                    }
                }]
        '''
        r = get_object_or_404(AnnouncementReply, pk=self.reply_id)
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
        r = get_object_or_404(AnnouncementReply, pk=self.reply_id)
        post = json.loads(self.request.raw_post_data)
        r.content = post.has_key("content") and post["content"] or r.content
        r.save()
        return HttpResponse(json.dumps("success"), mimetype="application/json")
    
    @login_required  
    def do_PUT(self):
        '''
        http method: PUT
        to create a certain reply
        type:    json
        @param content: the content of a reply
        @param announcement: the id of the announcemet
        @return: reply.pk or failed(a dictionary)
        '''
        put = json.loads(self.request.raw_post_data)
        a = get_object_or_404(Announcement, pk=put["announcement"])
        r = a.announcementreply_set.create(content=put["content"],
                                           publisher=self.request.user,
                                           publish_time=datetime.datetime.now())
        return HttpResponse(json.dumps(r.pk), mimetype="application/json")
    
    @login_required  
    def do_DELETE(self):
        '''
        http method: DELETE
        to delete a certain reply
        @return: success or failed(a dictionary)
        '''
        r = get_object_or_404(AnnouncementReply, pk=self.reply_id)
        r.delete()
        return HttpResponse(json.dumps("success"), mimetype="application/json")
