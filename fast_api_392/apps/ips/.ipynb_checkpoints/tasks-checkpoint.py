import asyncio
import requests
import aiohttp
from pyquery import PyQuery as pq
import pandas as pd
import os
from datetime import datetime
#
from fastapi import Request
#
from .config import url_free, cacert, cwd, headers, ips_csv, ips_html
from .utils import aio_get, write_file


async def get_freeproxy(t, once=True):
    while 1:
        await asyncio.sleep(t)
        print('get_freeproxy')
        #
        async with aiohttp.ClientSession(connector=aiohttp.TCPConnector(verify_ssl=cacert)) as session:
            r = await aio_get(session, url_free)
            if r is not None:
                now = datetime.today()
                elite = []
                doc = pq(r, parser='html')
                trs = doc.find('table.table').eq(0).find('tr')
                for tr in trs:
                    tr = pq(tr)
                    level = tr.find('td').eq(4).text().strip()
                    if level != 'elite proxy':
                        continue
                    tmp = {
                        'ip': tr.find('td').eq(0).text().strip(),
                        'port': tr.find('td').eq(1).text().strip(),
                        'level': level,
                        'now': now,
                    }
                    elite.append(tmp)
                # 寫入檔案
                write_file(ips_html, r)
                pd.DataFrame(elite).to_csv(ips_csv, index=False)
        if once:
            break
print(__name__)
if __name__ == '__main__':
    print(333)
    loop = asyncio.get_event_loop()
    task = loop.create_task(get_freeproxy(1))
    loop.run_until_complete(task)
else:
    print(567)
