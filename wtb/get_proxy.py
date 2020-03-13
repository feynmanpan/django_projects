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


def get_proxy(which='free',now=False):
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
                if len(line.split(":"))>1:
                    ippos.append(line)
    if now:
        return random.choice(ippos)
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
            test=['http://icanhazip.com/','https://whatismyipaddress.com/']
            r = requests.get("http://icanhazip.com/", 
                             headers=UA,
                             proxies=proxies,
                             timeout=4)
            r.encoding='utf8'
            #print(r.text)
            #return 22
            #
            if(r.status_code == 200 and ip in r.text):
                print("OK:"+which+"_"+ippo)
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
            sleep(1.5+random.uniform(0, 2))
            continue
        #else:
        #    print(r.text)
        #    print("OK2:"+ip)
        #    r.close()       
        #    break    
