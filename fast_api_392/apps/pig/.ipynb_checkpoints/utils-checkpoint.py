from time import sleep, time
from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta
import requests
import asyncio
import aiohttp
from pyquery import PyQuery as pq
import os
from os import path
from random import random, uniform
#
from .config import (
    cwd,
    date_format, month_format, year_format, wd_map,
    cacert, headers,
    url_pig, url_pig2
)


def write_file(fpath, text):
    with open(fpath, 'w') as f:
        f.write(text)


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


async def aio_get(session, url: str):
    async with session.get(url, headers=headers) as r:
        return await r.text(encoding='utf8')


async def aio_post(session, url: str, postdata):
    async with session.post(url, headers=headers, data=postdata) as r:
        return await r.text(encoding='utf8')


async def get_single_d(D: str):
    stime = time()
    await asyncio.sleep(uniform(0.1, 1))
    # 每個session重造connector
    async with aiohttp.ClientSession(connector=aiohttp.TCPConnector(verify_ssl=cacert)) as session:
        # (1)第一次進入頁面
        r1 = await aio_get(session, url_pig)
        doc1 = pq(r1, parser='html')
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
            'ctl00$ctl00$ContentPlaceHolder_contant$ContentPlaceHolder_contant$TextBox_Content1_ThisDate': D,
            'ctl00$ctl00$ContentPlaceHolder_contant$ContentPlaceHolder_contant$TextBox_Content1_LastDate': D,
        }
        # (2)開始查詢送出表單
        r2 = await aio_post(session, url_pig, postdata)
        doc2 = pq(r2, parser='html')
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
        return today


async def get_miss_ds(miss_date: list):
    '''日行情'''
    # 開始查詢送出表單
    tasks = [asyncio.create_task(get_single_d(D)) for D in miss_date]
    day_data = await asyncio.gather(*tasks)
    #     
    return day_data
