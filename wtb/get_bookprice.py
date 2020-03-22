#%load get_bookprice.py
#%run get_bookprice.py
# -*- coding: utf-8 -*-
#________________________________________________
import os
import django
from django.utils import timezone
from django.db.models import Q
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
from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.keys import Keys
#
import requests
import urllib.parse
import pandas as pd
import numpy as np
import random
import re
import json
import csv
#
from get_proxy import get_proxy
from get_mollie import get_mollie
#
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'wtb.settings')
os.environ["DJANGO_ALLOW_ASYNC_UNSAFE"] = "true"
django.setup()
from mainsite.models import Bookinfo,Bookprice,Store
from dict_stores import url_qs

#________________________________________________

def get_bookprice(bookid:str='',isbn:str='',store:str='',tryDB=True)->dict:
    
    bookprice={'err':'','bookid':bookid,'isbn':isbn,'isbn13':'','store':store}
    tw = pytz.timezone('Asia/Taipei')
    #用匯入的
    #url_qs={
    #    'elite':"http://www.eslite.com/Search_BW.aspx?searchType=&query=",
    #    'ks':"https://www.kingstone.com.tw/search/search?q=",
        #'momo':"https://www.momoshop.com.tw/search/searchShop.jsp?keyword="
        #momo用手機板查
    #    'momo':"https://m.momoshop.com.tw/search.momo?searchKeyword="
    #}
    
    
    #1.確認====================================
    #(0)一定要指定店家
    if not store:
        bookprice['err']='nostore'
        return bookprice
    if store not in url_qs:
        bookprice['err']='nosuchstore'
        return bookprice
        
    #(1)bookid跟isbn至少要有一個
    if not bookid and not isbn:
        bookprice['err']='nobookidisbn'
        return bookprice
    #(2)更新bookid及isbn
    if bookid:
        if type(bookid) is not str or len(bookid)!=10:
            bookprice['err']='wrongbookid'
            return bookprice 
        #以重查的isbn為準
        row=Bookinfo.objects.filter(bookid=bookid)
        if row.count()==1:
            bookprice['bookid']=row.first() #要使用instance，update_or_create才能存           
            bookprice['isbn']=row.first().isbn
            bookprice['isbn13']=row.first().isbn13
            isbn=row.first().isbn            
            isbn13=row.first().isbn13            
        else:
            bookprice['err']='nosuchbookid'
            return bookprice 
    else:
        #沒bookid，就一定要用isbn重查
        row=Bookinfo.objects.filter(isbn=isbn)
        if row.count()==1:        
            bookprice['bookid']=row.first() #要使用instance，update_or_create才能存       
            bookid=row.first().bookid  
        else:
            bookprice['err']='nosuchisbn'
            return bookprice        
            
    #2.DB: 確認bookprice表是否已有資料=======================
    if tryDB:
        row=Bookprice.objects.filter(bookid=bookid,store=store)
        if row.count()==1:
            bookprice.update(row.values()[0])        
            bookprice['tryDB']=tryDB
            bookprice['fromDB']=True
            bookprice['create']=None   
            #回傳顯示CST台北時間
            bookprice['create_dt']=bookprice['create_dt'].astimezone(tw)     
            #
            return bookprice        
        
    #3.開始抓==================================== 
    #mollie用get_mollie的selenium
    if store=='mollie':
        isbn=isbn13 or isbn
        result=get_mollie(isbn)        
        #
        if 'err' in result:
            bookprice['err']=result[:50]
        else:
            bookprice['stock']=result
        #
        bookprice['create_dt']=timezone.now() #django timezone會抓OS的UTC時間
        where={'bookid':bookprice['bookid'],#要用instance來指定
               'store':store,#bookid+store決定唯一一筆，update_or_create是get
               'defaults':bookprice}
        row, create = Bookprice.objects.update_or_create(**where)          
        #(2)整理回傳
        bookprice['tryDB']=tryDB
        bookprice['fromDB']=False
        bookprice['create']=create
        #回傳顯示CST台北時間
        bookprice['create_dt']=bookprice['create_dt'].astimezone(tw)
        #
        return bookprice  
    
    #根據store抓不同搜尋頁面
    #isbn='9789571380041' #9789571380049 #9789571380041AAA
    url_q=url_qs[store]+isbn+"+"+isbn13
    url_q_13=url_qs[store]+isbn13
    #print(url_q)
    #
    fake_header = Headers(
        browser="chrome",  # Generate only Chrome UA
        os="win",  # Generate ony Windows platform
        headers=True  # generate misc headers
    )    
    UA=fake_header.generate()  
    ippo=get_proxy(which="OK",now=True)
    proxies={
            "http": "http://"+ippo,
            #"https": "http://"+ippo
            } 
    #特殊處理___________________________________
    if store=='elite':
        proxies={}  
    if store=='ruten':
        url_api1="https://rtapi.ruten.com.tw/api/search/v2/index.php/core/prod?sort=prc%2Fac&q="
        url_api2="https://rtapi.ruten.com.tw/api/search/v2/index.php/m/core/prod?sort=prc%2Fac&q="
        url_apis=[url_api1,url_api2]
        isbn=isbn13 or isbn
        url_q=random.choice(url_apis)+isbn
    # 
    try:
        r = requests.get(url_q, 
                         headers=UA,
                         proxies=proxies,
                         #cookies=cookies,
                         #allow_redirects=False,
                         timeout=20)    
        r.encoding='utf8'
        #print(r.text)
        #
        doc=pq(r.text)                    
        r.close()
        #________________例外收集________________________________                            
        #狀態碼400~599        
        if r.status_code != 200:
            raise Exception(r.status_code) 
        #________________各家price收集________________________________
        #url_book=''
        price_sale='';
        price_sale_ebook='';
        #(1)誠品
        if store=='elite':
            count=doc.find("#ctl00_ContentPlaceHolder1_lbTotalResultCount").text()
            if count!='1':
                raise Exception('count='+count)             
            #
            #________________price收集________________________________
            price_sale=doc.find(".summary .price_sale font").text()
            url_book=doc.find(".box_list td.name a[title]").attr("href")            
        #(2)金石堂    
        elif store=='ks':
            #count=doc.find(".searchResultTitle > span:nth-child(2)").text()
            #只能有一本紙本書
            count=doc.find("span:Contains('加入購物車')").size()
            count2=doc.find("span:Contains('可訂購時通知我')").size()  
            count3=doc.find("span:Contains('停售')").size()  
            if count+count2+count3<1:
                raise Exception('count='+str(count)+"_"+str(count2)+"_"+str(count3))             
            #
            #________________price收集________________________________
            #--紙本書
            price_sale=doc.find("div.buymixbox:Contains('加入購物車')>span:Contains('特價')>b").text()
            if not price_sale:
                price_sale=doc.find("div.buymixbox:Contains('可訂購時通知我')>span:Contains('特價')>b").text()
            if not price_sale:
                price_sale=doc.find("div.buymixbox:Contains('停售')>span:Contains('特價')>b").text()
            #
            url =doc.find("div.buymixbox:Contains('加入購物車')").parent().find(".pdnamebox>a").attr("href") or ''
            url2=doc.find("div.buymixbox:Contains('可訂購時通知我')").parent().find(".pdnamebox>a").attr("href") or ''
            url3=doc.find("div.buymixbox:Contains('停售')").parent().find(".pdnamebox>a").attr("href") or ''
            url =(url or url2) or url3
            if url:
                url_book="https://www.kingstone.com.tw"+url
            #--電子書
            price_sale_ebook=doc.find("div.buymixbox:Contains('電子書')>span:Contains('特價')>b").text() or ''
            tmp=doc.find("div.buymixbox:Contains('電子書')").parent().find(".pdnamebox>a").attr("href")
            url_ebook=(tmp and "https://www.kingstone.com.tw"+tmp) or ''
        #(3)MOMO
        elif store=='momo':
            #(1)先從手機板抓店內碼
            goodsItemLi=doc.find("article.prdListArea li.goodsItemLi")
            count=goodsItemLi.find("p.publishInfo").size().__str__()
            if count!='1':
                raise Exception('count='+count)
            #
            #抓店內碼
            href=goodsItemLi.find("a[href*='goods']").attr("href")
            m=re.search(r'i_code=(.+?)&',href)
            i_code=m.group(1)
            #(2)從商品頁面抓price
            url_book="https://www.momoshop.com.tw/goods/GoodsDetail.jsp?i_code="+i_code
            r = requests.get(url_book, 
                             headers=UA,
                             proxies=proxies,
                             #cookies=cookies,
                             timeout=20)    
            r.encoding='utf8'
            #
            doc_prod=pq(r.text)  
            r.close()
            #________________price收集________________________________
            price_sale=doc_prod.find(".prdPrice .special span").text()            
        #(4)TAAZE
        elif store=='taaze':
            price_sale=''
            url_book=''
            ms=doc.find("div.media[rel]")   
            if ms.size()==0:
                #單獨用isbn13再查一次
                r = requests.get(url_q_13, 
                                 headers=UA,
                                 proxies=proxies,
                                 #cookies=cookies,
                                 #allow_redirects=False,
                                 timeout=20) 
                doc=pq(r.text)
                r.close() 
                ms=doc.find("div.media[rel]") 
                if ms.size()==0:
                    raise Exception('count=0')  
            #處理影片
            oid=ms.eq(0).attr("rel2")
            url_oid="https://www.taaze.tw/goods/"+oid+".html"
            r = requests.get(url_oid, 
                             headers=UA,
                             proxies=proxies,
                             #cookies=cookies,
                             timeout=20)    
            r.encoding='utf8'
            #
            doc_oid=pq(r.text)  
            r.close() 
            url_vdo=doc_oid.find('source').attr('src') or ''
            #________________price收集________________________________
            for m in ms:
                #子店內碼
                media=pq(m)
                pid=media.attr('rel')
                #oid=media.attr('rel2')                                       
                #(a)電子書
                if pid[:2]=='14':
                    price_sale_ebook=media.attr("data-saleprice_28")
                    url_ebook=media.find(".titleMain").find("a").attr("href")
                    continue
                #(b)第三碼判斷
                #--紙本新書    
                if pid[2]=='1' and pid[:2]!='14':
                    if not price_sale and not url_book:
                        price_sale=media.attr("data-saleprice_28")
                        url_book=media.find(".titleMain").find("a").attr("href")
                    #
                    continue                    
                #--回頭或二手    
                if pid[2] in ['2','3'] and pid[:2]!='14':
                    if media.attr("data-min_sale_price")!='nodata':#media.attr('data-qty_28')!='undefined' and 
                        price_sale=media.attr("data-min_sale_price")#要用小寫
                        url_book=media.find(".titleMain").find("a").attr("href") 
                    #
                    continue 
        #(5)灰熊
        elif store=='iread':
            price_sale=doc.find('.PP').find('.redword2').eq(-1).text() or ''
            url_book=doc.find('meta[property="og:url"]').attr('content') or ''
        #(6)城邦
        elif store=='cite':
            price_sale=doc.find('.book-info-2 ul').find('span.font-color01').eq(-1).text() or ''
            url_book=doc.find('.book-img.book_div a').attr('href') or ''
            if url_book:
                url_book='https://www.cite.com.tw'+url_book     
        #(7)天瓏
        elif store=='tenlong':
            price_sale=doc.find('.pricing .price').eq(0).text().replace('售價: $','').replace('貴賓價: $','') or ''
            url_book=doc.find('.cover').attr('href') or ''
            if url_book:
                url_book='https://www.tenlong.com.tw'+url_book 
        #(8)露天
        elif store=='ruten': 
            #先決定最低價的店內碼
            ans_dict=json.loads(r.text)
            TotalRows=ans_dict['TotalRows']
            if TotalRows>0:
                rt_id=ans_dict['Rows'][0]['Id']             
            #再去商品頁查
            if rt_id:
                url_book="https://goods.ruten.com.tw/item/show?"+rt_id  
                url_book_m="https://m.ruten.com.tw/goods/show.php?g="+rt_id
                r = requests.get(url_book_m, #PC版常有亂碼
                                 headers=UA,
                                 proxies=proxies,
                                 #allow_redirects=False,
                                 timeout=30) 
                r.encoding='utf8'
                #
                doc_prod=pq(r.text)
                r.close()
                #
                #desc=doc_prod.find('meta[property="og:description"]').attr('content') #PC版常有亂碼
                desc=doc_prod.find("script[type='application/ld+json']").eq(0).text() or ''
                price_sale=re.search('直購價：([0-9,]+?)元',desc).group(1) or ''
        #(9)三民
        elif store=='sanmin':
            price_sale=doc.find(".price").text() or ''
            url_book=doc.find(".resultBooksInfor h3 a").attr("href") or ''
            if url_book:
                url_book="https://www.sanmin.com.tw"+url_book   
        #(10)Yahoo
        elif store=='yahoo':
            price_sale=doc.find(".gridList span.BaseGridItem__price___31jkj em").eq(0).text().replace('$','') or ''
            url_book=doc.find(".gridList a.BaseGridItem__content___3LORP").eq(0).attr("href") or ''             
                
        
        #在js處理&amp;
        #url_book=urllib.parse.quote(url_book)
        #price_sale_ebook=urllib.parse.quote(price_sale_ebook)
        #去掉千分位
        price_sale=price_sale.replace(',','');
        price_sale_ebook=price_sale_ebook.replace(',','');
    except Exception as e:
        error=str(e)
        if 'timeout' in error:
            bookprice['err']='timeout'
        else:    
            bookprice['err']=error[:50]
    else:
        cols=['price_sale','url_book',
              'price_sale_ebook','url_ebook',
              'url_vdo'
             ]
        #
        for col in cols:         
            bookprice[col]=locals().get(col,'')
    finally:
        #(1)爬成功或失敗，都存DB
        bookprice['create_dt']=timezone.now() #django timezone會抓OS的UTC時間
        where={'bookid':bookprice['bookid'],#要用instance來指定
               'store':store,#bookid+store決定唯一一筆，update_or_create是get
               'defaults':bookprice}
        row, create = Bookprice.objects.update_or_create(**where)          
        #(2)整理回傳
        bookprice['tryDB']=tryDB
        bookprice['fromDB']=False
        bookprice['create']=create
        #回傳顯示CST台北時間
        bookprice['create_dt']=bookprice['create_dt'].astimezone(tw)
        #
        return bookprice
