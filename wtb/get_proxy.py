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


def get_proxy(which='free'):
    which_dict={'kuai':"/home/pan/django_projects/wtb/ips_kuai.txt",
                'ihuan':"/home/pan/django_projects/wtb/ips_1000_ihuan.txt",
                'free':"/home/pan/django_projects/wtb/ips_free.txt",
                'OK':"/home/pan/django_projects/wtb/ips_OKs.txt"
               }
    ippos=[]
    with open(which_dict[which], 'r') as f:
            lines=f.readlines()
            for line in lines:
                line=line.strip()
                if line:
                    ippos.append(line)
    #ippo=random.choice(ippos)#.split(":")
    #ippo
    #測試代理_________________________________________
    while True:
        fake_header = Headers(
            browser="chrome",  # Generate only Chrome UA
            os="win",  # Generate ony Windows platform
            headers=True  # generate misc headers
        )    
        UA=fake_header.generate()
        #UA = {'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36'}
        #
        ippo=random.choice(ippos)
        ip=ippo.split(":")[0]
        proxies={"http": "http://"+ippo}  
        #print("test:"+ippo)    
        #clear_output(wait=True)
        try:
            r = requests.get("http://icanhazip.com/", 
                             headers=UA,
                             proxies=proxies,
                             timeout=4)
            r.encoding='utf8'
            #
            if(r.status_code == 200 and ip in r.text):
                print("OK:"+ippo)
                #print(r.status_code)
                #print(r.text)
                r.close() 
                if which!='OK':
                    with open('/home/pan/django_projects/wtb/ips_OKs.txt', 'a+') as f:
                        f.write(ippo+"\r\n")                
                return ippo            
        except Exception as e:
            #print(str(e))
            #clear_output(wait=True) 
            sleep(0.5+random.uniform(0, 1))
            continue
        #else:
        #    print(r.text)
        #    print("OK2:"+ip)
        #    r.close()       
        #    break    
