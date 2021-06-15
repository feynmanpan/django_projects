# -*- coding: utf-8 -*-
from asyncio.tasks import create_task
import aiohttp
import aiofiles
import asyncio
import re
import json
import os
from pyquery import PyQuery as pq
from datetime import datetime
from time import time
from typing import Dict, Any, Callable, Awaitable, Coroutine, Optional, Union
from PIL import Image
import pytesseract
import copy
import itertools
import sqlalchemy as sa
#
from apps.sql.config import dbwtb
from apps.book.model import INFO
from apps.book.classes.abookbase import BOOKBASE
from apps.book.utils import write_file
#
import apps.ips.config as ipscfg
from apps.ips.config import headers


###################################################


class MOLLIE(BOOKBASE):
    '''茉莉'''
    info_default = {
        "bookid": "9789571345826",  # 大騙局
    }
    #
    bookid_pattern = BOOKBASE.isbn_pattern  # 茉莉的書號就以isbn為書號
    #
    url_search = 'http://www.mollie.com.tw/Mobile/Books.asp'
    search_OK = [
        '目前各分店皆無此書籍/影音商品',
        '因商品擺放於賣場，隨時會被售出',
    ]
    stock_sep = '_'
    stock_none = '查無此書'
    page_err = []
    #
    formdata = {
        'Action': 'BookSerach',
        'BookName': '',
        'Author': '',
        'Publisher': '',
        'BarCode': '',
        'XCHK': 'Y',
    }
    # __________________________________________________________

    def __init__(self, **init):
        # 書號=isbn
        is_isbn13 = len(self.bid) == 13
        init['isbn10'] = ((not is_isbn13) and self.bid) or None
        init['isbn13'] = (is_isbn13 and self.bid) or None
        #
        super().__init__(**init)

    async def update_info(self, proxy: Optional[str] = None, uid: Optional[int] = None, db=dbwtb):
        self._stime = time()
        # ======== 只留 uid=1 進行爬蟲，其他則等待及結束 =======
        if (uid := await super().update_info(uid=uid, proxy=proxy)) != 1:
            return self._update_result
        # ===================================================
        try:
            # 抓庫存資訊
            print('post 茉莉查詢頁面---------------------')
            #
            formdata = self.formdata | {'BarCode': self.bid}
            async with self.ss.post(self.url_search, headers=headers, proxy=self.now_proxy, data=formdata) as r:
                status = r.status
                rtext = (await r.text(encoding='big5')).replace('big5', 'utf8')
                #
                if status == 200:
                    self._enter_bookpage = [s in rtext for s in self.search_OK]  # 要回傳有無庫存
        except asyncio.exceptions.TimeoutError as e:
            self._update['err'] = 'asyncio.exceptions.TimeoutError'
        except Exception as e:
            self._update['err'] = str(e)
        else:
            if sum(self._enter_bookpage) == 1:
                # 確定有查詢結果
                print('bookpage_handle ---------------------')
                result = self.bookpage_handle(rtext)
                self.update_handle(result)
            else:
                self.page_err_handle(rtext, status)
        finally:
            return await self.update_final(uid=uid, db=db)

    def bookpage_handle(self, rtext) -> Dict[str, Any]:
        doc = pq(rtext, parser='html')
        td = doc.find("section#A table.table.table-bordered.text tr").eq(1).find('td').eq(0)
        # ________________________________________
        if self._enter_bookpage == [False, True]:
            title = td.find('span').eq(0).text().strip()
            stock = self.stock_sep.join(sorted(re.findall('..店', td.text().strip())))
        else:
            stock = self.stock_none
        #
        return locals()
