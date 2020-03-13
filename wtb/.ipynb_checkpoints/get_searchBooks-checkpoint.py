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


def get_searchBooks():
    kw="動盪"
    url_searchbooks="https://search.books.com.tw/search/query/cat/BKA/key/"+kw
    #
    fake_header = Headers(
        browser="chrome",  # Generate only Chrome UA
        os="win",  # Generate ony Windows platform
        headers=True  # generate misc headers
    )    
    UA=fake_header.generate()
    proxies={"http": "http://"+get_proxy('OK')}
    #
    r = requests.get(url_searchbooks, 
                     headers=UA,
                     proxies=proxies,
                     timeout=30)
    r.encoding='utf8'
    doc=pq(r.text)
    #print(r.text)
    r.close()
    #
    searchbooks=doc.find("#searchlist .searchbook")
    top10=searchbooks.find(".item")
    return top10.size()
