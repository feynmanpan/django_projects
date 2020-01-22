# -*- coding: utf-8 -*- 

from django.shortcuts import render, redirect
from django.http import HttpResponse, Http404
#from django.core.urlresolvers import reverse
from django.urls import reverse
from datetime import datetime
from .models import Post

# Create your views here.
def homepage(request):
    posts = Post.objects.all()
    #now = datetime.now()
    tv={'name':'wed'}
    return render(request, 'index.html', locals())

def homepage_1(request,AAA):
    posts = Post.objects.all()
    post_list=[]
    for c,post in enumerate(posts):
        post_list.append(f"No.{str(c)+': '+str(post)+'<br>'}")
        post_list.append("<h1>"+post.body+"</h1>")
    #
    a='''
    <style>
        
        .rwd{
            width:auto;height:auto;color:red;border:1px solid red;font-size:22px;
        }
    @media (max-width:970px){
        
        .rwd{
            width:60%; 
        }
    }
    </style>
    
    <html>
    <head>
     <meta name="viewport" content="width=device-width, min-scale=1, initial-scale=1, maximum-scale=1, user-scalable=no ,shrink-to-fit=no" />
    </head>
    <body>
    <p style="font-size: 22px">我</p> 
    <img class='rwd' src='https://www.taaze.tw//new_ec/rwd/include/images/sell_image/pic/pic_486x320_a.jpg'>
    <img class='rwd' src='https://www.taaze.tw//new_ec/rwd/include/images/sell_image/pic/pic_486x320_a.jpg'>
    </body>
    <script>//alert(screen.width);alert(window.innerWidth);</script>
    </html>
    '''
    #return HttpResponse(post_list) 
    b=str(123)
    return HttpResponse(AAA)

def homepage_2(request,AAA,BBB):
    #a=reverse('test-url',args=('swsw','%%@@@'))
    #return HttpResponse('<a href='+a+'>dede</a>')
    posts = Post.objects.all()
    now = datetime.now()
    tv={'name':'wed','price':87654321.12345}    
    return render(request, 'index.html', locals())
    
    
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


