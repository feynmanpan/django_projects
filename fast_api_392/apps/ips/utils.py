import asyncio
import aiohttp
import re
import random
#
from .config import (
    cacert,
    headers, ipcols, maxN,
    proxy_checkurls, timeout, check_atleast, sampleN
)


def write_file(fpath, text):
    with open(fpath, 'w') as f:
        f.write(text)


async def aio_get(session, url: str):
    async with session.get(url, headers=headers) as r:
        status_code = r.status
        # print(f'status_code={status_code}')
        if status_code == 200:
            rep = await r.text(encoding='utf8')
        else:
            rep = None
        return status_code, rep


def csv_update(df1, df2):
    # 保留500筆
    return df1.append(df2).sort_values(by=ipcols, ascending=True).drop_duplicates(subset=ipcols[:2]).reset_index(drop=True)[:maxN]


class CHECK_PROXY:

    def __init__(self, ip, port, now):
        self.ip = ip
        self.port = port
        self.now = now
        self.proxy = f"http://{ip}:{port}"  # aiohttp只支援http的proxy
        self._isGood = []

    async def check(self, proxy_checkurl):
        connector = aiohttp.TCPConnector(ssl=cacert)
        TO = aiohttp.ClientTimeout(total=timeout)
        ans = False
        try:
            await asyncio.sleep(random.randint(0, sampleN))
            async with aiohttp.ClientSession(connector=connector, timeout=TO) as session:
                async with session.get(proxy_checkurl, headers=headers, proxy=self.proxy) as r:
                    status = r.status
                    rtext = await r.text() # r.text(encoding='utf8') 
        except Exception as err:
            # print('err=',err)
            pass
        else:
            ans = (status == 200) and re.search(self.ip, rtext) is not None
        finally:
            self._isGood.append(ans)

    @property
    async def isGood(self):
        tasks = [asyncio.create_task(self.check(url)) for url in random.sample(proxy_checkurls, sampleN)]
        await asyncio.wait(tasks)
        p = None
        if sum(self._isGood) >= check_atleast:
            p = {
                'ip': self.ip,
                'port': self.port,
                'now': self.now,
            }
        return p

    @classmethod
    async def get_good_proxys(cls, ippts: list):
        tasks = [asyncio.create_task(cls(*ippt).isGood) for ippt in ippts]
        #
        return [p for p in await asyncio.gather(*tasks) if p]        
