# -*- coding: utf-8 -*-

from django.shortcuts import render, redirect
from django.http import HttpResponse, Http404, JsonResponse
from django.utils import timezone
from django.views.decorators.cache import cache_page
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.clickjacking import xframe_options_exempt
#from django.core.urlresolvers import reverse
from django.urls import reverse
from datetime import datetime
from time import sleep, time
import pytz
import requests
#
from .models import Bookinfo, Bookprice, Store, Post
from get_proxy import get_proxy
from get_bookinfo import get_bookinfo
from get_bookprice import get_bookprice
from get_searchBooks import get_searchBooks
from get_biggoKW import get_biggoKW
from get_tpml import get_tpml
from get_hybook import get_hybook
from dict_stores import url_qs, store_names, store_urls
#
from threading import Thread
from concurrent.futures import ThreadPoolExecutor, ProcessPoolExecutor
import json

# 處理首頁


def wtb_index(request):
    #stores = Store.objects.all().order_by('code')
    stores = Store.objects.filter(enable='Y').order_by('code')
    stores_count = stores.count()
    #
    return render(request, 'wtb_index.html', locals())


# 處理單書頁
def wtb_book(request, bookid='0010829817'):
    start_time = time()
    #
    jsonstr = ""
    book = {'info': None, 'price': None, 'time': None}
    #
    snames = store_names
    surls = store_urls
    #
    stores = list(url_qs.keys())  # 不爬博客來，其餘的店家
    n = len(stores)
    bookids = [bookid]*n
    isbns = ['']*n
    tryDBs = [False]*n
    ippos = get_proxy(which='OK', now=True, sample=True, sampleN=n)
    # return HttpResponse(ippos)
    #
    bookinfo = get_bookinfo(bookid, tryDB=True)
    middle_time = time()
    #
    if not bookinfo['err']:
        # (1)檢查更新時間，超過一天就全部重爬
        tw = pytz.timezone('Asia/Taipei')
        delta = timezone.now().astimezone(tw).date() - \
            bookinfo['create_dt'].date()
        if delta.days != 0:
            # 更新bookinfo
            bookinfo = get_bookinfo(bookid, tryDB=False)
            # Bookinfo.objects.filter(bookid=bookid).first()
            row = bookinfo['row']
            rows = [row]*n
            # 更新bookprice_用多執行緒
            with ThreadPoolExecutor(max_workers=n) as executor:
                bookprice_all = [bookprice for bookprice in executor.map(
                    get_bookprice, bookids, isbns, stores, tryDBs, ippos, rows)]
        else:
            bookprice_all = Bookprice.objects.filter(bookid=bookid)
            # 筆數不對也重爬
            if bookprice_all.count() < n:
                # Bookinfo.objects.filter(bookid=bookid).first()
                row = bookinfo['row']
                rows = [row]*n
                with ThreadPoolExecutor(max_workers=n) as executor:
                    bookprice_all = [bookprice for bookprice in executor.map(
                        get_bookprice, bookids, isbns, stores, tryDBs, ippos, rows)]
        # (2)整理
        book['info'] = bookinfo
        book['price'] = bookprice_all
        # book['delta']=delta.days
        #
    #
    end_time = time()
    # _{middle_time-start_time:.5f}'
    book['time'] = f'{end_time-start_time:.5f}'
    #
    if bookinfo['err']:
        book['err'] = bookinfo['err']
        # datetime物件要用default=str處理。ascii要False，避免\uxxxx的unicode表示
        jsonstr = json.dumps(book, default=str, ensure_ascii=False)
        return HttpResponse(jsonstr)
    else:
        return render(request, 'wtb_book.html', locals())

# 搜尋結果
@cache_page(60*60*24*3)
def wtb_search(request):
    kw = request.GET['kw']
    jsonstr = get_searchBooks(kw, which='OK', now=True)
    #
    return HttpResponse(jsonstr)

# 推薦關鍵字
@cache_page(60*60*24*3)
def wtb_autocom(request):
    kw = request.GET['kw']
    jsonstr = get_biggoKW(kw, which='OK', now=True)
    #
    return HttpResponse(jsonstr)


def kobo(request):
    return render(request, 'kobo100.html', {})

# ============================================================
# FastApi
def openapijson(request):
    url='http://0.0.0.0:5001/openapi.json'
    r = requests.get(url)
    r.encoding = 'utf-8'
    res = r.json()
    res = json.dumps(res, default=str, ensure_ascii=False)
    res = res.replace('/pig/','/fastapi/pig/')
    res = res.replace('/pig_m/','/fastapi/pig_m/')
    res = res.replace('/pig_y/','/fastapi/pig_y/')
    return HttpResponse(res)
@xframe_options_exempt    
def fastdoc(request):
    url='http://0.0.0.0:5001/docs'
    r = requests.get(url)
    r.encoding = 'utf-8'
    rtext = r.text.replace('/openapi.json','https://wtb.wtbwtb.tk/fastapi/openapijson/')
    return HttpResponse(rtext)
#     return HttpResponse(f'<iframe src={url}></iframe>')
def fasttest(request):
    url='http://0.0.0.0:5001/test'
    r = requests.get(url)
    r.encoding = 'utf-8'
    res = json.dumps(r.json(), default=str, ensure_ascii=False)
    return HttpResponse(res)    

@csrf_exempt
def pig(request):
    url='http://0.0.0.0:5001/pig/'
    # (1)無指定時，ajax的request.body是application/x-www-form-urlencoded，FormData
    # 　　request.body是sd=2021-01-07&ed=2021-01-07
    # (2)fastapi的doc頁面按執行，post資料是Content-Type: application/json
    # 　　request.body是{"sd":"2021-01-01","ed":"2021-01-05"}
    # (3) 前者django用request.POST變成dict，後者要用json.loads(request.body)
    # post = request.is_ajax() and request.POST or json.loads(request.body)　# request.is_ajax() html在桌機直接執行時，為False，放到web為True
    post = request.POST or json.loads(request.body)
    postdata = {
        'sd': post.get('sd', '2020-12-01'),
        'ed': post.get('ed', '2020-12-03'),
    }
    r = requests.post(url, json=postdata) # fastapi用BaseModel，要送json
    r.encoding = 'utf-8'    
    res = r.json()
    r.close()
    # Access-Control-Allow-Origin
#     response = HttpResponse(json.dumps(res, indent=4, ensure_ascii=False))
#     response = HttpResponse(r.text)
    response = JsonResponse(res)
    response["Access-Control-Allow-Origin"] = "*"
    response["Access-Control-Allow-Methods"] = "POST, GET, OPTIONS"
    response["Access-Control-Max-Age"] = "1000"
    response["Access-Control-Allow-Headers"] = "X-Requested-With, Content-Type"
#     if res.get('error'):
#         response.status_code = 400
    return response

def pig_m(request):
    url='http://0.0.0.0:5001/pig_m/'
    getdata = {
        'sd': request.GET.get('sd', '2020-12'),
        'ed': request.GET.get('ed', '2020-12'),
    }
    r = requests.get(url, params=getdata)
    r.encoding = 'utf-8'
    res = r.json()
    r.close()    
    #     
    response = HttpResponse(json.dumps(res, indent=4, ensure_ascii=False))
    response["Access-Control-Allow-Origin"] = "*"
    response["Access-Control-Allow-Methods"] = "POST, GET, OPTIONS"
    response["Access-Control-Max-Age"] = "1000"
    response["Access-Control-Allow-Headers"] = "X-Requested-With, Content-Type"    
    return response

def pig_y(request):
    url='http://0.0.0.0:5001/pig_y/'
    getdata = {
        'sd': request.GET.get('sd', '2020'),
        'ed': request.GET.get('ed', '2020'),
    }
    r = requests.get(url, params=getdata)
    r.encoding = 'utf-8'
    res = r.json()
    r.close()    
    #     
    response = HttpResponse(json.dumps(res, indent=4, ensure_ascii=False))
    response["Access-Control-Allow-Origin"] = "*"
    response["Access-Control-Allow-Methods"] = "POST, GET, OPTIONS"
    response["Access-Control-Max-Age"] = "1000"
    response["Access-Control-Allow-Headers"] = "X-Requested-With, Content-Type"    
    return response

# 北市圖
def wtb_tpml(request):
    isbn = request.GET['isbn']
    ans = get_tpml(isbn)
    return HttpResponse(ans)

# 曉園_http://www.hybook.com.tw/search.asp?page=12


def wtb_hybook(request, page):
    s = time()
    rows = get_hybook(page)
    e = time()
    ans = f'第{page}頁(花{e-s}秒)<br>'+'<br>'.join(rows)
    #
    return HttpResponse(ans)

def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return HttpResponse(ip)

def homepage(request, test):
    posts = Post.objects.all()
    #now = datetime.now()
    tv = {'name': 'wed'}
    if test:
        return HttpResponse('test')
    else:
        return HttpResponse('...')
    # return render(request, 'index.html', locals())


def homepage_1(request, AAA):
    posts = Post.objects.all()
    post_list = []
    for c, post in enumerate(posts):
        post_list.append(f"No.{str(c)+': '+str(post)+'<br>'}")
        post_list.append("<h1>"+post.body+"</h1>")
    #
    a = '''
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
    # return HttpResponse(post_list)
    b = str(123)
    return HttpResponse(AAA)


def homepage_2(request, AAA, BBB):
    # a=reverse('test-url',args=('swsw','%%@@@'))
    # return HttpResponse('<a href='+a+'>dede</a>')
    posts = Post.objects.all()
    now = datetime.now()
    tv = {'name': 'wed', 'price': 87654321.12345}
    return render(request, 'index.html', locals())


def showpost(request, slug):
    try:
        now = datetime.now()
        post = Post.objects.get(slug=slug)
        if post:
            return render(request, 'post.html', locals())
    except:
        return redirect('/index')


def showpost_1(request, slug):
    try:
        #now = datetime.now()
        post = Post.objects.get(slug=slug)
    except Post.DoesNotExist:
        # return redirect('/index')
        raise Http404("找不到_"+slug)
    return redirect('/index')
