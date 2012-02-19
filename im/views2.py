'''
Created on Jun 2, 2011

@author: zhangsheimi
'''
from Oedu.django_tornado.decorator import asynchronous
from Oedu.im.channel import Channel
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
import json

@login_required
@asynchronous
def update(request, handler):
    '''
    url: /im2/update
    http method: GET
    '''
    cursor = request.POST.get("cursor", None)
    def on_new_messages(messages):
        if handler.request.connection.stream.closed():
            return
        m = json.dumps(messages)
        handler.finish(m)
    channel = Channel()
    channel.wait_for_messages(handler.async_callback(on_new_messages), 
                                   (int)(request.user.id), cursor=cursor)

@login_required
def new_session(request):
    '''
    init a new session
    url: /im2/new_session
    http method: POST
    @param users: a list of id of user
    @param session_name: (optional)
    @return: json
    {
        'session_id'    :    a uuid to identify this session
        'session_name'  :    the name of this session, null if 1-1
        'users'         :    a list of user info   {name: , id:, is_online}
        'status'        :    the status of this session true is alive, false means no one is online
    }
    '''
    post = json.loads(request.raw_post_data)
    users = []
    us = post["users"]
    user_online = []
    session_name = post.has_key('session_name') and post["session_name"] or None
    channel = Channel()
    for u in us:
        user = get_object_or_404(User, pk=u)
        is_online = channel.is_online(u)
        user_info = {
            'id'     :  u,
            'name'   :  user.get_profile().name,
            'is_online' : is_online
        }
        users.append(user_info)
        if is_online :
            user_online.append(u)
    
    render = {
        'session_id'    :   None,
        'session_name'  :   session_name,
        'users'         :   users,
        'status'        :   False
    }
    if user_online:
        user_online.append(request.user.pk)
        render['session_id'] = channel.new_session(session_name, *user_online)["session_id"]
        render['status'] = True
    return HttpResponse(json.dumps(render), mimetype="application/json")

@login_required
def new_im(request):
    '''
    send message
    url: /im2/new_message
    http method: POST
    @param session_id: 
    @param message: 
    @return: 
    {
        'session_info' : {
            'session_id'    :
            'session_name'  :
            'users'         :
            'status'        :
        },
        sender_id:
        sender_name:
        type: 'im'
        message: the content
    }
    '''
    post = json.loads(request.raw_post_data)
    session_id = post["session_id"]
    channel = Channel()
    session = channel.check_session(session_id)
    if not session:
        pass
    session_status = {
        'session_id'  : session_id,
        'session_name': session["session_name"],
        'status'      : True,
        'users'       : session["users"],
    }
    message = {
            'sender_id'  :   request.user.pk,
            'sender_name':   request.user.get_profile().name,
            'type'       :   'im',
            'message'    :   post["message"],
            'session_info':  session_status,
    }
    channel.new_im(message, session_id)
    return HttpResponse(json.dumps(message), mimetype="application/json")

@login_required
def add_user(request):
    '''
    add users to a session
    url: /im2/add_user
    http method: POST
    @param users: a list of user id
    @param sesson_id: 
    @return: 
    {
        failed_list: a list of users {user_id: , user_name:}
        session_info: {
            'session_id'    :
            'session_name'  :
            'users'         :
            'status'        :
        }
    }
    '''
    post = json.loads(request.raw_post_data)
    session_id = post["session_id"]
    channel = Channel()
    session = channel.check_session(session_id)
    if not session:
        pass
    channel.add_users(session_id, *post["users"])
    render = {
        'failed_list' : [],
        'session_info': {
            'session_id'    : session_id,
            'session_name'  : session["session_name"],
            'users'         : session["users"],
            'status'        : True,
        }
    }
    return HttpResponse(json.dumps(render), mimetype="application/json")
    
    
    

@login_required
def quit(request):
    '''
    quit a session
    http method: POST
    url: /im2/quit
    @param session_id: 
    @return: success or failed
    '''
    post = json.loads(request.raw_post_data)
    session_id = post["session_id"]
    channel = Channel()
    session = channel.check_session(session_id)
    if not session:
        return HttpResponse(json.dumps('failed, session not exist'), mimetype="application/json")
    channel.quit(session_id, request.user.pk)
    return HttpResponse(json.dumps('success'), mimetype="application/json")
    

@login_required
def online_list(reqeust):
    '''
    check the online user
    http method: GET
    return:
    a list of on line user
    '''
    channel = Channel()
    on_line_users = []
    for key, value in channel.waiters.iteritems():
        if len(value):
            on_line_users.append(key)
    return HttpResponse(json.dumps(on_line_users), mimetype="application/json")