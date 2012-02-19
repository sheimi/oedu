# Create your views here.
from Oedu.im.views import IMChannel
from Oedu.mail.models import Mail
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.core import serializers
from django.http import HttpResponse
from django.shortcuts import render_to_response, get_object_or_404
import datetime
import json
import poplib
import smtplib

@login_required
def index(request):
    user = request.user
    mails = Mail.objects.all().filter(to_user=user.pk)
    return render_to_response('mail/index.html', {'mails': mails})

@login_required
def popup(request, mail_id=0, receiver_id=0):
    '''
    url: /mail/popup
    @return: a popup page to set up a mail
    '''
    mail = None
    receiver = None
    if mail_id:
        mail = Mail.objects.get(pk=mail_id)
    if receiver_id:
        receiver = User.objects.get(pk=receiver_id)
    return render_to_response('mail/popup.html', {'mail' : mail, 'receiver' : receiver})

@login_required
def send(request):
    pass

@login_required
def get_mail(request):
    pass



class mail_detail:
    '''
    url:    /mail/crud/{mail_id}
    restful interface of a certain mail
    '''
    
    def __call__(self, request, mail_id = 0):
        self.request, self.user, self.build_absolute_uri, self.get_full_path = \
            request, request.user, request.build_absolute_uri, request.get_full_path
        self.mail_id = mail_id
        try:
            callback = getattr(self, "do_%s" % request.method)
        except AttributeError:
            pass
        return callback()
    
    @login_required  
    def do_GET(self):
        '''
        http method: GET
        @return: a dictionary of a certain mail 
            type:    json
            list of a dic:    
            sample:   [{
                            "pk": 1, 
                            "model": "mail.mail", 
                            "fields": {
                                "to_user": 2, 
                                "message": "test", 
                                "title": "test", 
                                "sent_time": "2011-05-12 10:56:43", 
                                "from_user": 1
                            }
                        }]
        '''
        m = get_object_or_404(Mail, pk=self.mail_id)
        return HttpResponse(serializers.serialize("json", [m]), mimetype="application/json")
    
    @login_required
    def do_POST(self):
        '''
        http method: POST
        to update a certain mail
        type:    json
        @param title:    title of the mail (optional)
        @param message:  content of the mail (optional)
        @param is_read:  (optional)
        @return: success or failed(a dictionary)
        '''
        m = get_object_or_404(Mail, pk=self.mail_id)
        post = json.loads(self.request.raw_post_data)
        try:
            m.title = post.has_key("title") and post["message"] or m.title
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
        to create a certain mail
        type:    json
        @param title:    title of the mail
        @param message:  content of the mail
        @param to_user: the id of the receiver of the mail
        @return: mail.pk or failed(a dictionary)
        '''
        put = json.loads(self.request.raw_post_data)
        try:
            m = self.request.user.mail_sent.create(title=put["title"],
                                                     message=put["message"],
                                                     to_user=User.objects.get(pk=put["to_user"]),
                                                     sent_time=datetime.datetime.now(),
                                                     is_read=False,
                                                )
        except:
            return HttpResponse("failed", mimetype="application/json")
        return HttpResponse(json.dumps(m.pk), mimetype="application/json")
    
    @login_required  
    def do_DELETE(self):
        '''
        http method: DELETE
        to delete a certain mail
        @return: success or failed(a dictionary)
        '''
        m = get_object_or_404(Mail, pk=self.mail_id)
        try:
            m.delete()
        except:
            return HttpResponse("failed", mimetype="application/json")
        return HttpResponse(json.dumps("success"), mimetype="application/json")
    
@login_required
def send_mail_mul(request):
    '''
    url: /mail/send/mul
    @param title:    title of the mail
    @param message:  content of the mail
    @param to_users: the list of id of the receiver of the mail
    @return: success or failed(a dictionary)
    '''
    put = json.loads(request.raw_post_data)
    us = put["to_users"]
    users = [User.objects.get(pk=u) for u in us]
    for user in users:
        request.user.mail_sent.create(title=put["title"], message=put["message"],to_user=user,
                                      sent_time=datetime.datetime.now(), is_read=False)
    return HttpResponse(json.dumps("success"), mimetype="application/json")