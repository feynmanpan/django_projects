# -*- coding: utf-8 -*-
import aiohttp
import asyncio
import re
from pyquery import PyQuery as pq
#
from apps.book.classes.abookbase import BOOK_BASE
import apps.ips.config as ipscfg
from apps.ips.config import ips_csv_path, dtype, cacert, timeout, headers
###################################################


class BOOKS(BOOK_BASE):
    url_target_prefix = "https://www.books.com.tw/products/"
    bookid = "0010770978"  # 刺殺騎士團長

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    @property
    def proxy(self):
        if ips_cycle := ipscfg.ips_cycle:
            tmp = next(ips_cycle)
            return f"http://{tmp['ip']}:{tmp['port']}"

    async def get_info(self):
        url_target = f"{self.url_target_prefix}{self.bookid}"
        connector = aiohttp.TCPConnector(ssl=cacert)
        TO = aiohttp.ClientTimeout(total=timeout)
        proxy = self.proxy
        info = None
        try:
            async with aiohttp.ClientSession(connector=connector, timeout=TO) as session:
                async with session.get(url_target, headers=headers, proxy=proxy) as r:
                    status = r.status
                    rtext = await r.text(encoding='utf8')
        except asyncio.exceptions.TimeoutError as e:
            print('asyncio.exceptions.TimeoutError')
        except Exception as e:
            print(str(e))
        else:
            if (status == 200) and re.search(self.bookid, rtext) is not None:
                doc = pq(rtext, parser='html')
                info = {
                    'title': doc.find('.mod.type02_p002.clearfix h1').eq(0).text().strip(),
                }
            else:
                print(status, rtext)
        finally:
            print(info)

    def save_info(self):
        pass
