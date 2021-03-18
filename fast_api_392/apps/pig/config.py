
from collections import namedtuple
import os
import aiohttp
###########################################################


# 規格豬
cacert = True
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.135 Safari/537.36',
}
url_pig = "https://ppg.naif.org.tw/naif/MarketInformation/Pig/FPSCompare.aspx"
url_pig2 = "http://ppg.naif.org.tw/naif/MarketInformation/Pig/TranStatistics.aspx"  # 單日多市場價量比較
#
cwd = os.path.dirname(os.path.realpath(__file__))
dmy = ['d', 'm', 'y']
pig_csv_path = namedtuple('pig_csv', dmy)(*[os.path.join(cwd, f'pig_{tmp}.csv') for tmp in dmy])

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
