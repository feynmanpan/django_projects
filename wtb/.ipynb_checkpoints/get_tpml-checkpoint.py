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
def get_tpml(isbn):
    url_q="http://book.tpml.edu.tw/webpac/booksearch.do?searchtype=simplesearch&search_field=ISBN&search_input="+isbn
    fake_header = Headers(
        browser="chrome",  # Generate only Chrome UA
        os="win",  # Generate ony Windows platform
        headers=True  # generate misc headers
    )    
    UA=fake_header.generate()  
    ippo=get_proxy(which="free",now=True)
    proxies={
            "http": "http://"+ippo,
            #"https": "http://"+ippo
            }
    try:
        r = requests.get(url_q, 
                         headers=UA,
                         #proxies=proxies,
                         #allow_redirects=False,
                         timeout=30)    
        r.encoding='utf8'        
        r.close()
        book_href=re.findall('bookDetail.+id=[0-9]+',r.text)
        if len(book_href)!=1:
            return ''
        else:
            return 'http://book.tpml.edu.tw/webpac/'+book_href[0]
    except Exception as err:
        return ''
        
