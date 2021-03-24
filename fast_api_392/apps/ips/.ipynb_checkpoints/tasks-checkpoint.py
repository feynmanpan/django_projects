# %%writefile get_biggoKW.py
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
#
from fastapi import Request
# 為了在jupyter中試，從apps開始import
import apps.ips.config as ips_cfg
from apps.ips.config import url_free, cacert, ips_csv_path, ips_html_path, dtype, dt_format, ipcols
from apps.ips.utils import aio_get, write_file, csv_update
###############################################################################


async def get_freeproxy(t, once=True):
    get_freeproxy_cnt = 0
    while 1:
        T = (ips_cfg.ips_cycle and os.path.isfile(ips_csv_path))*t  # 沒有 csv 或 ips_cycle 就馬上爬
        await asyncio.sleep(T)
        #
        async with aiohttp.ClientSession(connector=aiohttp.TCPConnector(verify_ssl=cacert)) as session:
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
                        if level != 'elite proxy' or https != 'yes':
                            continue
                        tmp = {
                            'ip': tds.eq(0).text().strip(),
                            'port': tds.eq(1).text().strip(),
                            'level': level,
                            'https': https,
                            'now': now,
                        }
                        elite.append(tmp)
                    # 1 儲存每次撈取的原始頁面
                    write_file(ips_html_path, rtext)
                    # 2 重存csv: 讀取csv檔案，與最新爬的比較
                    if os.path.isfile(ips_csv_path):
                        df1 = pd.read_csv(ips_csv_path, dtype=dtype)
                        df2 = pd.DataFrame(elite).astype(dtype)
                        df3 = csv_update(df1, df2)
                    else:
                        df3 = pd.DataFrame(elite).astype(dtype)
                    df3 = df3.sample(frac=1)  # 亂排
                    df3.to_csv(ips_csv_path, index=False)
                    # 3 更新ips_cycle產生器
                    ips_cfg.ips_cycle = itertools.cycle(df3[ipcols].values.tolist())
                    #
                    get_freeproxy_cnt += 1
                    print(f'get_freeproxy 第{get_freeproxy_cnt}次更新成功:{now}')
                else:
                    pass
        if once:
            break

#
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