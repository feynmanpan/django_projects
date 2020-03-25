#%load get_bookinfo.py
#%run get_bookinfo.py
# -*- coding: utf-8 -*-
#________________________________________________
import os
import django
from django.utils import timezone
#from django.utils.dateparse import parse_datetime
from datetime import datetime,date#,timezone
import pytz
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
import isbnlib
import requests
import pandas as pd
import numpy as np
import random
import re
import json
import csv
#
from get_proxy import get_proxy
from get_isbn_from_elite import get_isbn_from_elite
#
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'wtb.settings')
os.environ["DJANGO_ALLOW_ASYNC_UNSAFE"] = "true"
django.setup()
from mainsite.models import Bookinfo,Bookprice,Store
#________________________________________________

def get_bookinfo(bookid:str,tryDB=True)->dict:

    bookinfo={'err':'','bookid':bookid}
    tw = pytz.timezone('Asia/Taipei')
    
    #1.確認是否10位數字串
    if type(bookid) is not str or len(bookid)!=10:
        bookinfo['err']='wrongbookid'
        return bookinfo
    
    #2.DB: 確認bookinfo表是否已有資料=======================
    if tryDB:
        row=Bookinfo.objects.filter(bookid=bookid)
        if row.count()==1:
            bookinfo.update(row.values()[0])        
            bookinfo['tryDB']=tryDB
            bookinfo['fromDB']=True
            bookinfo['create']=None   
            #回傳顯示CST台北時間
            bookinfo['create_dt']=bookinfo['create_dt'].astimezone(tw)     
            #
            return bookinfo
    
    #3.Web: 沒有才從博客來抓===============================
    url_q="https://www.books.com.tw/products/"+bookid
    fake_header = Headers(
        browser="chrome",  # Generate only Chrome UA
        os="win",  # Generate ony Windows platform
        headers=True  # generate misc headers
    )    
    UA=fake_header.generate()
    ippo=get_proxy(which="OK",now=True)
    #ippo="103.236.114.38:49638"
    proxies={
            "http": "http://"+ippo,
            #"https": "http://"+ippo  #https有問題
            }
    #
    try:        
        r = requests.get(url_q, 
                         headers=UA,
                         proxies=proxies,
                         #cookies=cookies,
                         timeout=30)    
        r.encoding='utf8'
        #
        #print(r.text)
        doc=pq(r.text)
        r.close()
        #________________例外收集________________________________                            
        #(0)狀態碼400~599        
        if r.status_code != 200:
            #print(r.raise_for_status())
            #print(r.status_code)
            raise Exception(r.status_code)
            
        #(1)404頁面連結錯誤        
        msg_info=doc.find("h2.msg_info").eq(0).text()
        if '錯誤' in msg_info:
            raise Exception('notfound')
  
        #(2)只抓有isbn的，博客來有時完全沒有isbn，如刺蝟的優雅十周年版
        isbn=doc.find(".mod_b.type02_m058.clearfix .bd").find("ul").eq(0).find("li").eq(0).text() or ''
        isbn13=''
        if 'ISBN' not in isbn:# or (len(isbn.replace("ISBN：",""))==10 and not isbnlib.to_isbn13(isbn)):
            title=doc.find(".mod.type02_p002.clearfix > h1").text()
            isbns=get_isbn_from_elite(title)
            if not isbns:
                raise Exception('noisbn')
            isbn=isbns[0]
            isbn13=isbns[1]
            
        #________________info收集________________________________
        #ISBN
        isbn=isbn.replace("ISBN：","")
        if len(isbn)==10 and not isbn13:
            isbn13=isbnlib.to_isbn13(isbn) or '' #0010847679轉不出13碼_Column 'isbn13' cannot be null
        #書名
        title=doc.find(".mod.type02_p002.clearfix > h1").text()
        title2=doc.find(".mod.type02_p002.clearfix > h2").text() or ''
        #=========================
        tmp=doc.find(".type02_p003.clearfix").find("ul").eq(0)
        #--作者/原文作者/譯者
        #author=tmp.find("li").eq(0).find("a[href*='adv_author']").text()
        authors=tmp.find("li").find("a[href*='adv_author']")
        author=''
        for au in authors:
            if '作者' in pq(au).parent().text() and '原文作者' not in pq(au).parent().text():
                author+='作者：'+pq(au).text()+"/"
                continue
            if '原文作者' in pq(au).parent().text():
                author+='原文作者：'+pq(au).text()+"/"                
                continue
            if '譯者' in pq(au).parent().text():
                author+='譯者：'+pq(au).text()+"/"                
                continue
            if '編者' in pq(au).parent().text():
                author+='編者：'+pq(au).text()+"/"                
                continue                
        #
        author=author.rstrip('/')
        #--出版社
        publisher=tmp.find("a[href*='sys_puballb']").text() or ''
        #--原文出版社
        if not publisher:
            publisher=tmp.find("li:Contains('原文出版社')").text().replace('原文出版社：','').strip() or ''        
        #--出版日期YYYY-MM-DD，字串轉存datetime物件
        pub_dt=tmp.find("li:Contains('出版日期')").text().replace('出版日期：','').replace('/','-')
        pub_dt=datetime.strptime(pub_dt, "%Y-%m-%d").date()
        #--語言
        lang=tmp.find("li:Contains('語言')").text().replace('語言：','').strip()
        #--定價
        tmp2=doc.find(".cnt_prod002.clearfix ul.price").eq(0)
        price_list=tmp2.find("em").text()
        price_sale=tmp2.find("strong.price01").eq(-1).find("b").text() #有優惠價跟特價，要找最後一個
        if not price_list:
            price_list=price_sale
        #--電子書
        tmp3=doc.find("#li_M201106_0_getEbkRitems_P00a400020119-0")
        if tmp3.find("a span").eq(0).text()=="電子書":
            price_sale_ebook=tmp3.find(".price em").text() or ''
            bookid_ebook=tmp3.find("a").attr("href") or ''
            bookid_ebook=bookid_ebook.replace("https://www.books.com.tw/products/","")
        #=========================
        #規格
        spec=doc.find(".mod_b.type02_m058.clearfix .bd li:Contains('規格')").text().replace(" ","").replace("規格：","")
        #簡介
        intro=doc.find(".bd .content").eq(0).html() or ''
        #YT影片
        url_vdo=doc.find('.cont iframe').eq(0).attr('src') or ''
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
        #失敗不存出版日期
        bookinfo['pub_dt']=None    
    else:
        #
        cols=['isbn','isbn13','title','title2','author','publisher',
              'pub_dt','lang','price_list','price_sale','price_sale_ebook','bookid_ebook',
              'spec','intro','url_vdo','url_cover']
        #
        for col in cols:
            bookinfo[col]=locals().get(col,'')
        
    finally:
        #(1)爬成功或失敗，都存DB
        bookinfo['create_dt']=timezone.now() #django timezone會抓OS的UTC時間
        row, create = Bookinfo.objects.update_or_create(bookid=bookid,defaults=bookinfo)          
        #(2)整理回傳
        bookinfo['tryDB']=tryDB
        bookinfo['fromDB']=False
        bookinfo['create']=create
        #回傳顯示CST台北時間
        bookinfo['create_dt']=bookinfo['create_dt'].astimezone(tw)
        #
        return bookinfo
        #return json.dumps(bookinfo,default=str,ensure_ascii=False)
        #
