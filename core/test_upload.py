'''
Created on May 25, 2011

@author: zhangsheimi
'''
from django.http import HttpResponse
from django.shortcuts import render_to_response
  
def upload_image_test(request):
    if request.method == 'GET':
        return render_to_response("test/index.html")
    else:
        file = request.FILES["file"]
        file_path = file.name
        destination = open(file_path, 'wb+')
        for chunk in file.chunks():
            destination.write(chunk)
        destination.close()
        return HttpResponse("success")
    
def upload_drop_test(request):
    return render_to_response("test/upload_plugin.html")

def parse_xls(file_path):
    pass

def parse_xlsx(file_path):
    pass