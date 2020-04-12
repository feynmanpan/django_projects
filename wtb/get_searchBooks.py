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
    
    #1. UA__________________
    fake_header = Headers(
        browser="chrome",  # Generate only Chrome UA
        os="win",  # Generate ony Windows platform
        headers=True  # generate misc headers
    )    
    #ua = UserAgent()  #20200412_突然掛了
    UA={
            'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
            'Accept-Encoding':'gzip, deflate, br',
            'Accept-Language':'zh-TW,zh;q=0.9,en-US;q=0.8,en;q=0.7,ja;q=0.6,zh-CN;q=0.5,fr;q=0.4,nl;q=0.3',
            'Connection':'keep-alive',
            #'Cookie':'bid=5e6c707e6c0b6; _gcl_au=1.1.107924002.1584165002; _fbp=fb.2.1584165006803.1736193256; _ga=GA1.3.412690052.1584165010; _gid=GA1.3.1308642955.1584165010; __gads=ID=51bf519d611621e6':'T=1584165012':'S=ALNI_MY8XQcRb1LkFIbgMraUAQceRgccNQ; s_session=Xm0LpwomC28AAXEquPAAAAAi; home_tbanner=0; ssid=5e6c707e6c0b6.1584553407; BIGipServerpool_nsearch_http=1863001610.20480.0000; key_history=%7B%221584554411%22%3A%22%25E7%2599%25BD%25E9%25AF%25A8%25E8%25A8%2598%22%2C%221584516646%22%3A%22%25E5%25B0%258B%25E7%25BE%258A%25E5%2586%2592%25E9%259A%25AA%25E8%25A8%2598%22%2C%221584426616%22%3A%22%25E5%258B%2595%25E7%259B%25AA%22%2C%221584283952%22%3A%22%25E5%25A4%25A7%25E9%25A8%2599%25E5%25B1%2580%22%2C%221584283926%22%3A%22%25E6%258C%25AA%25E5%25A8%2581%25E7%259A%2584%25E6%25A3%25AE%25E6%259E%2597%2520%2520%25E4%25B8%258A%2520%22%2C%221584283835%22%3A%2282%25E5%25B9%25B4%25E7%2594%259F%25E7%259A%2584%25E9%2587%2591%25E6%2599%25BA%25E8%258B%25B1%22%2C%221584254136%22%3A%22%25E6%25A7%258D%25E7%25A0%25B2%25E7%2597%2585%25E8%258F%258C%25E8%2588%2587%25E9%258B%25BC%25E9%2590%25B5%22%2C%221584208117%22%3A%220010379034%22%2C%221584204707%22%3A%22F016393358%22%2C%221584204696%22%3A%220010844123%22%2C%221584202375%22%3A%22V.S%22%2C%221584201909%22%3A%22%25E8%25B2%2593%25E9%25A0%25AD%25E9%25B7%25B9%25E5%259C%25A8%25E9%25BB%2583%25E6%2598%258F%25E9%25A3%259B%25E7%25BF%2594%25EF%25BC%259A%25E5%25B7%259D%25E4%25B8%258A%25E6%259C%25AA%25E6%2598%25A0%25E5%25AD%2590V.S%25E6%259D%2591%25E4%25B8%258A%25E6%2598%25A5%25E6%25A8%25B9%25E8%25A8%25AA%25E8%25AB%2587%25E9%259B%2586%22%2C%221584201802%22%3A%22%25E8%25B2%2593%25E9%25A0%25AD%25E9%25B7%25B9%25E5%259C%25A8%25E9%25BB%2583%25E6%2598%258F%25E9%25A3%259B%25E7%25BF%2594%2520%25E5%25B7%259D%25E4%25B8%258A%25E6%259C%25AA%25E6%2598%25A0%25E5%25AD%2590V.S%25E6%259D%2591%25E4%25B8%258A%25E6%2598%25A5%25E6%25A8%25B9%25E8%25A8%25AA%25E8%25AB%2587%25E9%259B%2586%22%2C%221584195796%22%3A%22%25E4%25BB%258A%25E5%25A4%25A9%25E7%259A%2584%25E6%2588%2591%25E8%25A6%2581%25E5%2592%258C%25E6%2598%258E%25E5%25A4%25A9%25E7%259A%2584%25E4%25BD%25A0%25E7%25B4%2584%25E6%259C%2583%22%7D',
            'Host':'search.books.com.tw',
            'Sec-Fetch-Dest':'document',
            'Sec-Fetch-Mode':'navigatev',
            'Sec-Fetch-Site':'nonev',
            'Sec-Fetch-User':'?1',
            'Upgrade-Insecure-Requests':'1',
            #'User-Agent':ua.random,  
            'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.132 Safari/537.36',
        }
    UA=fake_header.generate()
    #UA= {'User-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36'}
    #UA= {'user-agent':'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36'}

    
    #2. Proxy______________________________________
    ippo=get_proxy(which,now)
    proxies={"http": "http://"+ippo}
    #
    try:
        r = requests.get(url_searchbooks, 
                         headers=UA,
                         proxies=proxies,
                         timeout=30)
        r.encoding='utf8'
        #print(r.text)
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
            book['publisher']=item.find("a[rel=mid_publish]").text() or ''
            #白鯨記沒有出版日期
            m=re.search('出版日期[^0-9]+?([0-9\-]+)',item.text())
            if m:
                book['pub_dt']=m.group(1)
            else:
                book['pub_dt']=''
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
    except Exception as err:
        return ''#str(err)
