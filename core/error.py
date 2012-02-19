'''
Created on Apr 19, 2011

@author: zhangsheimi
'''

from django.shortcuts import render_to_response

def error(message):
    return render_to_response('error.html', {'message' : message, 'color_theme' : 'energy'})
    
def oops404(response):
    return error('404')