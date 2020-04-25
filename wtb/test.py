import requests
from pyquery import PyQuery as pq

year = 2020
month = 4
day = 20

url = f'https://aprp.atri.org.tw/dailytrans/daily-report/render/?day={day}&month={month}&year={year}'

header = {'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36'}

r = requests.get(url,
                 headers=header,
                 # data={'k':'村'},
                 # proxies=proxies,
                 # cookies=cookies,
                 timeout=15)
r.encoding = 'utf8'
rtext=r.text

