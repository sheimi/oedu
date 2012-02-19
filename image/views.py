# Create your views here.
from Oedu import settings
from Oedu.core.models import UserGroup
from Oedu.image.models import ImageInfo
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.core import serializers
from django.http import HttpResponse
from django.shortcuts import render_to_response, get_object_or_404, redirect
import datetime
import json
import uuid

@login_required
def index(request, user_id=0):
    if user_id == 0 :
        rd = '/image/%d' % request.user.pk
        return redirect(rd)
    if int(user_id) == request.user.pk:
        images = request.user.imageinfo_set.filter(active=True)
        return render_to_response("image/index.html", {'user' : request.user,
                                                   'user_current' : request.user,
                                                   'images'       : images,
                                                   'now'          : "photo-gallery"})
    user = get_object_or_404(User, pk=user_id)
    groups = request.user.group_belong.filter(owner__pk=int(user_id))
    imgs = user.imageinfo_set.filter(active=True)
    images = []
    for img in imgs:
        gs = img.share_to.all()
        for g in groups:
            if g in gs:
                images.append(img)
                break
    return render_to_response("image/index.html", {'user' : request.user,
                                                   'user_current' : user,
                                                   'images'       : images,
                                                   'now'          : "photo-gallery"})

@login_required
def upload(request):
    if request.method == 'GET':
        return render_to_response("test/upload_plugin.html")
    else:
        file = request.FILES["file"]
        subfix = file.name.split('.')[-1]
        image_info = ImageInfo.objects.create(owner=request.user, active=True,
                                              upload_time=datetime.datetime.now())
        path = 'images/photo_lib/' + str(image_info.pk) + '.' + subfix
        file_path = settings.STATIC_DIR + path
        image_info.path = path
        image_info.save()
        destination = open(file_path, 'wb+')
        for chunk in file.chunks():
            destination.write(chunk)
        destination.close()
        return HttpResponse(serializers.serialize("json", [image_info]), mimetype="application/json")

@login_required    
def delete(request, image_id):
    image_info = get_object_or_404(ImageInfo, pk=image_id)
    image_info.active = False
    image_info.save()
    return HttpResponse(json.dumps("success"))

@login_required
def set_share_json(request, image_id):
    '''
    http method: POST
    type:    json
    @param operation: update or add or delete(change the users)
    @param groups: a list of group id (type json)
    @return: success or failed(a dictionary)
    '''
    
    image_info = get_object_or_404(ImageInfo, pk=image_id)
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
            image_info.share_to.clear()
            if groups:
                image_info.share_to.add(*groups)
        elif operation == "add":
            image_info.share_to.add(*groups)
        elif operation == "delete":
            image_info.share_to.remove(*groups)
        image_info.save()
    except:
        return HttpResponse("failed", mimetype="application/json")
    return HttpResponse(json.dumps("success"), mimetype="application/json")

@login_required
def set_share_popup(request, image_id):
    image_info = get_object_or_404(ImageInfo, pk=image_id)
    shared = image_info.share_to.all()
    shared_id = [shared_s.pk for shared_s in shared]
    all = request.user.groups_set.all()
    not_shared = []
    for g in all:
        if g.id not in shared_id:
            not_shared.append(g)
    return render_to_response("image/share_popup.html", {'user' : request.user, 
                                                         'image_info' : image_info,
                                                         'not_shared' : not_shared,})

def active_all(request):
    images = ImageInfo.objects.filter(active=False)
    for image in images:
        image.active = True
        image.save()
    return HttpResponse(json.dumps("success"))