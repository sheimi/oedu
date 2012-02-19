# Create your views here.
from Oedu.im.views import IMChannel
from Oedu.message.models import Message
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.core import serializers
from django.http import HttpResponse
from django.shortcuts import render_to_response, get_object_or_404
import datetime
import json
import poplib
import smtplib

def leave_message(message, from_user_id, to_user_id):
    from_user = get_object_or_404(User, pk=from_user_id)
    to_user = get_object_or_404(User, pk=to_user_id)
    m = from_user.message_sent.create(message=message, to_user=to_user,
                                      sent_time=datetime.datetime.now(),
                                      is_read=False)
    

class message_detail:
    '''
    url:    /message/crud/{message_id}
    restful interface of a certain message
    '''
    
    def __call__(self, request, message_id = 0):
        self.request, self.user, self.build_absolute_uri, self.get_full_path = \
            request, request.user, request.build_absolute_uri, request.get_full_path
        self.message_id = message_id
        try:
            callback = getattr(self, "do_%s" % request.method)
        except AttributeError:
            pass
        return callback()
    
    @login_required  
    def do_GET(self):
        '''
        http method: GET
        @return: a dictionary of a certain message 
            type:    json
            list of a dic:    
            sample:
        '''
        m = get_object_or_404(Message, pk=self.message_id)
        return HttpResponse(serializers.serialize("json", [m]), mimetype="application/json")
    
    @login_required
    def do_POST(self):
        '''
        http method: POST
        to update a certain 
        type:    json
        @param message:  content of the message (optional)
        @param is_read:  (optional)
        @return: success or failed(a dictionary)
        '''
        m = get_object_or_404(Message, pk=self.message_id)
        post = json.loads(self.request.raw_post_data)
        try:
            m.message = post.has_key("message") and post["message"] or m.message
            m.is_read = post.has_key("is_read") and post["is_read"] or m.is_read
            m.save()
        except:
            return HttpResponse("failed", mimetype="application/json")
        return HttpResponse(json.dumps("success"), mimetype="application/json")
    
    
    @login_required  
    def do_PUT(self):
        '''
        http method: PUT
        to create a certain message
        type:    json
        @param message:  content of the message
        @param to_user: the id of the receiver of the message
        @return: message.pk or failed(a dictionary)
        '''
        put = json.loads(self.request.raw_post_data)
        try:
            m = self.request.user.message_sent.create(message=put["message"],
                                                     to_user=User.objects.get(pk=put["to_user"]),
                                                     sent_time=datetime.datetime.now(),
                                                     is_read=False,
                                                )
            #notice the receiver
#            me = {'type' :   'message',
#                  'id'   :   m.id,
#                 }
#            channel = IMChannel()
#            channel.on_new_messages(me, put["resceiver"]) 
        except:
            return HttpResponse("failed", mimetype="application/json")
        return HttpResponse(json.dumps(m.pk), mimetype="application/json")
    
    @login_required  
    def do_DELETE(self):
        '''
        http method: DELETE
        to delete a certain message
        @return: success or failed(a dictionary)
        '''
        m = get_object_or_404(Message, pk=self.message_id)
        try:
            m.delete()
        except:
            return HttpResponse("failed", mimetype="application/json")
        return HttpResponse(json.dumps("success"), mimetype="application/json")