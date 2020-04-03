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

#https://free-proxy-list.net/
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
            if len(line.split(":"))==2:
                ippos.append(line)
    if now:
        sleep(1.5)
        return random.choice(ippos)
    #ippo
    old=[]
    #測試代理_________________________________________
    while True:
        fake_header = Headers(
            browser="chrome",  # Generate only Chrome UA
            os="win",  # Generate ony Windows platform
            headers=True  # generate misc headers
        )    
        UA=fake_header.generate()
        #UA = {'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36'}
        #已經測過的就不要
        ippo=random.choice(ippos)
        if len(old)/len(ippos) > 0.5:
            old=[]
        if ippo in old:
            continue
        else:
            old.append(ippo)
        #    
        ip=ippo.split(":")[0]
        proxies={
                "http": "http://"+ippo,
                "https": "http://"+ippo
                }  
        #print("test:"+ippo)    
        #clear_output(wait=True)
        try:
            test=['http://icanhazip.com/','https://myip.com.tw/','https://www.showmyipaddress.eu/']
            r = requests.get(random.choice(test),#test[1], 
                             headers=UA,
                             proxies=proxies,
                             timeout=4)
            r.encoding='utf8'
            #print(r.status_code)
            #print(r.text)
            #return
            #return 22
            #
            if(r.status_code == 200 and (ip in r.text or '&#46;'.join(ip.split('.')) in r.text) ):
                print("OK:"+which+"_"+ippo)
                #print(r.status_code)
                #print(r.text)
                r.close() 
                if which!='OK':
                    fn='/home/pan/django_projects/wtb/ips_OKs.txt'
                    mode=0                    
                    if mode==0:
                        #加到最後一行
                        with open(fn, 'a+') as f:
                            f.write(ippo+"\r\n")      
                    else:
                        #刪掉第一行_加到最後一行
                        with open(fn, 'r+') as f: # open file in read / write mode
                            firstLine = f.readline() # read the first line and throw it out
                            data = f.read() # read the rest
                            data += ippo+"\r\n"
                            f.seek(0) # set the cursor to the top of the file
                            f.write(data) # write the data back
                            f.truncate() # set the file size to the current size 
                #______________
                return ippo
            else:#if not (r.status_code == 200 and ip in r.text):
                r.close()
                raise Exception('fail')
               
        except Exception as e:
            #print(str(e))
            #clear_output(wait=True) 
             
            sleep(1.5+random.uniform(0, 2))
            #sleep(0.1)
            continue
        #else:
        #    print(r.text)
        #    print("OK2:"+ip)
        #    r.close()       
        #    break    
