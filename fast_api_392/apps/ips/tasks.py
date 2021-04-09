# -*- coding: utf-8 -*-
import asyncio
import requests
import aiohttp
from pyquery import PyQuery as pq
import pandas as pd
import os
import sys
from datetime import datetime
import itertools
import random
from time import time
#
from fastapi import Request
# 為了在jupyter中試，從apps開始import
import apps.ips.config as ips_cfg
from apps.ips.config import (
    url_free_cycle, level_https, cacert,
    ips_csv_path, ips_html_path,
    dtype, dt_format,
    ipcols, get_freeproxy_delta,
)
from apps.ips.utils import aio_get, write_file, csv_update, CHECK_PROXY
from .crud import bulk_insert
#
from .model import IPS  # ,tb_ips
from apps.sql.config import dbwtb
###############################################################################


async def get_freeproxy(t, once=True):
    get_freeproxy_cnt = 0
    while 1:
        T = (ips_cfg.ips_cycle and os.path.isfile(ips_csv_path))*t  # 沒有 csv 或 ips_cycle 就馬上爬
        await asyncio.sleep(T)
        stime = time()
        url_free = next(url_free_cycle)
        #
        async with aiohttp.ClientSession(connector=aiohttp.TCPConnector(ssl=cacert)) as session:
            status_code, rtext = await aio_get(session, url_free)
            if status_code == 200 and rtext not in ['', None]:
                doc = pq(rtext, parser='html')
                trs = doc.find('table.table').eq(0).find('tr')
                if trs.size():
                    now = datetime.today().strftime(dt_format)
                    elite = []
                    for tr in trs:
                        tds = pq(tr).find('td')
                        level = tds.eq(4).text().strip()
                        https = tds.eq(6).text().strip()
                        # _________________________________
                        if (level, https) not in level_https:
                            continue
                        # _________________________________
                        tmp = {
                            'ip': tds.eq(0).text().strip(),
                            'port': tds.eq(1).text().strip(),
                            'now': now,
                            'goodcnt': 0,
                        }
                        elite.append(tmp)
                    if not elite:
                        continue
                    # 1 儲存每次撈取的原始頁面 #################################
                    write_file(ips_html_path, rtext)
                    # 2 重存csv: 讀取csv檔案，與最新爬的比較 #################################
                    if os.path.isfile(ips_csv_path):
                        df1 = pd.read_csv(ips_csv_path, dtype=dtype)
                        df2 = pd.DataFrame(elite).astype(dtype)
                        df3 = csv_update(df1, df2)
                    else:
                        df3 = pd.DataFrame(elite).astype(dtype)
                    # 3 檢查代理 #################################
                    ippts = df3[ipcols].values.tolist()  # goodcnt不傳進CHECK_PROXY
                    print(f'\n開始檢查proxy:共 {len(ippts)} 個 ({url_free})')
                    good_proxys = await CHECK_PROXY.get_good_proxys(ippts)
                    print(f'結束檢查proxy: {time()-stime}')
                    random.shuffle(good_proxys)
                    # 4 存 csv #################################
                    df3 = pd.DataFrame(good_proxys).astype(dtype)  # df.sample(frac=1)  # 亂排
                    df3.to_csv(ips_csv_path, index=False)
                    #
                    await bulk_insert(dbwtb, IPS, good_proxys)
                    print(f'bulk_insert ips to db')
                    # 5 更新ips_cycle產生器 #################################
                    ips_cfg.ips_cycle = itertools.cycle(good_proxys)
                    #
                    get_freeproxy_cnt += 1
                    print(f'get_freeproxy 第{get_freeproxy_cnt}次更新成功:{now}')
                    print(f'good_proxys 數量: {len(good_proxys)}\n')
                else:
                    pass
        if once:
            break


###############################################################################
tasks_list = [
    (get_freeproxy, [get_freeproxy_delta, False]),
]
###############################################################################


if __name__ == '__main__':
    try:
        tmp = 'zmqshell' in str(type(get_ipython()))  # 在jupyter
        print(tmp, '在jupyter')
    except Exception:
        loop = asyncio.get_event_loop()
        task = loop.create_task(get_freeproxy(1))
        loop.run_until_complete(task)
else:
    if 0:
        asyncio.create_task(get_freeproxy(3, False))
