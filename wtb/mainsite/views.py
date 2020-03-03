# -*- coding: utf-8 -*- 

from django.shortcuts import render, redirect
from django.http import HttpResponse, Http404
#from django.core.urlresolvers import reverse
from django.urls import reverse
from datetime import datetime
from time import sleep, time
from .models import Store,Post
from get_bookinfo import get_bookinfo
from get_bookprice import get_bookprice
from threading import Thread
from concurrent.futures import ThreadPoolExecutor,ProcessPoolExecutor 
import json

# 處理首頁 
def wtb_index(request):
    stores = Store.objects.all().order_by('code')
    stores_count=stores.count()
    #
    return render(request, 'wtb_index.html', locals())


# 處理單書頁
def wtb_book(request,bookid='0010829817'):
    start_time = time()
    jsonstr=""
    book={'time':'0'}
    #
    bookinfo=get_bookinfo(bookid,tryDB=True)
    if not bookinfo['err']:
        book={'info':bookinfo,'price':[]} 
        #
        #用多執行緒____________________________        
        stores=['elite','ks']
        n=len(stores)
        bookids=[bookid]*n
        isbns=['']*n        
        tryDBs=[False]*n
        #
        with ThreadPoolExecutor(max_workers=n) as executor:
            for bookprice in executor.map(get_bookprice,bookids,isbns,stores,tryDBs):
                book['price'].append(bookprice)

        #threads = []
        #for store in stores:
        #    thread = Thread(target=get_bookprice, args=(bookid,'',store,False))
        #    threads.append(thread)
        #    thread.start()
        #for thread in threads:
        #    thread.join()        
        
    #
    end_time = time()
    book['time']=f'{end_time-start_time:.5f}'
    #datetime物件要用default=str處理。ascii要False，避免\uxxxx的unicode表示
    jsonstr=json.dumps(book,default=str,ensure_ascii=False)
    return HttpResponse(jsonstr)





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


