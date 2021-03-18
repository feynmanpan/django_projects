from fastapi import FastAPI, Request
from pydantic import BaseModel, Field
from starlette.middleware.cors import CORSMiddleware
import pandas as pd
import numpy as np
import requests
from random import random, uniform
from pyquery import PyQuery as pq
from time import sleep, time
from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta
import json
import math
import re
import asyncio
import nest_asyncio
nest_asyncio.apply()
#
app = FastAPI(
    title="FastAPI",
    description="",
    version="1.0.0",
    openapi_tags=[
        {
            'name': '規格豬',
            'description': '抓取 [畜產行情資訊網](http://ppg.naif.org.tw/naif/MarketInformation/Poultry/TranStatistics.aspx)【毛豬行情查詢】之日/月/年行情',
            # "externalDocs": {
            #     "description": "來源",
            #     "url": "http://ppg.naif.org.tw/naif/MarketInformation/Poultry/TranStatistics.aspx",
            # },
        },
        # {
        #     'name': '測試',
        #     'description': '測試用',
        # }
    ],
)
app.add_middleware(CORSMiddleware, allow_origins=['*'])


# 規格豬
cacert = True
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.135 Safari/537.36',
}
url_pig = "https://ppg.naif.org.tw/naif/MarketInformation/Pig/FPSCompare.aspx"
url_pig2 = "http://ppg.naif.org.tw/naif/MarketInformation/Pig/TranStatistics.aspx"  # 單日多市場價量比較
#
year_format = '%Y'
month_format = '%Y-%m'
date_format = '%Y-%m-%d'
time_format = '%H:%M:%S'
#
wd_map = {
    0: '(一)',
    1: '(二)',
    2: '(三)',
    3: '(四)',
    4: '(五)',
    5: '(六)',
    6: '(日)',
}
#
today = datetime.today().date()
yesday1 = today - timedelta(days=1)
yesday2 = today - timedelta(days=2)
last_m = str(today - relativedelta(months=1))[:7]
last_y = str(today - relativedelta(years=1))[:4]


class DateRange(BaseModel):
    sd: str = Field(str(yesday2), title='開始日期', example=str(yesday2))  # Schemas
    ed: str = Field(str(yesday1), title='結束日期', example=str(yesday1))

    class Config:
        schema_extra = {
            "example": {
                "sd": str(yesday2),  # "2021-01-01", # try it out
                "ed": str(yesday1),  # "2021-01-05",
            }
        }


def isocheck(sd: str, ed: str, ymd_format: str):
    err = 'error'
    # (1) iso格式檢查
    try:
        datetime.strptime(sd, ymd_format)
        datetime.strptime(ed, ymd_format)
    except Exception:
        return False, {err: '日期格式非ISO標準，如2021-01-02，或日期數字過大過小不正常'}
    #
    print(f'sd={sd}, ed={ed}')
    # (2) 日期範圍檢查
    today = datetime.today().date()
    last_d = str(today - relativedelta(days=1))
    last_m = str(today - relativedelta(months=1))[:7]
    last_y = str(today - relativedelta(years=1))[:4]
    if ymd_format == date_format and ed > last_d:
        return False, {err: f'結束最晚到昨天{last_d}'}
    elif ymd_format == month_format and ed > last_m:
        return False, {err: f'結束最晚到上個月{last_m}'}
    elif ymd_format == year_format and ed > last_y:
        return False, {err: f'結束最晚到去年{last_y}'}
    #
    if sd > ed:
        return False, {err: f'開始需早於結束'}
    #
    return True, None


def floatint(x):
    x = str(x).replace(',', '').replace('-', '0').replace(' ', '')
    x = x or '0'
    xf = float(x)
    xn = int(xf)
    return xf > xn and xf or xn


def zero(x):
    return x != 0 and x or 0


# 爬蟲loop
loop = asyncio.get_event_loop()


async def async_func(get_func, Dinlist):
    '''將同步函數封成async'''
    return await loop.run_in_executor(None, get_func, Dinlist)


def async_get_miss(get_func, miss_date):
    '''迴圈同步爬，改成一日一task異步爬'''
    tasks = []
    for D in miss_date:
        task = loop.create_task(async_func(get_func, [D]))
        tasks.append(task)
    # 爬蟲結果扁平化 result=[[{D1}],[{D2}],[{D3}],...] ==> [{D1},{D2},{D3},...]
    result = loop.run_until_complete(asyncio.gather(*tasks))
    result = [dictD for eachD in result for dictD in eachD]
    #
    return result


def get_miss_date_T(miss_date):
    '''【交易行情統計】'''
    # 第一次進入頁面【交易行情統計】
    r1 = requests.get(url_pig2, headers=headers, verify=cacert)
    r1.encoding = 'utf-8'
    doc1 = pq(r1.text, parser='html')
    r1.close()
    #
    postdata = {
        # 按下【單日多市場價量比較】
        '__EVENTTARGET': 'ctl00$ctl00$ContentPlaceHolder_contant$ContentPlaceHolder_contant$LinkButton_query2',
        '__VIEWSTATE': doc1.find("#__VIEWSTATE").attr('value'),
        '__VIEWSTATEGENERATOR': doc1.find("#__VIEWSTATEGENERATOR").attr('value'),
        '__EVENTVALIDATION': doc1.find("#__EVENTVALIDATION").attr('value'),
    }
    r2 = requests.post(url_pig2, headers=headers, data=postdata, verify=cacert)
    r2.encoding = 'utf-8'
    doc2 = pq(r2.text, parser='html')
    r2.close()
    postdata = {
        '__VIEWSTATE': doc2.find("#__VIEWSTATE").attr('value'),
        '__VIEWSTATEGENERATOR': doc2.find("#__VIEWSTATEGENERATOR").attr('value'),
        '__EVENTVALIDATION': doc2.find("#__EVENTVALIDATION").attr('value'),
        'ctl00$ctl00$ContentPlaceHolder_contant$ContentPlaceHolder_contant$Button_Content2_Submit': '查詢',
    }
    # 開始查詢
    day_data = []
    for D in miss_date:
        sleep(uniform(0.1, 1))
        #
        postdata['ctl00$ctl00$ContentPlaceHolder_contant$ContentPlaceHolder_contant$TextBox_Content2_QueryDate'] = D
        #
        r3 = requests.post(url_pig2, headers=headers, data=postdata, verify=cacert)
        r3.encoding = 'utf-8'
        doc3 = pq(r3.text, parser='html')
        r3.close()
        # 抓12個儲存格
        today = {
            'A1_tw@': doc3.find('#ContentPlaceHolder_contant_ContentPlaceHolder_contant_GridView2_Label3_0').text(),  # 台灣合計成交頭數
            'A2@': doc3.find('#ContentPlaceHolder_contant_ContentPlaceHolder_contant_GridView2_Label3_1').text(),  # 台灣(不含澎湖)合計成交頭數
            'A3_tw@': doc3.find('#ContentPlaceHolder_contant_ContentPlaceHolder_contant_GridView2_Label6_0').text(),  # 台灣規格豬成交頭數
            'A3@': doc3.find('#ContentPlaceHolder_contant_ContentPlaceHolder_contant_GridView2_Label6_1').text(),  # 不含澎湖之規格豬成交頭數
            #
            'B1_tw@': doc3.find('#ContentPlaceHolder_contant_ContentPlaceHolder_contant_GridView2_Label4_0').text(),  # 台灣均重
            'B2@': doc3.find('#ContentPlaceHolder_contant_ContentPlaceHolder_contant_GridView2_Label4_1').text(),  # 不含澎湖均重
            'B3_tw@': doc3.find('#ContentPlaceHolder_contant_ContentPlaceHolder_contant_GridView2_Label8_0').text(),  # 台灣規格豬均重
            'B3@': doc3.find('#ContentPlaceHolder_contant_ContentPlaceHolder_contant_GridView2_Label8_1').text(),  # 不含澎湖之規格豬均重
            #
            'C1_tw@': doc3.find('#ContentPlaceHolder_contant_ContentPlaceHolder_contant_GridView2_Label5_0').text(),  # 台灣均價
            'C2@': doc3.find('#ContentPlaceHolder_contant_ContentPlaceHolder_contant_GridView2_Label5_1').text(),  # 不含澎湖均價
            'C3_tw@': doc3.find('#ContentPlaceHolder_contant_ContentPlaceHolder_contant_GridView2_Label10_0').text(),  # 台灣規格豬均價
            'C3@': doc3.find('#ContentPlaceHolder_contant_ContentPlaceHolder_contant_GridView2_Label10_1').text(),  # 不含澎湖之規格豬均價
        }
        print(f'爬取 {D} 之日行情 OK (單日多市場價量比較)')
        day_data.append(today)
    #
    return day_data


def get_miss_date(miss_date):
    '''日行情'''
    # 第一次進入頁面
    r1 = requests.get(url_pig, headers=headers, verify=cacert)
    r1.encoding = 'utf-8'
    doc1 = pq(r1.text, parser='html')
    r1.close()
    #
    postdata = {
        '__VIEWSTATE': doc1.find("#__VIEWSTATE").attr('value'),
        '__VIEWSTATEGENERATOR': doc1.find("#__VIEWSTATEGENERATOR").attr('value'),
        '__EVENTVALIDATION': doc1.find("#__EVENTVALIDATION").attr('value'),
        'ctl00$ctl00$ContentPlaceHolder_contant$ContentPlaceHolder_contant$CheckBoxList_Market$1': 'H268',  # 宜蘭,新竹,苗栗,花蓮,澎湖,台灣地區，一次查
        'ctl00$ctl00$ContentPlaceHolder_contant$ContentPlaceHolder_contant$CheckBoxList_Market$3': 'H302',
        'ctl00$ctl00$ContentPlaceHolder_contant$ContentPlaceHolder_contant$CheckBoxList_Market$4': 'H356',
        'ctl00$ctl00$ContentPlaceHolder_contant$ContentPlaceHolder_contant$CheckBoxList_Market$20': 'H955',
        'ctl00$ctl00$ContentPlaceHolder_contant$ContentPlaceHolder_contant$CheckBoxList_Market$21': 'H880',  # 澎湖
        'ctl00$ctl00$ContentPlaceHolder_contant$ContentPlaceHolder_contant$CheckBoxList_Market$22': '%',  # 台灣
        "ctl00$ctl00$ContentPlaceHolder_contant$ContentPlaceHolder_contant$Button_query": "查詢",
    }

    # 開始查詢送出表單
    day_data = []
    for D in miss_date:
        stime = time()
        sleep(uniform(0.1, 1))
        #
        postdata['ctl00$ctl00$ContentPlaceHolder_contant$ContentPlaceHolder_contant$TextBox_Content1_ThisDate'] = D
        postdata["ctl00$ctl00$ContentPlaceHolder_contant$ContentPlaceHolder_contant$TextBox_Content1_LastDate"] = D
        #
        r2 = requests.post(url_pig, headers=headers, data=postdata, verify=cacert)
        r2.encoding = 'utf-8'
        doc2 = pq(r2.text, parser='html')
        r2.close()
        # 抓13列
        trs = doc2.find('.tbResult').find('tr')
        # 宜蘭,新竹,苗栗,花蓮的155以上
        tr11 = trs.eq(11).find('td')
        tr28 = trs.eq(28).find('td')
        tr45 = trs.eq(45).find('td')
        tr62 = trs.eq(62).find('td')
        # 澎湖
        tds71 = trs.eq(71).find('td')
        tds72 = trs.eq(72).find('td')
        tds73 = trs.eq(73).find('td')
        tds74 = trs.eq(74).find('td')
        tds75 = trs.eq(75).find('td')
        tds76 = trs.eq(76).find('td')
        tds77 = trs.eq(77).find('td')
        tds78 = trs.eq(78).find('td')
        tds79 = trs.eq(79).find('td')
        # 台灣地區
        # tds88 = trs.eq(88).find('td')
        # tds89 = trs.eq(89).find('td')
        # tds90 = trs.eq(90).find('td')
        tds91 = trs.eq(91).find('td')
        tds92 = trs.eq(92).find('td')
        tds93 = trs.eq(93).find('td')
        tds94 = trs.eq(94).find('td')
        tds95 = trs.eq(95).find('td')
        tds96 = trs.eq(96).find('td')
        #
        today = {
            'date': D,
            'wd': wd_map[datetime.strptime(D, date_format).weekday()],
            # A.成交頭數_______________________________
            # 'A1': tds88.eq(2).text(),
            # 'A2': tds89.eq(2).text(),
            # 'A3': tds90.eq(2).text(),
            'A1_tw@': '0',
            'A2@': '0',
            'A3_tw@': '0',
            'A3@': '0',
            #
            'A375': '0',  # 75+
            'A395': '0',  # 95+
            'A75': tds91.eq(2).text(),
            'A7595': tds92.eq(2).text(),
            'A95115': tds93.eq(2).text(),
            'A115135': tds94.eq(2).text(),
            'A135155': tds95.eq(2).text(),
            'A155': tds96.eq(2).text(),
            #
            'A155A': tr11.eq(2).text(),
            'A155B': tr28.eq(2).text(),
            'A155C': tr45.eq(2).text(),
            'A155D': tr62.eq(2).text(),
            'A155ABCD': '0',
            # B.平均重量_______________________________
            # 'B1': tds88.eq(5).text(),
            # 'B2': tds89.eq(5).text(),
            # 'B3': tds90.eq(5).text(),
            'B1_tw@': '0',
            'B2@': '0',
            'B3_tw@': '0',
            'B3@': '0',
            #
            'B375': '0',
            'B395': '0',
            'B75': tds91.eq(5).text(),
            'B7595': tds92.eq(5).text(),
            'B95115': tds93.eq(5).text(),
            'B115135': tds94.eq(5).text(),
            'B135155': tds95.eq(5).text(),
            'B155': tds96.eq(5).text(),
            #
            'B155A': tr11.eq(5).text(),
            'B155B': tr28.eq(5).text(),
            'B155C': tr45.eq(5).text(),
            'B155D': tr62.eq(5).text(),
            'B155ABCD': '0',
            # C.成交價格_______________________________
            # 'C1': tds88.eq(8).text(),
            # 'C2': tds89.eq(8).text(),
            # 'C3': tds90.eq(8).text(),
            'C1_tw@': '0',
            'C2@': '0',
            'C3_tw@': '0',
            'C3@': '0',
            #
            'C375': '0',
            'C395': '0',
            'C375D': '0',
            'C395D': '0',
            'C75': tds91.eq(8).text(),
            'C7595': tds92.eq(8).text(),
            'C95115': tds93.eq(8).text(),
            'C115135': tds94.eq(8).text(),
            'C135155': tds95.eq(8).text(),
            'C155': tds96.eq(8).text(),
            #
            'C155A': tr11.eq(8).text(),
            'C155B': tr28.eq(8).text(),
            'C155C': tr45.eq(8).text(),
            'C155D': tr62.eq(8).text(),
            'C155ABCD': '0',
            # P.澎湖的9列數據=========================================
            'P1_A': tds71.eq(2).text(),
            'P2_A': tds72.eq(2).text(),
            'P3_A': tds73.eq(2).text(),
            'P75_A': tds74.eq(2).text(),
            'P7595_A': tds75.eq(2).text(),
            'P95115_A': tds76.eq(2).text(),
            'P115135_A': tds77.eq(2).text(),
            'P135155_A': tds78.eq(2).text(),
            'P155_A': tds79.eq(2).text(),
            #
            'P1_B': tds71.eq(5).text(),
            'P2_B': tds72.eq(5).text(),
            'P3_B': tds73.eq(5).text(),
            'P75_B': tds74.eq(5).text(),
            'P7595_B': tds75.eq(5).text(),
            'P95115_B': tds76.eq(5).text(),
            'P115135_B': tds77.eq(5).text(),
            'P135155_B': tds78.eq(5).text(),
            'P155_B': tds79.eq(5).text(),
            #
            'P1_C': tds71.eq(8).text(),
            'P2_C': tds72.eq(8).text(),
            'P3_C': tds73.eq(8).text(),
            'P75_C': tds74.eq(8).text(),
            'P7595_C': tds75.eq(8).text(),
            'P95115_C': tds76.eq(8).text(),
            'P115135_C': tds77.eq(8).text(),
            'P135155_C': tds78.eq(8).text(),
            'P155_C': tds79.eq(8).text(),
        }
        print(f'爬取 {D} 之日行情 OK,{time()-stime}')
        day_data.append(today)
        #
    return day_data


def get_miss_ym(miss_ym, YorM):
    # 第一次進入頁面
    r1 = requests.get(url_pig, headers=headers, verify=cacert)
    r1.encoding = 'utf-8'
    doc1 = pq(r1.text, parser='html')
    r1.close()
    # 按下月/年行情頁籤
    target = {
        'm': "ctl00$ctl00$ContentPlaceHolder_contant$ContentPlaceHolder_contant$LinkButton_query3",
        'y': "ctl00$ctl00$ContentPlaceHolder_contant$ContentPlaceHolder_contant$LinkButton_query4",
    }
    postdata = {
        '__EVENTTARGET': target[YorM],
        '__VIEWSTATE': doc1.find("#__VIEWSTATE").attr('value'),
        '__VIEWSTATEGENERATOR': doc1.find("#__VIEWSTATEGENERATOR").attr('value'),
        '__EVENTVALIDATION': doc1.find("#__EVENTVALIDATION").attr('value'),
    }
    r2 = requests.post(url_pig, headers=headers, data=postdata, verify=cacert)
    r2.encoding = 'utf-8'
    doc2 = pq(r2.text, parser='html')
    r2.close()
    postdata = {
        '__VIEWSTATE': doc2.find("#__VIEWSTATE").attr('value'),
        '__VIEWSTATEGENERATOR': doc2.find("#__VIEWSTATEGENERATOR").attr('value'),
        '__EVENTVALIDATION': doc2.find("#__EVENTVALIDATION").attr('value'),
        'ctl00$ctl00$ContentPlaceHolder_contant$ContentPlaceHolder_contant$CheckBoxList_Market$1': 'H268',  # 宜蘭,新竹,苗栗,花蓮,台灣地區，一次查
        'ctl00$ctl00$ContentPlaceHolder_contant$ContentPlaceHolder_contant$CheckBoxList_Market$3': 'H302',
        'ctl00$ctl00$ContentPlaceHolder_contant$ContentPlaceHolder_contant$CheckBoxList_Market$4': 'H356',
        'ctl00$ctl00$ContentPlaceHolder_contant$ContentPlaceHolder_contant$CheckBoxList_Market$20': 'H955',
        'ctl00$ctl00$ContentPlaceHolder_contant$ContentPlaceHolder_contant$CheckBoxList_Market$21': 'H880',  # 澎湖
        'ctl00$ctl00$ContentPlaceHolder_contant$ContentPlaceHolder_contant$CheckBoxList_Market$22': '%',
        "ctl00$ctl00$ContentPlaceHolder_contant$ContentPlaceHolder_contant$Button_query": "查詢",
    }
    #
    # 開始查詢送出表單
    ym_data = []
    for ym in miss_ym:
        if YorM == 'm':
            y = ym[:4]
            m = ym[-2:].lstrip('0')
            postdata["ctl00$ctl00$ContentPlaceHolder_contant$ContentPlaceHolder_contant$DropDownList_Content3_ThisDate_Year"] = y
            postdata["ctl00$ctl00$ContentPlaceHolder_contant$ContentPlaceHolder_contant$DropDownList_Content3_ThisDate_Month"] = m
            postdata["ctl00$ctl00$ContentPlaceHolder_contant$ContentPlaceHolder_contant$DropDownList_Content3_LastDate_Year"] = y
            postdata["ctl00$ctl00$ContentPlaceHolder_contant$ContentPlaceHolder_contant$DropDownList_Content3_LastDate_Month"] = m
        elif YorM == 'y':
            postdata["ctl00$ctl00$ContentPlaceHolder_contant$ContentPlaceHolder_contant$DropDownList_Content4_ThisDate_Year"] = ym
            postdata["ctl00$ctl00$ContentPlaceHolder_contant$ContentPlaceHolder_contant$DropDownList_Content4_LastDate_Year"] = ym
        #
        r3 = requests.post(url_pig, headers=headers, data=postdata, verify=cacert)
        r3.encoding = 'utf-8'
        doc3 = pq(r3.text, parser='html')
        r3.close()
        # 抓13列
        trs = doc3.find('.tbResult').find('tr')
        # 宜蘭,新竹,苗栗,花蓮的155以上
        tr11 = trs.eq(11).find('td')
        tr28 = trs.eq(28).find('td')
        tr45 = trs.eq(45).find('td')
        tr62 = trs.eq(62).find('td')
        # 澎湖
        tds71 = trs.eq(71).find('td')
        tds72 = trs.eq(72).find('td')
        tds73 = trs.eq(73).find('td')
        tds74 = trs.eq(74).find('td')
        tds75 = trs.eq(75).find('td')
        tds76 = trs.eq(76).find('td')
        tds77 = trs.eq(77).find('td')
        tds78 = trs.eq(78).find('td')
        tds79 = trs.eq(79).find('td')
        # 台灣地區
        tds88 = trs.eq(88).find('td')
        tds89 = trs.eq(89).find('td')
        tds90 = trs.eq(90).find('td')
        tds91 = trs.eq(91).find('td')
        tds92 = trs.eq(92).find('td')
        tds93 = trs.eq(93).find('td')
        tds94 = trs.eq(94).find('td')
        tds95 = trs.eq(95).find('td')
        tds96 = trs.eq(96).find('td')
        #
        this_ym = {
            'date': ym,
            # 'wd': wd_map[datetime.strptime(D, date_format).weekday()],
            # A.成交頭數_______________________________
            'A1_tw': tds88.eq(2).text(),
            'A2': tds89.eq(2).text(),
            'A3_tw': tds90.eq(2).text(),
            'A3': '0',
            'A375': '0',  # 75+
            'A395': '0',  # 95+
            'A75': tds91.eq(2).text(),
            'A7595': tds92.eq(2).text(),
            'A95115': tds93.eq(2).text(),
            'A115135': tds94.eq(2).text(),
            'A135155': tds95.eq(2).text(),
            'A155': tds96.eq(2).text(),
            #
            'A155A': tr11.eq(2).text(),
            'A155B': tr28.eq(2).text(),
            'A155C': tr45.eq(2).text(),
            'A155D': tr62.eq(2).text(),
            'A155ABCD': '0',
            # B.平均重量_______________________________
            'B1_tw': tds88.eq(5).text(),
            'B2': tds89.eq(5).text(),
            'B3_tw': tds90.eq(5).text(),
            'B3': '0',
            'B375': '0',
            'B395': '0',
            'B75': tds91.eq(5).text(),
            'B7595': tds92.eq(5).text(),
            'B95115': tds93.eq(5).text(),
            'B115135': tds94.eq(5).text(),
            'B135155': tds95.eq(5).text(),
            'B155': tds96.eq(5).text(),
            'B155ABCD': '0',
            #
            'B155A': tr11.eq(5).text(),
            'B155B': tr28.eq(5).text(),
            'B155C': tr45.eq(5).text(),
            'B155D': tr62.eq(5).text(),
            # C.成交價格_______________________________
            'C1_tw': tds88.eq(8).text(),
            'C2': tds89.eq(8).text(),
            'C3_tw': tds90.eq(8).text(),
            'C3': '0',
            'C375': '0',
            'C395': '0',
            'C375D': '0',
            'C395D': '0',
            'C75': tds91.eq(8).text(),
            'C7595': tds92.eq(8).text(),
            'C95115': tds93.eq(8).text(),
            'C115135': tds94.eq(8).text(),
            'C135155': tds95.eq(8).text(),
            'C155': tds96.eq(8).text(),
            'C155ABCD': '0',
            #
            'C155A': tr11.eq(8).text(),
            'C155B': tr28.eq(8).text(),
            'C155C': tr45.eq(8).text(),
            'C155D': tr62.eq(8).text(),
            # P.澎湖的9列數據=========================================
            'P1_A': tds71.eq(2).text(),
            'P2_A': tds72.eq(2).text(),
            'P3_A': tds73.eq(2).text(),
            'P75_A': tds74.eq(2).text(),
            'P7595_A': tds75.eq(2).text(),
            'P95115_A': tds76.eq(2).text(),
            'P115135_A': tds77.eq(2).text(),
            'P135155_A': tds78.eq(2).text(),
            'P155_A': tds79.eq(2).text(),
            #
            'P1_B': tds71.eq(5).text(),
            'P2_B': tds72.eq(5).text(),
            'P3_B': tds73.eq(5).text(),
            'P75_B': tds74.eq(5).text(),
            'P7595_B': tds75.eq(5).text(),
            'P95115_B': tds76.eq(5).text(),
            'P115135_B': tds77.eq(5).text(),
            'P135155_B': tds78.eq(5).text(),
            'P155_B': tds79.eq(5).text(),
            #
            'P1_C': tds71.eq(8).text(),
            'P2_C': tds72.eq(8).text(),
            'P3_C': tds73.eq(8).text(),
            'P75_C': tds74.eq(8).text(),
            'P7595_C': tds75.eq(8).text(),
            'P95115_C': tds76.eq(8).text(),
            'P115135_C': tds77.eq(8).text(),
            'P135155_C': tds78.eq(8).text(),
            'P155_C': tds79.eq(8).text(),
        }
        print(f'爬取 {ym} 之{YorM=="m" and "月" or "年"}行情 OK')
        ym_data.append(this_ym)
        sleep(random()+0.1)
    return ym_data


def df_miss_7595(df_miss):
    '''
        兩種標準之計算
    '''
    # 九個欄位: 台灣地區扣掉澎湖
    # cols = ['1', '2', '3', '75', '7595', '95115', '115135', '135155', '155']
    small = 0.0000012345
    ym = len(df_miss['date'][0]) <= 7
    cols = ['75', '7595', '95115', '115135', '135155', '155']  # 日行情時，75以前的欄位不做計算，由價量比較網頁值直接填入
    # (1)成交頭數 A 處理==================================================
    for col in cols:
        df_miss[f'A{col}'] = df_miss[f'A{col}']-df_miss[f'P{col}_A']
    if ym:
        df_miss['A3'] = df_miss['A3_tw']-df_miss['P3_A']
    # 不含澎湖的規格豬頭數計算
    df_A75 = df_miss.loc[:, 'A7595':'A135155']
    df_A155 = df_miss.loc[:, 'A155A':'A155D']
    # 兩種標準計算
    df_miss['A375'] = df_A75.sum(axis=1) + df_A155.sum(axis=1)
    df_miss['A395'] = df_miss['A375'] - df_miss['A7595']

    # (2)平均重量 B 處理==================================================
    for col in cols:
        T_weight = (df_miss[f'A{col}'] + df_miss[f'P{col}_A'])*df_miss[f'B{col}']
        P_weight = df_miss[f'P{col}_A']*df_miss[f'P{col}_B']
        #
        df_miss[f'B{col}'] = (T_weight - P_weight)/df_miss[f'A{col}'].replace(0, small)
    if ym:
        T_weight = df_miss['A3_tw']*df_miss['B3_tw']
        P_weight = df_miss['P3_A']*df_miss['P3_B']
        df_miss['B3'] = (T_weight-P_weight)/df_miss['A3'].replace(0, small)
    # 不含澎湖的規格豬平均重量計算
    df_A75 = df_miss.loc[:, 'A7595':'A135155']
    df_B75 = df_miss.loc[:, 'B7595':'B135155']
    df_A95 = df_miss.loc[:, 'A95115':'A135155']
    df_B95 = df_miss.loc[:, 'B95115':'B135155']
    df_A155 = df_miss.loc[:, 'A155A':'A155D']
    df_B155 = df_miss.loc[:, 'B155A':'B155D']
    # 以A區塊的欄名統一，之後相乘
    df_B75.columns = df_A75.columns
    df_B95.columns = df_A95.columns
    df_B155.columns = df_A155.columns
    # 兩種標準計算
    tmp75 = (df_A75 * df_B75).sum(axis=1)
    tmp95 = (df_A95 * df_B95).sum(axis=1)
    tmp155 = (df_A155 * df_B155).sum(axis=1)
    df_miss['B375'] = (tmp75 + tmp155) / df_miss['A375'].replace(0, small)
    df_miss['B395'] = (tmp95 + tmp155) / df_miss['A395'].replace(0, small)

    # (3)成交價格 C 處理==================================================
    for col in cols:
        P_weight = df_miss[f'P{col}_A']*df_miss[f'P{col}_B']
        P_total = P_weight*df_miss[f'P{col}_C']
        #
        T_weight = df_miss[f'A{col}']*df_miss[f'B{col}'] + P_weight
        T_total = T_weight*df_miss[f'C{col}']
        #
        df_miss[f'C{col}'] = (T_total - P_total)/(T_weight - P_weight).replace(0, small)
    if ym:
        P_weight = df_miss['P3_A']*df_miss['P3_B']  # 澎湖規格豬總重
        P_total = P_weight*df_miss['P3_C']  # 澎湖規格豬總金額
        #
        T_weight = df_miss['A3_tw']*df_miss['B3_tw']
        T_total = T_weight*df_miss['C3_tw']
        #
        df_miss['C3'] = (T_total - P_total)/(T_weight - P_weight).replace(0, small)
    #
    # 不含澎湖的規格豬平均價格計算
    df_A75 = df_miss.loc[:, 'A7595':'A135155']
    df_B75 = df_miss.loc[:, 'B7595':'B135155']
    df_C75 = df_miss.loc[:, 'C7595':'C135155']
    df_A95 = df_miss.loc[:, 'A95115':'A135155']
    df_B95 = df_miss.loc[:, 'B95115':'B135155']
    df_C95 = df_miss.loc[:, 'C95115':'C135155']
    df_A155 = df_miss.loc[:, 'A155A':'A155D']
    df_B155 = df_miss.loc[:, 'B155A':'B155D']
    df_C155 = df_miss.loc[:, 'C155A':'C155D']
    # 以A區塊的欄名統一，之後相乘
    df_B75.columns = df_A75.columns
    df_C75.columns = df_A75.columns
    df_B95.columns = df_A95.columns
    df_C95.columns = df_A95.columns
    df_B155.columns = df_A155.columns
    df_C155.columns = df_A155.columns
    # 兩種標準計算
    tmp75 = (df_A75 * df_B75 * df_C75).sum(axis=1)
    tmp95 = (df_A95 * df_B95 * df_C95).sum(axis=1)
    tmp155 = (df_A155 * df_B155 * df_C155).sum(axis=1)
    df_miss['C375'] = (tmp75 + tmp155) / (df_miss['A375']*df_miss['B375']).replace(0, small)
    df_miss['C395'] = (tmp95 + tmp155) / (df_miss['A395']*df_miss['B395']).replace(0, small)
    #
    if ym:
        df_miss['C375D'] = df_miss['C375'] - df_miss['C3']
        df_miss['C395D'] = df_miss['C395'] - df_miss['C3']
    # (4)155以上 total處理==================================================
    df_miss['A155ABCD'] = df_A155.sum(axis=1)
    df_miss['B155ABCD'] = (df_A155 * df_B155).sum(axis=1)/df_miss['A155ABCD'].replace(0, small)
    df_miss['C155ABCD'] = (df_A155 * df_B155 * df_C155).sum(axis=1)/(df_miss['A155ABCD']*df_miss['B155ABCD']).replace(0, small)
    #
    return df_miss

# 用BaseModel時，django requests要送json過來


@app.post("/pig/", tags=["規格豬"])
def pig(dr: DateRange):
    """
    # 日行情
    # (1)輸入查詢條件:
    - **sd**: 開始日期
    - **ed**: 結束日期
    # (2)回傳欄位說明:
    以下均扣掉澎湖
    - A: A開頭的，為成交頭數(深紅)。B: 平均重量(kg)(橘色)。C: 平均價格(元/kg)(藍色)
    - A1,A2,A3: 成交總數,成交總數(不含澎湖),規格豬。BC類推
    - A3@,B3@,C3@: 單日多市場價量比較的不含澎湖的規格豬的頭數/均重/均價
    - A375,A395: 含75-95之舊算法(淺綠), 不含75-95之舊算法(深綠)。可與A3 (紅字)比對
    - C375D,C395D: C375-C3, C395-C3，亦即兩種算法與規格豬欄位之差
    - A75,...,A155: 數字代表對應之重量範圍
    - A155A,...,A155D: 最後四個代表155以上的四個縣市來源(宜蘭,新竹,苗栗,花蓮)
    - 最後的P則為澎湖

    """
    stime = time()
    # (1)從post取得日期字串
    sd = dr.sd
    ed = dr.ed
    OK, errmsg = isocheck(sd, ed, date_format)
    if not OK:
        print(errmsg)
        return errmsg
    # (2)篩選日期
    pig_csv = 'pig.csv'
    df = pd.read_csv(pig_csv)
    # df['date'] = pd.to_datetime(df['date']).dt.date  # 轉timeseries做篩選
    where = (sd <= df['date']) & (df['date'] <= ed)
    df_in = df[where]

    # (3)找出miss date，有就重爬
    miss_date = pd.date_range(start=sd, end=ed).astype(str).difference(df_in['date']).tolist()
    if miss_date:
        # (1)缺少的日期去爬蟲
        # df_miss = pd.DataFrame(get_miss_date(miss_date))
        df_miss = pd.DataFrame(async_get_miss(get_miss_date, miss_date))
        # A1 開始 floatint
        df_miss.iloc[:, 2:] = df_miss.iloc[:, 2:].applymap(floatint)
        # 進行7595兩種標準之計算
        df_miss = df_miss_7595(df_miss)
        # (2)再去單日多市場價量比較爬蟲，然後插入df_miss
        # df_miss_T = pd.DataFrame(get_miss_date_T(miss_date)).applymap(floatint)
        df_miss_T = pd.DataFrame(async_get_miss(get_miss_date_T, miss_date)).applymap(floatint)
        cols = ['1_tw@', '2@', '3_tw@', '3@']
        for col_pre in list('ABC'):
            cols_ = [f'{col_pre}{col}' for col in cols]
            df_miss.loc[:, cols_] = df_miss_T.loc[:, cols_]
        df_miss['C375D'] = df_miss['C375'] - df_miss['C3@']
        df_miss['C395D'] = df_miss['C395'] - df_miss['C3@']
        df_miss.iloc[:, 2:] = df_miss.iloc[:, 2:].applymap(floatint)
        print('單日多市場價量插入df_miss完成')
        # (3)加新資料重存csv
        df.append(df_miss).sort_values('date').drop_duplicates(subset=['date']).reset_index(drop=True).applymap(zero).round(2).to_csv(pig_csv, index=False)
        print(f'{pig_csv}更新完成')
        # (4)組織回傳
        resdata = df_in.append(df_miss).sort_values('date').drop_duplicates(subset=['date']).reset_index(drop=True).applymap(zero).round(2).to_dict('records')
    else:
        resdata = df_in.to_dict('records')
    #
    # __________________________________________________________
    duration = time() - stime
    print(f'duration={duration}')
    res = {
        'log': {
            'now': datetime.now().strftime(f'{date_format}_{time_format}'),
            'duration': duration,
            'postdata': dr.dict(),
            'miss_date': miss_date,
        },
        'resdata': resdata,
    }
    return res  # json.dumps(res, indent=4)


@app.get("/pig_m/", tags=["規格豬"])
def pig_m(sd: str = last_m, ed: str = last_m):
    """
    # 月行情
    # (1)輸入查詢條件:
    - **sd**: 開始月
    - **ed**: 結束月
    # (2)回傳欄位說明:
    - A: A開頭的，為成交頭數(深紅)。B: 平均重量(kg)(橘色)。C: 平均價格(元/kg)(藍色)
    - A1,A2,A3: 成交總數,成交總數(不含澎湖),規格豬。BC類推
    - A375,A395: 含75-95之舊算法(淺綠), 不含75-95之舊算法(深綠)。可與A3 (紅字)比對
    - C375D,C395D: C375-C3, C395-C3，亦即兩種算法與規格豬欄位之差
    - A75,...,A155: 數字代表對應之重量範圍
    - A155A,...,A155D: 最後四個代表155以上的四個縣市來源(宜蘭,新竹,苗栗,花蓮)
    """
    stime = time()
    # (1) 檢查
    OK, errmsg = isocheck(sd, ed, month_format)
    if not OK:
        print(errmsg)
        return errmsg
    # (2) 篩選月份
    pig_m_csv = 'pig_m.csv'
    df = pd.read_csv(pig_m_csv)
    where = (sd <= df['date']) & (df['date'] <= ed)
    df_in = df[where]
    # (3) 找出 miss_m，有就重爬
    miss_m = pd.date_range(start=sd, end=ed, freq='MS').astype(str).str[:7].difference(df_in['date']).tolist()
    if miss_m:
        # 缺少的月份去爬蟲
        df_miss = pd.DataFrame(get_miss_ym(miss_m, 'm'))
        # 月沒有wd欄位，從 1 開始 floatint
        df_miss.iloc[:, 1:] = df_miss.iloc[:, 1:].applymap(floatint)
        # 進行7595兩種標準之計算
        df_miss = df_miss_7595(df_miss)
        df_miss.iloc[:, 1:] = df_miss.iloc[:, 1:].applymap(floatint)
        # 加新資料重存csv
        df.append(df_miss).sort_values('date').drop_duplicates(subset=['date']).reset_index(drop=True).applymap(zero).round(2).to_csv(pig_m_csv, index=False)
        # 組織回傳
        resdata = df_in.append(df_miss).sort_values('date').drop_duplicates(subset=['date']).reset_index(drop=True).applymap(zero).round(2).to_dict('records')
    else:
        resdata = df_in.to_dict('records')
    # __________________________________________________
    duration = time() - stime
    print(f'duration={duration}')
    res = {
        'log': {
            'now': datetime.now().strftime(f'{date_format}_{time_format}'),
            'duration': duration,
            'getdata': f'sd={sd},ed={ed}',
            'miss_m': miss_m,
        },
        'resdata': resdata,
    }
    return res


@app.get("/pig_y/", tags=["規格豬"])
def pig_y(sd: str = last_y, ed: str = last_y):
    """
    # 年行情
    # (1)輸入查詢條件:
    - **sd**: 開始年
    - **ed**: 結束年
    # (2)回傳欄位說明:
    - A: A開頭的，為成交頭數(深紅)。B: 平均重量(kg)(橘色)。C: 平均價格(元/kg)(藍色)
    - A1,A2,A3: 成交總數,成交總數(不含澎湖),規格豬。BC類推
    - A375,A395: 含75-95之舊算法(淺綠), 不含75-95之舊算法(深綠)。可與A3 (紅字)比對
    - C375D,C395D: C375-C3, C395-C3，亦即兩種算法與規格豬欄位之差
    - A75,...,A155: 數字代表對應之重量範圍
    - A155A,...,A155D: 最後四個代表155以上的四個縣市來源(宜蘭,新竹,苗栗,花蓮)
    """
    stime = time()
    # (1) 檢查
    OK, errmsg = isocheck(sd, ed, year_format)
    if not OK:
        print(errmsg)
        return errmsg
    # (2) 篩選年份
    pig_y_csv = 'pig_y.csv'
    df = pd.read_csv(pig_y_csv, dtype={'date': str})
    where = (sd <= df['date']) & (df['date'] <= ed)
    df_in = df[where]
    # (3) 找出 miss_y，有就重爬
    miss_y = pd.date_range(start=sd, end=ed, freq='YS').astype(str).str[:4].difference(df_in['date']).tolist()
    if miss_y:
        # 缺少的年去爬蟲
        df_miss = pd.DataFrame(get_miss_ym(miss_y, 'y'))
        # 年沒有wd欄位，從 1 開始 floatint
        df_miss.iloc[:, 1:] = df_miss.iloc[:, 1:].applymap(floatint)
        # 進行7595兩種標準之計算
        df_miss = df_miss_7595(df_miss)
        df_miss.iloc[:, 1:] = df_miss.iloc[:, 1:].applymap(floatint)
        # 加新資料重存csv
        df.append(df_miss).sort_values('date').drop_duplicates(subset=['date']).reset_index(drop=True).applymap(zero).round(2).to_csv(pig_y_csv, index=False)
        # 組織回傳
        resdata = df_in.append(df_miss).sort_values('date').drop_duplicates(subset=['date']).reset_index(drop=True).applymap(zero).round(2).to_dict('records')
    else:
        resdata = df_in.to_dict('records')
    # __________________________________________________
    duration = time() - stime
    print(f'duration={duration}')
    res = {
        'log': {
            'now': datetime.now().strftime(f'{date_format}_{time_format}'),
            'duration': duration,
            'getdata': f'sd={sd},ed={ed}',
            'miss_y': miss_y,
        },
        'resdata': resdata,
    }
    return res
