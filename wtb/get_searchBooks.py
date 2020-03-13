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
from concurrent.futures import ThreadPoolExecutor,ProcessPoolExecutor 

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
from get_proxy import get_proxy

#_________________________________________________
def get_searchBooks(kw:str='村上春樹',which='free',now=False):
    #kw="動盪"
    url_searchbooks="https://search.books.com.tw/search/query/cat/BKA/key/"+kw
    #
    fake_header = Headers(
        browser="chrome",  # Generate only Chrome UA
        os="win",  # Generate ony Windows platform
        headers=True  # generate misc headers
    )    
    UA=fake_header.generate()
    ippo=get_proxy('OK',now)
    proxies={"http": "http://"+ippo}
    #
    r = requests.get(url_searchbooks, 
                     headers=UA,
                     proxies=proxies,
                     timeout=30)
    r.encoding='utf8'
    doc=pq(r.text)
    r.close()
    #
    searchbooks=doc.find("#searchlist .searchbook")
    items=searchbooks.find(".item")
    n=items.size()
    results=[]    
    if n==0:
        return json.dumps(results,default=str,ensure_ascii=False)
    if n>10:
        n=10
    #最多取10筆結果________________
    for i in range(n):
        book={}
        item=items.eq(i)
        #整理資料====================================
        #book['bookid']=item.find("div.input_buy input").attr('value')     
        #有些沒checkbox
        href=item.find("a[rel=mid_name]").attr('href')                
        bookid=re.search('/mid/item/(.+?)/page',href).group(1)
        book['bookid']=bookid        
        src=item.find("img.itemcov").attr("data-original")
        if 'restricted18' in src:
            #18禁先不搜
            continue
        #    
        book['src']=src
        
        book['title']=item.find("a[rel=mid_name]").text()
        #
        authors=''
        for a in item.find("a[rel=go_author]"):
            authors+=pq(a).text()+"/"
        book['author']=authors.strip("/")
        #
        book['publisher']=item.find("a[rel=mid_publish]").text()
        book['pub_dt']=re.search('出版日期[^0-9]+?([0-9\-]+)',item.text()).group(1)
        count_off= item.find('span.price').find("b").eq(0).text().ljust(2,'0')
        price_sale=item.find('span.price').find("b").eq(1).text()
        if price_sale:
            price_list=int(price_sale)*100//int(count_off)
        else:
            price_list=int(count_off) #沒有折扣
        #book['sale']=count_off+"_"+price_sale
        book['price_list']=price_list
        intro=item.find('span.price').next().text()
        intro=re.sub('\.+? *more','',intro)
        book['intro']=intro
        #
        results.append(book)    
    
    #___________________
    results=json.dumps(results,default=str,ensure_ascii=False) 
    return results
