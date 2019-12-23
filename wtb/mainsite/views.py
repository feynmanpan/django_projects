# -*- coding: utf-8 -*- 

from django.shortcuts import render, redirect
from django.http import HttpResponse, Http404
from datetime import datetime
from .models import Post

# Create your views here.
def homepage(request):
    posts = Post.objects.all()
    #now = datetime.now()
    return render(request, 'index.html', locals())

def homepage_1(request):
    posts = Post.objects.all()
    post_list=[]
    for c,post in enumerate(posts):
        post_list.append(f"No.{str(c)+': '+str(post)+'<br>'}")
        post_list.append("<h1>"+post.body+"</h1>")
    #
    #return HttpResponse(post_list) 
    return HttpResponse(["<h1>222","我</h1>"])
    
def showpost(request, slug):
    try:
        now = datetime.now()
        post = Post.objects.get(slug = slug)
        if post:
            return render(request, 'post.html', locals())
    except:
        return redirect('/index')    
    
def showpost_1(request, slug):
    try:
        #now = datetime.now()
        post = Post.objects.get(slug = slug)
    except Post.DoesNotExist:
        #return redirect('/index')            
        raise Http404("找不到_"+slug)
    return redirect('/index')        


