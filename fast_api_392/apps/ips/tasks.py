# %load get_bookprice.py
# %run get_bookprice.py
# -*- coding: utf-8 -*-
import asyncio
import requests
import aiohttp
from pyquery import PyQuery as pq
import pandas as pd
import os
import sys
from datetime import datetime
#
from fastapi import Request
# 為了在jupyter中試，從apps開始import
from apps.ips.config import url_free, cacert, cwd, headers, ips_csv, ips_html
from apps.ips.utils import aio_get, write_file
##################################################

async def get_freeproxy(t, once=True):
    while 1:
        await asyncio.sleep(t)
        #
        async with aiohttp.ClientSession(connector=aiohttp.TCPConnector(verify_ssl=cacert)) as session:
            rtext = await aio_get(session, url_free)
            if rtext is not None:
                print('get_freeproxy爬取成功')
                now = datetime.today()
                elite = []
                doc = pq(rtext, parser='html')
                trs = doc.find('table.table').eq(0).find('tr')
                for tr in trs:
                    tds = pq(tr).find('td')
                    level = tds.eq(4).text().strip()
                    if level != 'elite proxy':
                        continue
                    tmp = {
                        'ip': tds.eq(0).text().strip(),
                        'port': tds.eq(1).text().strip(),
                        'level': level,
                        'now': now,
                    }
                    elite.append(tmp)
                # 寫入檔案
                write_file(ips_html, rtext)
                pd.DataFrame(elite).to_csv(ips_csv, index=False)
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
