#%load get_bookinfo.py
#%run get_bookinfo.py
# -*- coding: utf-8 -*-
#_____________________tt
import os
import django
from django.utils import timezone
from bs4 import BeautifulSoup
from bs4.element import NavigableString
from difflib import SequenceMatcher
from IPython.display import clear_output, display
from time import sleep, time
from threading import Thread
from fake_useragent import UserAgent
from fake_headers import Headers
from pyquery import PyQuery as pq
#
import requests
import pandas as pd
import numpy as np
import random
import re
import json
import csv
#
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'wtb.settings')
os.environ["DJANGO_ALLOW_ASYNC_UNSAFE"] = "true"
django.setup()
from mainsite.models import Bookinfo,Store,Post
#__________________________
#stores = Store.objects.all().order_by('code')
#for s in stores:
#    print(s.name) 
    
#p = Post.objects.create(AA='55',title='dede',slug='S7',body='dede',pub_date=timezone.now())
#p.save()
#
def get_bookinfo(bookid,tryDB=True):
    
    bookinfo={'err':'','bookid':bookid}
    
    #1.確認是否10位數字串
    if type(bookid) is not str or len(bookid)!=10:
        bookinfo['err']='bookid有誤'
        return bookinfo
    
    #2.DB: 確認bookinfo表是否已有資料=======================
    if tryDB:
        row=Bookinfo.objects.filter(bookid=bookid)
        if row:
            bookinfo['tryDB']=tryDB
            bookinfo['fromDB']=True
            bookinfo['create']=None
            bookinfo.update(row.values()[0])        
            return bookinfo
    
    #3.Web: 沒有才從博客來抓===============================
    url_q="https://www.books.com.tw/products/"+bookid
    fake_header = Headers(
        browser="chrome",  # Generate only Chrome UA
        os="win",  # Generate ony Windows platform
        headers=True  # generate misc headers
    )    
    UA=fake_header.generate()
    #
    try:        
        r = requests.get(url_q, 
                         headers=UA,
                         #proxies=proxies,
                         #cookies=cookies,
                         timeout=3)    
        r.encoding='utf8'
        htmlstr=r.text
        doc=pq(htmlstr)
        #________________例外收集________________________________                    
        #(1)頁面連結錯誤        
        msg_info=doc.find("h2.msg_info").eq(0).text()
        if '錯誤' in msg_info:
            raise Exception('notfound')
  
        #(2)只抓有isbn的        
        isbn=doc.find(".mod_b.type02_m058.clearfix .bd").find("ul").eq(0).find("li").eq(0).text()
        if 'ISBN' not in isbn:
            raise Exception('noisbn')
            
        #________________info收集________________________________
        #ISBN
        isbn=isbn.replace("ISBN：","")
        #書名
        title=doc.find(".mod.type02_p002.clearfix > h1").text()
        tmp=doc.find(".type02_p003.clearfix").find("ul").eq(0)
        #作者
        author=tmp.find("li").eq(0).find("a[href*='adv_author']").text()
        #出版社
        publisher=tmp.find("a[href*='sys_puballb']").text()
        #封面
        url_cover=doc.find(".cover_img > img.cover").attr("src")

        #
    except Exception as e:
    #except requests.exception.Timeout as e:
        #有任何例外，紀錄error
        error=str(e)
        if 'timeout' in error:
            bookinfo['err']='timeout'
        else:    
            bookinfo['err']=error[:50]            
    else:
        #
        bookinfo['isbn']=isbn
        bookinfo['title']=title
        bookinfo['author']=author
        bookinfo['publisher']=publisher  
        bookinfo['url_cover']=url_cover  
        
    finally:
        #爬成功或失敗，都存DB
        #row = Bookinfo.objects.create(**bookinfo)
        #row.save()   
        #增加tryDB選擇，直接爬可能update
        row, create = Bookinfo.objects.update_or_create(bookid=bookid,defaults=bookinfo)          
        #
        bookinfo['tryDB']=tryDB
        bookinfo['fromDB']=False
        bookinfo['create']=create
        return bookinfo
        #
            
