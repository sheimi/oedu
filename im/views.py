# Create your views here.
from Oedu.core.models import Tag, UserGroup
from Oedu.django_tornado.decorator import asynchronous
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import render_to_response, redirect, get_object_or_404
import json
import logging
import uuid

class IMChannel(object):
    '''
    An im channel
    '''
    _instance = None
    waiters = {}
    cache = []
    cache_size = 200

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super(IMChannel, cls).__new__(
                                        cls, *args, **kwargs)
        return cls._instance
    
    def wait_for_messages(self, callback, id, cursor=None):
        if cursor:
            index = 0
            for i in xrange(len(self.cache)):
                index = len(self.cache) - i - 1
                if self.cache[index]["id"] == cursor: break
            recent = self.cache[index + 1:]
            if recent:
                callback(recent)
                return
        if self.waiters.has_key(id):
            self.waiters[id].append(callback)
        else: 
            self.waiters[id] = [callback]

    def on_new_messages(self, message, id):
        if not self.waiters.has_key(id):
            return
        callbacks = self.waiters[id]
        while len(callbacks):
            callback = callbacks.pop()
            callback(message)
            
    def on_new_tag_chat(self, message, tag_id):
        tag = get_object_or_404(Tag, pk=tag_id)
        message["tag_name"] = tag.description
        users = tag.users.all()
        for user in users:
            self.on_new_messages(message, user.pk)
            
    def on_new_usergroup_chat(self, message, usergroup_id):
        ug = get_object_or_404(UserGroup, pk=usergroup_id)
        message["usergroup_name"] = ug.description
        users = ug.users.all()
        for user in users:
            self.on_new_messages(message, user.pk)
        
            
    def is_online(self, id):
        if not self.waiters.has_key(id):
            return False;
        callbacks = self.waiters[id]
        if len(callbacks) == 0:
            return False;
        return True;
        
@login_required
@asynchronous
def update(request, handler):
    cursor = request.POST.get("cursor", None)
    def on_new_messages(messages):
        if handler.request.connection.stream.closed():
            return
        m = json.dumps(messages)
        handler.finish(m)
    channel = IMChannel()
    channel.wait_for_messages(handler.async_callback(on_new_messages), 
                                   (int)(request.user.id), cursor=cursor)
'''
@login_required 
def newIM(request):
    message = {
            "id": str(uuid.uuid4()),
            "from": request.user.username,
            "body": request.POST.get("body", None)
    }
    message["html"] = '<div class="message" id="m%s"> \
                        <b>%s: </b>%s</div>' \
                        % (message['id'], message['from'], message['body'])
    if request.POST.get("next", None):
        redirect(request.POST["next"])
    else:
        pass
    to_id = request.POST.get("to_id", None)
    if to_id:
        channel = IMChannel()
        channel.on_new_messages([message], (int)(to_id))
    return HttpResponse(json.dumps(message), mimetype="application/json")
'''

@login_required
def new_im(request):
    '''
    a new message come
    url: /im/newmessage
    method: POST
    datatype:json
    @param receiver:  id of message receiver
    @param message:    the message content
    return data:
    {
        id: uuid,
        type: 'im',
        message: the message
        sender_id:
        reseiver_id:
    }
    '''
    post = json.loads(request.raw_post_data)
    message = {
            'id'        :   str(uuid.uuid4()),
            'type'      :   'im',
            'sender'    :   request.user.username,
            'sender_id' :   request.user.pk,
            'message'   :   post["message"],
    }
    
    receiver = post.has_key("receiver") and post["receiver"] or None
    if receiver:
        message["receiver_id"] = receiver
        channel = IMChannel()
        is_online = channel.is_online(receiver)
        if not is_online:
            message["type"] = "not_online"
            from Oedu.message.views import leave_message
            leave_message(message["message"], message["sender_id"], receiver)
            return HttpResponse(json.dumps(message), mimetype="application")
        channel.on_new_messages(message, (int)(receiver))
    return HttpResponse(json.dumps(message), mimetype="application/json")

@login_required
def new_im_by_tag(request):
    '''
    a new message come
    url: /im/newmessage/tag
    method: POST
    datatype:json
    @param tag_id:  id of a tag
    @param message:    the message content
    return data:
    {
        id: uuid,
        type: 'im-tag',
        message: the message
        sender: the name of sender
        sender_id: the id of sender
        tag_id:
    }
    other people can receive a tag name
    '''
    post = json.loads(request.raw_post_data)
    message = {
            'id'        :   str(uuid.uuid4()),
            'type'      :   'im-tag',
            'sender'    :   request.user.username,
            'sender_id' :   request.user.pk,
            'tag_id'    :   post["tag_id"],
            'message'   :   post["message"],
    }
    channel = IMChannel()
    channel.on_new_tag_chat(message, post["tag_id"])
    return HttpResponse(json.dumps(message), mimetype="application/json")
    
@login_required
def new_im_by_usergroup(request):
    '''
    a new message come
    url: /im/newmessage/usergroup
    method: POST
    datatype:json
    @param usergroup_id:  id of a usergroup
    @param message:    the message content
    return data:
    {
        id: uuid,
        type: 'im-usergroup',
        message: the message
        sender: the name of sender
        usergroup_id:
        sender_id
    }
    other people can receive a usergroup name
    '''
    post = json.loads(request.raw_post_data)
    message = {
            'id'        :   str(uuid.uuid4()),
            'type'      :   'im-usergroup',
            'sender'    :   request.user.username,
            'sender_id' :   request.user.pk,
            'message'   :   post["message"],
            'usergroup_id' :   post["usergroup_id"],
    }
    channel = IMChannel()
    channel.on_new_usergroup_chat(message, post["usergroup_id"])
    return HttpResponse(json.dumps(message), mimetype="application/json")

@login_required
def test(request):
    return render_to_response("im/test.html")

@login_required
def online_list(request):
    channel = IMChannel()
    on_line_users = []
    for key, value in channel.waiters.iteritems():
        if len(value):
            on_line_users.append(key)
    return HttpResponse(json.dumps(on_line_users), mimetype="application/json")