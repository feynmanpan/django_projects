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
#
def get_hybook(page):
    url_hybook="http://www.hybook.com.tw/search.asp?page="+str(page)
    #
    fake_header = Headers(
        browser="chrome",  # Generate only Chrome UA
        os="win",  # Generate ony Windows platform
        headers=True  # generate misc headers
    )    
    UA=fake_header.generate()
    #UA={'User-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36'}

    
    #
    while True:
        try:
            ippo=get_proxy(which='free',now=True)
            #print(ippo)
            #ippo='103.241.227.107:6666'
            proxies={"http": "http://"+ippo}
            #
            r = requests.get(url_hybook, 
                             headers=UA,
                             #proxies=proxies,
                             timeout=8,
                             allow_redirects=False
                            )
            #r.encoding='utf-8'
            r.encoding='big5'
            doc=pq(r.text)
            #print(r.content) #text有亂碼
            r.close()

            table=doc.find('table').eq(1)
            trs=table.find('tr')
            page=[]
            for tr in trs:
                tr=pq(tr)
                row=''
                for i in range(9):
                    row+=tr.find('td').eq(i).text()+','
                    #print(tr.find('td').eq(i).text())
                #
                row=row.strip(',')
                page.append(row)
            #
            if len(page)==0:
                raise Exception('norows')  
            #
            return page
        except Exception as err:
            print(str(err))
            #page.append['page_'+str(page)+"_"+str(err)]
            continue
            
