from fastapi import FastAPI, Request
from pydantic import BaseModel, Field
from starlette.middleware.cors import CORSMiddleware
import pandas as pd
import numpy as np
import requests
from random import random
from pyquery import PyQuery as pq
from time import sleep
from datetime import datetime, timedelta
import json
import math
import re
#
app = FastAPI(
    title="FastAPI",
    description="",
    version="1.0.0",
    openapi_tags=[
        {
            'name': '規格豬',
            'description': '抓取 [畜產行情資訊網](http://ppg.naif.org.tw/naif/MarketInformation/Poultry/TranStatistics.aspx)【毛豬行情查詢】之日行情(月年行情待補)',
            # "externalDocs": {
            #     "description": "來源",
            #     "url": "http://ppg.naif.org.tw/naif/MarketInformation/Poultry/TranStatistics.aspx",
            # },
        },
        {
            'name': '測試',
            'description': '測試用',
        }
    ],
)
app.add_middleware(CORSMiddleware, allow_origins=['*'])

#


@app.get("/test/", tags=["測試"])
async def test():
    return {"message": "Hello World!! YES! no nonono!!!"}


# 規格豬
date_format = '%Y-%m-%d'
wd_map = {
    0: '(一)',
    1: '(二)',
    2: '(三)',
    3: '(四)',
    4: '(五)',
    5: '(六)',
    6: '(日)',
}


class DateRange(BaseModel):
    sd: str = Field(title='開始日期', example="2021-01-01")
    ed: str = Field(title='結束日期', example="2021-01-05")

    class Config:
        schema_extra = {
            "example": {
                "sd": "2021-01-01",
                "ed": "2021-01-05",
            }
        }


def floatint(x):
    x = str(x).replace(',', '').replace('-', '0').replace(' ', '')
    x = x or '0'
    xf = float(x)
    xn = int(xf)
    return xf > xn and xf or xn


def get_miss_date(miss_date):
    url = "https://ppg.naif.org.tw/naif/MarketInformation/Pig/FPSCompare.aspx"

    #
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.135 Safari/537.36',
    }
    # 第一次進入頁面
    r1 = requests.get(url, headers=headers)
    r1.encoding = 'utf-8'
    doc1 = pq(r1.text, parser='html')
    r1.close()
    #
    postdata = {
        '__VIEWSTATE': doc1.find("#__VIEWSTATE").attr('value'),
        '__VIEWSTATEGENERATOR': doc1.find("#__VIEWSTATEGENERATOR").attr('value'),
        '__EVENTVALIDATION': doc1.find("#__EVENTVALIDATION").attr('value'),
        'ctl00$ctl00$ContentPlaceHolder_contant$ContentPlaceHolder_contant$CheckBoxList_Market$1': 'H268',  # 宜蘭,新竹,苗栗,花蓮,台灣地區，一次查
        'ctl00$ctl00$ContentPlaceHolder_contant$ContentPlaceHolder_contant$CheckBoxList_Market$3': 'H302',
        'ctl00$ctl00$ContentPlaceHolder_contant$ContentPlaceHolder_contant$CheckBoxList_Market$4': 'H356',
        'ctl00$ctl00$ContentPlaceHolder_contant$ContentPlaceHolder_contant$CheckBoxList_Market$20': 'H955',
        'ctl00$ctl00$ContentPlaceHolder_contant$ContentPlaceHolder_contant$CheckBoxList_Market$22': '%',
        "ctl00$ctl00$ContentPlaceHolder_contant$ContentPlaceHolder_contant$Button_query": "查詢",
    }
    # 開始查詢送出表單
    day_data = []
    for D in miss_date:
        postdata['ctl00$ctl00$ContentPlaceHolder_contant$ContentPlaceHolder_contant$TextBox_Content1_ThisDate'] = D
        postdata["ctl00$ctl00$ContentPlaceHolder_contant$ContentPlaceHolder_contant$TextBox_Content1_LastDate"] = D
        r2 = requests.post(url, headers=headers, data=postdata)
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
        # 台灣地區
        tds71 = trs.eq(71).find('td')
        tds72 = trs.eq(72).find('td')
        tds73 = trs.eq(73).find('td')
        tds74 = trs.eq(74).find('td')
        tds75 = trs.eq(75).find('td')
        tds76 = trs.eq(76).find('td')
        tds77 = trs.eq(77).find('td')
        tds78 = trs.eq(78).find('td')
        tds79 = trs.eq(79).find('td')
        #
        today = {
            'date': D,
            'wd': wd_map[datetime.strptime(D, date_format).weekday()],
            # A.成交頭數_______________________________
            'A1': tds71.eq(2).text(),
            'A2': tds72.eq(2).text(),
            'A3': tds73.eq(2).text(),
            'A375': '0',  # 75+
            'A395': '0',  # 95+
            'A75': tds74.eq(2).text(),
            'A7595': tds75.eq(2).text(),
            'A95115': tds76.eq(2).text(),
            'A115135': tds77.eq(2).text(),
            'A135155': tds78.eq(2).text(),
            'A155': tds79.eq(2).text(),
            #
            'A155A': tr11.eq(2).text(),
            'A155B': tr28.eq(2).text(),
            'A155C': tr45.eq(2).text(),
            'A155D': tr62.eq(2).text(),
            # B.平均重量_______________________________
            'B1': tds71.eq(5).text(),
            'B2': tds72.eq(5).text(),
            'B3': tds73.eq(5).text(),
            'B375': '0',
            'B395': '0',
            'B75': tds74.eq(5).text(),
            'B7595': tds75.eq(5).text(),
            'B95115': tds76.eq(5).text(),
            'B115135': tds77.eq(5).text(),
            'B135155': tds78.eq(5).text(),
            'B155': tds79.eq(5).text(),
            #
            'B155A': tr11.eq(5).text(),
            'B155B': tr28.eq(5).text(),
            'B155C': tr45.eq(5).text(),
            'B155D': tr62.eq(5).text(),
            # C.成交價格_______________________________
            'C1': tds71.eq(8).text(),
            'C2': tds72.eq(8).text(),
            'C3': tds73.eq(8).text(),
            'C375': '0',
            'C395': '0',
            'C375D': '0',
            'C395D': '0',
            'C75': tds74.eq(8).text(),
            'C7595': tds75.eq(8).text(),
            'C95115': tds76.eq(8).text(),
            'C115135': tds77.eq(8).text(),
            'C135155': tds78.eq(8).text(),
            'C155': tds79.eq(8).text(),
            #
            'C155A': tr11.eq(8).text(),
            'C155B': tr28.eq(8).text(),
            'C155C': tr45.eq(8).text(),
            'C155D': tr62.eq(8).text(),
        }
        print(D)
        day_data.append(today)
        sleep(random()+0.3)
        #
    return day_data


@app.post("/pig/", tags=["規格豬"])
async def pig(dr: DateRange):
    """
    # 日行情
    ## (1)輸入查詢條件:
    - **sd**: 開始日期
    - **ed**: 結束日期
    ## (2)回傳欄位說明:
    - A: A開頭的，為成交頭數(深紅)。B: 平均重量(kg)(橘色)。C: 平均價格(元/kg)(藍色)
    - A1,A2,A3: 成交總數,成交總數(不含澎湖),規格豬。BC類推
    - A375,A395: 含75-95之舊算法(淺綠), 不含75-95之舊算法(深綠)。可與A3 (紅字)比對
    - C375D,C395D: C375-C3, C395-C3，亦即兩種算法與規格豬欄位之差
    - A75,...,A155: 數字代表對應之重量範圍
    - A155A,...,A155D: 最後四個代表155以上的四個縣市來源(宜蘭,新竹,苗栗,花蓮) 

    """
    # 從post取得時間範圍
    dr = dr.dict()
    sd = dr['sd']
    ed = dr['ed']
    # -----------------------------------------------
    iso = '^[0-9]{4}-[0-9]{2}-[0-9]{2}$'
    m1 = re.search(iso, sd)
    m2 = re.search(iso, ed)
    if not m1 or not m2:
        return {'error': '日期格式不符合ISO之標準，如2021-01-02'}
    #
    today = datetime.today().date()
    yesday = today - timedelta(1)
    yesday = datetime.strftime(yesday, '%Y-%m-%d')
    # print(ed, yesday)
    if ed > yesday:
        return {'error': f'結束日期最晚到昨天{yesday}'}
    # -----------------------------------------------
    # 篩選日期
    pig_csv = 'pig.csv'
    df = pd.read_csv(pig_csv)
    df['date'] = pd.to_datetime(df['date'])  # 轉timeseries做篩選
    where = df['date'] >= sd
    where &= df['date'] <= ed
    df_in = df[where]
    df_in['date'] = df_in['date'].astype(str)  # 轉回字串

    # 找出miss date，有就重爬
    dr_all = pd.date_range(start=sd, end=ed).strftime(date_format)
    miss_date = list(set(dr_all) - set(df_in['date']))
    miss_date.sort()
    if miss_date:
        day_data = get_miss_date(miss_date)
        df_miss = pd.DataFrame(day_data)
        df_miss.iloc[:, 2:] = df_miss.iloc[:, 2:].applymap(floatint)
        #
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
        # A 三種試算與規格豬網頁值的比較
        df_miss['A375'] = df_A75.sum(axis=1) + df_A155.sum(axis=1)
        df_miss['A395'] = df_miss['A375'] - df_miss['A7595']
        df_miss['A375'] = df_miss['A375'].replace(0, 0.0001)
        df_miss['A395'] = df_miss['A395'].replace(0, 0.0001)
        # B
        df_miss['B375'] = ((df_A75 * df_B75).sum(axis=1) + (df_A155 * df_B155).sum(axis=1)) / df_miss['A375']
        df_miss['B395'] = ((df_A95 * df_B95).sum(axis=1) + (df_A155 * df_B155).sum(axis=1)) / df_miss['A395']
        df_miss['B375'] = df_miss['B375'].replace(0, 0.0001)
        df_miss['B395'] = df_miss['B395'].replace(0, 0.0001)
        # C
        df_miss['C375'] = ((df_A75 * df_B75 * df_C75).sum(axis=1) + (df_A155 * df_B155 * df_C155).sum(axis=1)) / (df_miss['A375']*df_miss['B375'])
        df_miss['C395'] = ((df_A95 * df_B95 * df_C95).sum(axis=1) + (df_A155 * df_B155 * df_C155).sum(axis=1)) / (df_miss['A395']*df_miss['B395'])
        df_miss['C375D'] = df_miss['C375'] - df_miss['C3']
        df_miss['C395D'] = df_miss['C395'] - df_miss['C3']
        #
        df_all = df_in.append(df_miss).sort_values('date').reset_index(drop=True).applymap(lambda x: x != 0 and x or 0).round(2)
        resdata = df_all.to_dict('records')
        #
        df['date'] = df['date'].astype(str)
        df.append(df_all).drop_duplicates(subset=['date']).sort_values('date').reset_index(drop=True).to_csv(pig_csv, index=False)
    else:
        resdata = df_in.to_dict('records')
    #
    # __________________________________________________________
    res = {
        'log': {
            'now': datetime.now().strftime(f'{date_format}_%H:%M:%S'),
            'postdata': dr,
            'miss_date': miss_date,
        },
        'resdata': resdata,
    }
    return res  # json.dumps(res, indent=4)
