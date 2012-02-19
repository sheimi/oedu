# Create your views here.
from Oedu.core.models import Tag, UserProfile
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.core import serializers
from django.http import HttpResponse
from django.shortcuts import render_to_response, get_object_or_404, redirect

@login_required
def index(request):
    query = request.GET.get('query', None)
    if not query:
        return redirect("/search/general")
    qs = query.split(' ')
    query_str = ''
    for q in qs:
        if q[0:3] == 'gpa':
            query_str += 'gpa=' + q +'&'
        else:
            query_str += 'realname=' +  q + '&'
    tag = query.split('&')[-1]
    if tag == 'tag':
        query_str += "type=tag&"
    return redirect("/search/general?"+query_str[0:(len(query_str)-1)])

@login_required
def search_general(request):
    realname = request.GET.get('realname', '')
    gpa = request.GET.get('gpa', '')
    tag = request.GET.get('type', '')
    query = realname + " " + gpa
    return render_to_response("search/search_general.html", {'realname' : realname, 'gpa' : gpa, "query" : query, "tag": tag})

@login_required
def search_tag(request):
    '''
    url:        /search/tag
    method:    GET
    @param name: a part of the tag name
    '''
    name = request.GET.get("name", "")
    tags = Tag.objects.all()
    if name :
        tags = Tag.objects.filter(description__icontains=name)
    return HttpResponse(serializers.serialize("json", tags), mimetype="application/json")

@login_required
def search_user_all(request):
    '''
    url: /serach/user/all
    method: GET
    '''
    users = User.objects.all()
    return HttpResponse(serializers.serialize("json", users), mimetype="application/json")

@login_required
def search_user_info(request):
    '''
    url:    /search/user_info
    method: GET
    @param  username:
    @param realname: 
    @param group:
    '''    
    realname = request.GET.get('realname', None)
    gpa = request.GET.get('gpa', None)
    profiles = UserProfile.objects.all()
    if realname :
        profiles = profiles.filter(name__icontains=realname)
    if gpa :
        op = gpa[3]
        gpa = float(gpa[4:])
        render = []
        for profile in profiles:
            g = profile.user.cal_gpa()
            if op == '>' and g > gpa:
                render.append(profile)
            elif op == '<' and g < gpa:
                render.append(profile)
        profiles = render
    return HttpResponse(serializers.serialize("json", profiles), mimetype="application/json")

@login_required
def search_user(request):
    '''
    url:    /search/user
    method: GET
    @param  username:
    @param realname: 
    @param group:
    '''
    username = request.GET.get('username', None)
    if username :
        users = User.objects.filter(username__icontains=username)
        return HttpResponse(serializers.serialize("json", users), mimetype="application/json")
    realname = request.GET.get('realname', None)
    if realname :
        profiles = UserProfile.objects.filter(name__icontains=realname)
        users = [p.user for p in profiles]        
        return HttpResponse(serializers.serialize("json", users), mimetype="application/json")
    group = request.GET.get('group', None)
    if group:
        users = User.objects.all()
        us = []
        for u in users:
            groupnames = u.groupnames()
            for groupname in groupnames :
                if (groupname == group):
                    us.append(u)
        return HttpResponse(serializers.serialize("json", us), mimetype="application/json")

        
@login_required
def get_users_by_tag(request, tag_id):
    '''
    url:    /search/user/tag/{tag_id}
    method: GET
    '''
    tag = get_object_or_404(Tag, pk=tag_id)
    users = tag.users.all()
    if request.is_ajax() :
        return HttpResponse(serializers.serialize("json", users), mimetype="application/json")
    else:
        return render_to_response("search/get_users_by_tag.html", {
                                                            "users" : users,
                                                            "user"  : request.user,
                                                            })

@login_required
def search_usergroup(request):
    '''
    url:    /search/usergroup
    method: GET
    @param name: 
    '''
    name = request.GET.get("name", "")
    ugs = request.user.groups_set.all()
    if name :
        ugs = ugs.filter(description__icontains=name)
    return HttpResponse(serializers.serialize("json", ugs), mimetype="application/json")