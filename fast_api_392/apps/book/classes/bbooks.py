# -*- coding: utf-8 -*-
import aiohttp
import asyncio
import re
from pyquery import PyQuery as pq
from datetime import datetime
#
from apps.book.classes.abookbase import BOOKBASE
import apps.ips.config as ipscfg
from apps.ips.config import ips_csv_path, dtype, cacert, timeout, headers
from apps.book.config import dt_format
###################################################


class BOOKS(BOOKBASE):
    info_default = {
        "bookid": "0010770978"  # 刺殺騎士團長
    }
    # 博客來單書頁
    url_target_prefix = "https://www.books.com.tw/products/"

    def __init__(self, **init):
        super().__init__(**init)

    @property
    def proxy(self):
        if ips_cycle := ipscfg.ips_cycle:
            tmp = next(ips_cycle)
            return f"http://{tmp['ip']}:{tmp['port']}"

    async def update_info(self):
        connector = aiohttp.TCPConnector(ssl=cacert)
        TO = aiohttp.ClientTimeout(total=timeout)
        url_target = f"{self.url_target_prefix}{self.info['bookid']}"
        update = {}
        try:
            async with aiohttp.ClientSession(connector=connector, timeout=TO) as session:
                async with session.get(url_target, headers=headers, proxy=self.proxy) as r:
                    status = r.status
                    rtext = await r.text(encoding='utf8')
        except asyncio.exceptions.TimeoutError as e:
            update['err'] = 'asyncio.exceptions.TimeoutError'
        except Exception as e:
            update['err'] = str(e)
        else:
            if (status == 200) and re.search(self.info['bookid'], rtext) is not None:
                doc = pq(rtext, parser='html')
                update = {
                    'title': doc.find('.mod.type02_p002.clearfix h1').eq(0).text().strip(),
                    'err': None,
                }
            else:
                update['err'] = f'status={status},rtext={rtext[:100]}'
        finally:
            update['create_dt'] = datetime.today().strftime(dt_format)
            self.info = {**self.info, **update}
            print(self.info)

    def save_info(self):
        pass
