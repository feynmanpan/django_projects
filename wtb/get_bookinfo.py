#%load get_bookinfo.py
#%run get_bookinfo.py
# -*- coding: utf-8 -*-
#_____________________
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
def get_bookinfo(bookid):
    bookid=bookid
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
        #________________________________________________
        #result=BeautifulSoup(r.text,"lxml")    
        #print(htmlstr)
        bookinfo={}
        doc=pq(htmlstr)
        isbn=doc.find(".mod_b.type02_m058.clearfix .bd").find("ul").eq(0).find("li").eq(0).text()
        #只抓有isbn的
        if 'ISBN' not in isbn:
            print('noisbn')
            return None
        else:
            isbn=isbn.replace("ISBN：","")
        #
        title=doc.find(".mod.type02_p002.clearfix > h1").text()
        tmp=doc.find(".type02_p003.clearfix").find("ul").eq(0)
        author=tmp.find("li").eq(0).find("a[href*='adv_author']").text()
        publisher=tmp.find("a[href*='sys_puballb']").text()
        
        #________________________________________________
        bookinfo['bookid']=bookid
        bookinfo['isbn']=isbn
        bookinfo['title']=title
        bookinfo['author']=author
        bookinfo['publisher']=publisher
        #
        return bookinfo
    except:
        print('NG')
        return None
