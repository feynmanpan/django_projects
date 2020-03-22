#%load get_bookprice.py
#%run get_bookprice.py
# -*- coding: utf-8 -*-

import time
import requests
from bs4 import BeautifulSoup
from bs4.element import NavigableString
import pandas as pd
import numpy as np
from time import sleep, time
from threading import Thread
import random
import re
from IPython.display import clear_output, display
import json
import csv
import os
from get_proxy import get_proxy
#
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.expected_conditions import visibility_of_element_located
from selenium.webdriver.common.by import By   
#
#https://blog.csdn.net/zhangpeterx/article/details/83502641
def get_shopee(isbn):
    chrome_options = Options()
    chrome_options.add_argument('--no-sandbox')  #让Chrome在root权限下跑
    chrome_options.add_argument("--window-size=1920,1080")
    chrome_options.add_argument("--start-maximized")
    chrome_options.add_argument('--headless') #不用打开图形界面
    chrome_options.add_argument('--disable-dev-shm-usage')
    chrome_options.add_argument('blink-settings=imagesEnabled=false')
    chrome_options.add_argument('--disable-gpu')
    #
    #ippo=get_proxy('OK',now=True)
    ua='Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36'
    #用代理很久，要20s以上
    #chrome_options.add_argument(f'--proxy-server={ippo}')#.format(ippo))  
    chrome_options.add_argument("user-agent={}".format(ua))  

    #0.開chrome_記得查chrome版本，用同版本的driver:google-chrome -version
    driver = webdriver.Chrome("/home/pan/chromedriver80",options=chrome_options)
    driver.implicitly_wait(10)
    url = "https://shopee.tw/search?order=asc&page=0&sortBy=price&keyword="+isbn
    driver.get(url)
    print(driver.current_url+"_____")

    try:
        price_selector='#main span._341bF0'
        url_selector='.shopee-search-item-result__item>div>a'
        #
        WebDriverWait(driver, 10, 0.5).until(EC.presence_of_element_located((By.CSS_SELECTOR, price_selector))) 
        #
        price_sale=driver.find_element_by_css_selector(price_selector).text.replace(',','')    
        url_book=driver.find_element_by_css_selector(url_selector).get_attribute("href")  
    
        driver.quit()
        return [price_sale,url_book]
    except Exception as err:
        driver.quit()
        return 'err_'+str(err)
