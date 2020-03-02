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
from mainsite.models import Bookinfo,Bookprice,Store,Post

#________________________________________________

def get_bookprice(bookid:str='',isbn:str='',store:str='',tryDB=True)->dict:
    
    bookprice={'err':'','bookid':bookid,'isbn':isbn,'store':store}
    tw = pytz.timezone('Asia/Taipei')
    
    #1.確認====================================
    #(0)一定要指定店家
    if not store:
        bookprice['err']='nostore'
        return bookprice
    #(1)bookid跟isbn至少要有一個
    if not bookid and not isbn:
        bookprice['err']='nobookidisbn'
        return bookprice
    #(2)根據bookid有無，更新isbn
    if bookid:
        if type(bookid) is not str or len(bookid)!=10:
            bookprice['err']='wrongbookid'
            return bookprice 
        #以重查的isbn為準
        row=Bookinfo.objects.filter(bookid=bookid)
        if row.count()==1:
            bookprice['isbn']=row.first().isbn
        else:
            bookprice['err']='nosuchbookid'
            return bookprice 
    else:
        #沒bookid，就一定要用isbn重查
        row=Bookinfo.objects.filter(isbn=isbn)
        if row.count()==1:        
            bookprice['bookid']=row.first().bookid
        else:
            bookprice['err']='nosuchisbn'
            return bookprice        

    #2.開始抓====================================
    #搜尋類型用isbn會找不到，用全站
    url_q="http://www.eslite.com/Search_BW.aspx?searchType=&query="+isbn
    fake_header = Headers(
        browser="chrome",  # Generate only Chrome UA
        os="win",  # Generate ony Windows platform
        headers=True  # generate misc headers
    )    
    UA=fake_header.generate()
    
    #try    
    r = requests.get(url_q, 
                     headers=UA,
                     #proxies=proxies,
                     #cookies=cookies,
                     timeout=3)    
    r.encoding='utf8'
    #print(r.text)
    #
    doc=pq(r.text)    
        
    count=doc.find("#ctl00_ContentPlaceHolder1_lbTotalResultCount").text()
    
    if count=='1':
        price_sale=doc.find(".summary").eq(0).find(".price_sale font").text()
        bookprice['price_sale']=price_sale
    #
    return bookprice
    
