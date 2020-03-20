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
#
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'wtb.settings')
os.environ["DJANGO_ALLOW_ASYNC_UNSAFE"] = "true"
django.setup()
from mainsite.models import Bookinfo,Bookprice,Store
from dict_stores import url_qs


def get_isbn_from_elite(title):
    #(1)先查搜尋頁________________________________
    #title='刺蝟的優雅（十週年暢銷紀念書衣版）'
    url_q='http://www.eslite.com/Search_BW.aspx?searchType=&query='+title
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
    r = requests.get(url_q, 
                     headers=UA,
                     #proxies=proxies,
                     #cookies=cookies,
                     #allow_redirects=False,
                     timeout=30)    
    r.encoding='utf8'
    #print(r.text)
    #
    doc=pq(r.text)
    r.close()
    
    count=doc.find("#ctl00_ContentPlaceHolder1_lbTotalResultCount").text()
    if int(count)<1:
        return []
    
    #(2)查單書頁________________________________
    url_book=doc.find(".box_list td.name a[title]").eq(0).attr("href")    
    m=re.search('pgid=([0-9]+)',url_book)
    pgid=m.group(1)
    url_book="http://www.eslite.com/product.aspx?pgid="+pgid
    #print(url_book)
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
    r = requests.get(url_book, 
                     headers=UA,
                     #proxies=proxies,
                     #cookies=cookies,
                     #allow_redirects=False,
                     timeout=30)    
    r.encoding='utf8' 
    doc_book=pq(r.text)
    r.close()    
    #
    tmp=doc_book.find(".C_box:Contains('誠品26碼')").find('p').eq(0).text()
    isbn13=re.search('ISBN 13 ／([0-9]+)',tmp).group(1)
    isbn10=re.search('ISBN 10 ／([0-9]+)',tmp).group(1)    
    #
    return [isbn10,isbn13]
