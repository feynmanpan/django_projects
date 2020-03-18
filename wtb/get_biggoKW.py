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
#
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'wtb.settings')
os.environ["DJANGO_ALLOW_ASYNC_UNSAFE"] = "true"
django.setup()
#from mainsite.models import Bookinfo,Bookprice,Store

def get_biggoKW(kw:str='村上春樹',which='free',now=False):    
    #E:\00_Taaze\01_Taaze\doc\eclipse-workspace\taaze\src\new-service\com\xsx\ec\service\impl\EcSearchResultImp.java
    #注意ajax response格式
    #url_q='https://searchapi.biggo.com/taaze/suggestion.php?query='+kw    
    #url_q='https://biggo.com.tw/api/suggestion.php?query='+kw
    #url_q='http://www.eslite.com/Search_BW_DataSrc.aspx?term='+kw
    
    #https://www.taaze.tw/new_ec/rwd/include/js/main.js?v=6
    url_q='https://www.taaze.tw/beta/autocompleted.jsp?k='+kw
    fake_header = Headers(
        browser="chrome",  # Generate only Chrome UA
        os="win",  # Generate ony Windows platform
        headers=True  # generate misc headers
    )    
    UA=fake_header.generate()
    UA= {'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36'}
    #不代理，太慢了
    #ippo=get_proxy(which,now)
    #ippo="94.205.140.158:34561"
    #proxies={
     #       "http": "http://"+ippo,
            ##"https": "http://"+ippo
      #      }
    try:
        r = requests.get(url_q,                 
                         headers=UA,
                         #data={'k':'村'},
                         #proxies=proxies,
                         #cookies=cookies,
                         timeout=15)    
        r.encoding='utf8'
        ans=r.text
        r.close()
        #json.loads(r.text)        
        return ans
    except Exception as err:
        return ''#str(err)
    
