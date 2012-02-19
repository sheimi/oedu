# Create your views here.
'''
this is the view module
contains all the vew function of
'''

from Oedu import settings
from Oedu.core.models import Tag, UserGroup
from django import forms
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User, Group
from django.core import serializers
from django.http import HttpResponse, QueryDict
from django.shortcuts import render_to_response, redirect, get_object_or_404
from tornado.web import HTTPError
import json
import poplib

@login_required
def index(request):
    '''
    the index page of user
    url: /
    @return: 'user' : request.user
    '''
    render = {  'user'          :   request.user,
                'color_theme'   :   'peace',
                'now'           :   'home',
              }
    return render_to_response("core/index.html", render)

@login_required
def profile(request, user_id=0):
    '''
    url: /profile/
    the profile page of a person
    @return: user : the user himself
             profile: the information of the  owner of the page
    '''
    if user_id == 0 :
        rd = '/profile/%d' % request.user.pk
        return redirect(rd) 
    else:
        user = get_object_or_404(User, pk=user_id)
    #profile = user.get_profile()
    
    #fix the profile to render
    '''
    profile_render = {  'username'  :   user.username,
                        'groups'    :   user.groups.all(),
                        'email'     :   user.email,
                        'id'        :   user.pk,
                        'name'      :   profile.name,
                        'njuid'     :   profile.nju_id,
                        'grade'     :   profile.grade,
                        'mobile'    :   profile.mobile,
                        'qq'        :   profile.qq,
                      }
    profile_render['qq'] = profile.qq
    '''
    render = {'user'    :   request.user,
              'profile' :   user,
              'now'     :   'profile',
              }
    
    return render_to_response('core/profile.html', render)

def signin(request):
    '''
    to signin
    '''
    if request.method == "GET":
        return render_to_response('core/signin.html', {'next': request.GET.get('next', None)})
    elif request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        if user is not None:
            if user.is_active:
                login(request, user)
                next = request.POST.get('next', None)
                if next :
                    return redirect(request.POST['next'])
                else:
                    return redirect('/')
            # Redirect to a success page.
            else:
                return render_to_response('core/signin.html',
                                            {
                                                'next': request.POST.get('next', '/'),
                                                'error': 'user not active',
                                            })
            # Return a 'disabled account' error message
        else:
            return render_to_response('core/signin.html',
                                            {
                                                'next': request.POST.get('next', '/'),
                                                'error': 'user not active',
                                            })
            pop = poplib.POP3(settings.POP_URL, 110, 1)
            try:
                pop.user(username)
                pop.pass_(password)
            except :
                return render_to_response('core/signin.html',
                                            {
                                                'next': request.POST.get('next', '/'),
                                                'error': 'authenticate fail',
                                            })
            User.objects.create_user(username, username + '@' + settings.POP_URL, password)
            user = authenticate(username=username, password=password)
            user.userprofile_set.create(name="xx", nju_id="xxxxxxxxx", grade=2009)
            
            login(request, user)
            next = request.POST.get('next', None)
            if next :
                return redirect(request.POST['next'])
            else:
                return redirect('/')
            # Return an 'invalid login' error message.
            
def signout(request):
    '''
    to signout
    '''
    logout(request)
    return redirect(settings.LOGIN_URL)

@login_required
def upload_image(request):
    if request.method == 'GET':
        return render_to_response("test/upload_plugin.html")
    else:
        file = request.FILES["file"]
        subfix = file.name.split('.')[-1]
        img_url = str(request.user.pk)
        file_path = settings.STATIC_DIR + 'images/profile/' + img_url
        profile = request.user.get_profile()
        profile.img = img_url
        profile.save()
        destination = open(file_path, 'wb+')
        for chunk in file.chunks():
            destination.write(chunk)
        destination.close()
        return HttpResponse(json.dumps("success"))

class user_detail:
    '''
    url:    /core/crud/{user_id}
    restful interface of a certain user
    '''
    def __call__(self, request, user_id = 0):
        self.request, self.user, self.build_absolute_uri, self.get_full_path = \
            request, request.user, request.build_absolute_uri, request.get_full_path
        self.user_id = user_id
        try:
            callback = getattr(self, "do_%s" % request.method)
        except AttributeError:
            pass
        return callback()
    
    @login_required  
    def do_GET(self):
        '''
        http method: GET
        @return: a dictionary of a certain user 
            type:    json
            list of a dic:    
            sample:   
            [{
                pk:
                username:
                e_mail:
                
                pk_profile:
                name:
                nju_id:
                grade:
                address:
                mobile:
                qq:
                msn:
                research_field:
                interested_in:
                description:
                location:
            }]
        '''
        if not self.user_id:
            u = self.request.user
        else:
            u = get_object_or_404(User, pk=self.user_id)
        p = u.get_profile()
        render = {
                  "pk"              :   u.pk,
                  "username"        :   u.username,
                  "e_mail"          :   u.email,
                  
                  "pk_profile"      :   p.pk,
                  "name"            :   p.name,
                  "nju_id"          :   p.nju_id,
                  "grade"           :   p.grade,
                  "address"         :   p.address,
                  "mobile"          :   p.mobile,
                  "qq"              :   p.qq,
                  "msn"             :   p.msn,
                  "research_field"  :   p.research_field,
                  "interested_in"   :   p.interested_in,
                  "description"     :   p.description,
                  "location"        :   p.location,
                  "img"             :   p.img,
                }
        return HttpResponse(json.dumps([render]), mimetype="application/json")
    
    @login_required
    def do_POST(self):
        '''
        http method: POST
        to update a certain user
        type:    json
        @param email: (optional)
        @param name: the real name(optional)
        @param nju_id: (optional)
        @param grade: (optional)
        @param address: (optional)
        @param mobile: (optional)
        @param qq: (optional)
        @param msn: (optional)
        @param research_field: (optional)
        @param interested_in: (optiional)
        @param description: (optional)
        @param location: (optional)
        @return: success or failed(a dictionary)
        '''
        if not self.user_id:
            u = self.request.user
        else:
            u = get_object_or_404(User, pk=self.user_id)
        u = get_object_or_404(User, pk=self.user_id)
        post = json.loads(self.request.raw_post_data)
        try:
            p = u.get_profile()
            u.email =  post.has_key("email") and post["email"] or u.email
            u.save()
            p.name = post.has_key("name") and post["name"] or p.name
            p.nju_id = post.has_key("nju_id") and post["nju_id"] or p.nju_id
            p.grade = post.has_key("grade") and post["grade"] or p.grade
            p.address = post.has_key("address") and post["address"] or p.address
            p.mobile = post.has_key("mobile") and post["mobile"] or p.mobile
            p.qq = post.has_key("qq") and post["qq"] or p.qq
            p.msn = post.has_key("msn") and post["msn"] or p.msn
            p.research_field = post.has_key("research_field") \
                                    and post["research_field"] or p.research_field
            p.interested_in = post.has_key("interested_in") \
                                    and post["interested_in"] or p.interested_in
            p.description = post.has_key("description") \
                                    and post["description"] or p.description
            p.location = post.has_key("location") \
                                    and post["location"] or p.location
            p.save()
        except:
            return HttpResponse("failed", mimetype="application/json")
        return HttpResponse(json.dumps("success"), mimetype="application/json")
    
    @login_required 
    def do_PUT(self):
        '''
        THIS METHOD WILL NOT BE IMPLEMENTED
        YOU CAN'T CREATE A USER BY AJAX
        http method: PUT
        '''
        raise HTTPError(405)
    
    @login_required  
    def do_DELETE(self):
        '''
        THIS METHOD WILL NOT BE IMPLEMENTED
        YOU CAN'T DELETE A USER BY AJAX
        http method: DELETE
        to delete a certain user
        @return: success or failed(a dictionary)
        '''
        raise HTTPError(405)
        '''
        u = get_object_or_404(User, pk=self.user_id)
        try:
            p = u.get_profile()
            p.delete()
            u.delete()
        except:
            return HttpResponse("failed", mimetype="application/json")
        return HttpResponse(json.dumps("success"), mimetype="application/json")
        '''
      
@login_required        
def index_tag(request):
    '''
    url:/core/tag/
    @return: the partial page of the reply
    '''
    return render_to_response('anno/reply.html')



@login_required
def get_tag_list_all(request):
    '''
    url:    /core/taglist/all
    http method: GET
    '''
    tags = Tag.objects.all()
    return HttpResponse(serializers.serialize("json", tags), mimetype="application/json")

@login_required
def get_tag_list_user(request, user_id=0):
    '''
    url:    /core/taglist/user/{user_id}
    http method: GET
    '''
    if user_id == 0:
        u = request.user
    else:
        u = User.objects.get(pk=user_id)
    tags = u.tag_set.all().order_by('pk')
    return HttpResponse(serializers.serialize("json", tags), mimetype="application/json")


class tag_detail:
    '''
    url:    /core/crud/{tag_id}
    restful interface of a certain tag
    '''
    def __call__(self, request, tag_id = 0):
        self.request, self.user, self.build_absolute_uri, self.get_full_path = \
            request, request.user, request.build_absolute_uri, request.get_full_path
        self.tag_id = tag_id
        try:
            callback = getattr(self, "do_%s" % request.method)
        except AttributeError:
            pass
        return callback()
    
    @login_required  
    def do_GET(self):
        '''
        http method: GET
        @return: a dictionary of a certain tag 
            type:    json
            list of a dic:    
            sample:  [{
                        "pk": 2, 
                        "model": "core.tag", 
                        "fields": {
                            "description": "tag2", 
                            "users": [2, 3]
                        }
                    }]
        '''
        t = get_object_or_404(Tag, pk=self.tag_id)
        return HttpResponse(serializers.serialize("json", [t]), mimetype="application/json")
    
    @login_required
    def do_POST(self):
        '''
        http method: POST
        to update a certain tag
        type:    json
        @param description:(optional)
        @param operation: update or add or delete(change the users)
        @param users: a list of user id (type json)(optional)
        @return: success or failed(a dictionary)
        '''
        t = get_object_or_404(Tag, pk=self.tag_id)
        post = json.loads(self.request.raw_post_data)
        try:
            t.description = post.has_key("description") and post["description"] \
                            or t.description
            operation = post.has_key("operation") and post["operation"] or None
            users_id = post.has_key("users") and post["users"] or None
            
            def convert_id(user_id):
                return User.objects.get(pk=user_id)
                
            if operation == "update":
                users = map(convert_id, users_id)
                t.users.clear()
                t.users.add(*users)
            elif operation == "add":
                users = map(convert_id, users_id)
                t.users.add(*users)
            elif operation == "delete":
                users = map(convert_id, users_id)
                t.users.remove(*users)
            t.save()
        except:
            return HttpResponse("failed", mimetype="application/json")
        return HttpResponse(json.dumps("success"), mimetype="application/json")
    
    @login_required 
    def do_PUT(self):
        '''
        http method: PUT
        to create a certain tag
        type:    json
        @param description:
        #@param users: a list of user id
        @return: tag.pk or failed(a dictionary)
        '''
        put = json.loads(self.request.raw_post_data)
        des = put["description"]
        des_f = Tag.objects.filter(description=des)
        if len(des_f):
            tag = des_f[0]
            return HttpResponse(json.dumps(tag.pk), mimetype="application/json")
        try:
            desc = put["description"]
            tag = Tag.objects.create(description=desc)
        except:
            return HttpResponse("failed", mimetype="application/json")
        return HttpResponse(json.dumps(tag.pk), mimetype="application/json")
    
    @login_required  
    def do_DELETE(self):
        '''
        http method: DELETE
        to delete a certain tag
        @return: success or failed(a dictionary)
        '''
        t = get_object_or_404(Tag, pk=self.tag_id)
        try:
            t.delete()
        except:
            return HttpResponse("failed", mimetype="application/json")
        return HttpResponse(json.dumps("success"), mimetype="application/json")
    
class usergroup_detail:
    '''
    url:    /core/usergroup/crud/{usergroup_id}
    restful interface of a certain usergroup
    '''
    def __call__(self, request, usergroup_id = 0):
        self.request, self.user, self.build_absolute_uri, self.get_full_path = \
            request, request.user, request.build_absolute_uri, request.get_full_path
        self.usergroup_id = usergroup_id
        try:
            callback = getattr(self, "do_%s" % request.method)
        except AttributeError:
            pass
        return callback()
    
    @login_required  
    def do_GET(self):
        '''
        http method: GET
        @return: a dictionary of a certain usergroup 
            type:    json
            list of a dic:    
            sample:   
        '''
        a = get_object_or_404(UserGroup, pk=self.usergroup_id)
        return HttpResponse(serializers.serialize("json", [a]), mimetype="application/json")
    
    @login_required
    def do_POST(self):
        '''
        http method: POST
        to update a certain usergroup
        type:    json
        @param description:   description of the usergroup (optional)
        @param operation: update or add or delete(change the users)
        @param users: a list of user id (type json)(optional)
        @return: success or failed(a dictionary)
        '''
        ug = get_object_or_404(UserGroup, pk=self.usergroup_id)
        post = json.loads(self.request.raw_post_data)
        try:
            ug.description = post.has_key("description") and post["description"] or ug.description
            operation = post.has_key("operation") and post["operation"] or None
            users_id = post.has_key("users") and post["users"] or None
            def convert_id(user_id):
                return User.objects.get(pk=user_id)
                
            if operation == "update":
                users = map(convert_id, users_id)
                ug.users.clear()
                ug.users.add(*users)
            elif operation == "add":
                users = map(convert_id, users_id)
                ug.users.add(*users)
            elif operation == "delete":
                users = map(convert_id, users_id)
                ug.users.remove(*users)
            ug.save()
        except:
            return HttpResponse("failed", mimetype="application/json")
        return HttpResponse(json.dumps("success"), mimetype="application/json")
    
    @login_required 
    def do_PUT(self):
        '''
        http method: PUT
        to create a certain usergroup
        type:    json
        @param description:    title of the usergroup 
        @return: id or failed(a dictionary)
        '''
        put = json.loads(self.request.raw_post_data)
        try:
            ug = self.user.groups_set.create(description=put["description"])  
        except:
            return HttpResponse("failed", mimetype="application/json")
        return HttpResponse(json.dumps(ug.pk), mimetype="application/json")

    @login_required  
    def do_DELETE(self):
        '''
        http method: DELETE
        to delete a certain usergroup
        @return: success or failed(a dictionary)
        '''
        t = get_object_or_404(UserGroup, pk=self.usergroup_id)
        try:
            t.delete()
        except:
            return HttpResponse("failed", mimetype="application/json")
        return HttpResponse(json.dumps("success"), mimetype="application/json")

@login_required    
def usergroup_popup(request):
    ugs = request.user.groups_set.all()
    return render_to_response('core/usergroup_popup.html', {
                                    'user'    :     request.user,
                                    'groups'  :     ugs,
                                })

@login_required    
def new_user_group(request):
    return render_to_response('core/usergroup_new_popup.html')


@login_required
def manage_user_group(request, usergroup_id):
    ug = get_object_or_404(UserGroup, pk=usergroup_id)
    users_in = ug.users.all()
    users_all = User.objects.all()
    users_not_in = []
    for u in users_all:
        if u not in users_in:
            users_not_in.append(u)
    return render_to_response('core/usergroup_manage_popup.html', {
                'user': request.user,
                'group' : ug,
                'users_in'    : users_in,
                'users_not_in' : users_not_in,
            })

@login_required
def upload(request):
    if request.method == 'GET':
        return render_to_response("core/manage_users_popup.html")
    else:
        file = request.FILES["file"]
        file_path = settings.STATIC_DIR + 'user_info/' + file.name
        destination = open(file_path, 'wb+')
        for chunk in file.chunks():
            destination.write(chunk)
        destination.close()
        import xlrd
        book = xlrd.open_workbook(file_path)
        sheet = book.sheets()[0]
        users = []
        for i in range(1, sheet.nrows):
            user = {
                'username'  : sheet.cell(i, 0).value,
                'password'  : sheet.cell(i, 1).value,
                'name'      : sheet.cell(i, 2).value,
                'mail'      : sheet.cell(i, 3).value,
                'nju_id'    : sheet.cell(i, 4).value,
                'grade'     : sheet.cell(i, 5).value,
                'group'     : sheet.cell(i, 6).value,
            }
            users.append(user)
        
        for user in users :
            u = User.objects.create_user(user["username"], user["mail"], user["password"])
            u.userprofile_set.create(name=user["name"], nju_id=user["nju_id"], grade=int(user["grade"]))
            group = Group.objects.get(name=user["group"])
            u.groups.add(group)
            u.save()
        return redirect("/")
    