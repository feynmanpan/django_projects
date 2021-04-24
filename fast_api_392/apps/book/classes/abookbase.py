from abc import ABC, ABCMeta, abstractmethod
import aiohttp
import asyncio
import re
from collections import namedtuple
import os
import itertools
from typing import Dict, Any, Awaitable, Union
#
import sqlalchemy as sa
import pandas as pd
# from async_property import async_property
#
import apps.ips.config as ipscfg
from apps.ips.config import cacert
from apps.ips.model import IPS  # ,tb_ips
from apps.sql.config import dbwtb
from apps.book.config import (
    timeout,
)
#
##########################################################


class VALIDATE(ABCMeta):
    def __new__(cls, name, bases, class_dict):
        # 不驗證 BOOKBASE
        if (base := bases[0]) != object:
            # 檢查子類info_default的key
            info_cols = base.info_cols
            info_default = class_dict.get('info_default', {})
            if not isinstance(info_default, dict):
                raise TypeError(f'【{name}】的info_default不是dict')
            set0 = set(info_cols)
            set1 = set(info_default.keys())
            if (rest := set1 - set0) != base.empty:
                raise KeyError(f'info_default中，欄位{rest}不在BOOKBASE的info_cols裡面')
            # 造子類的預設info並assign，以子類類名為store名稱
            info_default = base.info_default | info_default
            info_default[base.INFO_COLS.store] = name
            class_dict['info_default'] = info_default
            # 將子類註冊入BOOKBASE
            newcls = super().__new__(cls, name, bases, class_dict)
            base.register_subclasses[name] = newcls
        else:
            newcls = super().__new__(cls, name, bases, class_dict)
        #
        return newcls


class BOOKBASE(object, metaclass=VALIDATE):
    register_subclasses = {}  # 註冊所有子類
    #
    info_cols = [
        'store',
        'bookid', 'isbn10', 'isbn13',
        'title', 'title2',
        'author',
        'publisher', 'pub_dt', 'lang',
        'price_list', 'price_sale',
        'stock',
        'spec', 'intro', 'comment',
        'url_book', 'url_vdo', 'url_cover',
        'err',
        'create_dt',
    ]
    INFO_COLS = namedtuple('INFO_COLS', info_cols)(*info_cols)
    #
    info_default = dict.fromkeys(info_cols, None)  # dict(zip(info_cols, [None]*len(info_cols)))
    update_default = {INFO_COLS.err: None}
    #
    bookid_pattern = ''
    int_pattern = '^[0-9]+$'
    float_pattern = r'^[0-9]*\.*[0-9]*$'
    int_err = 1234567
    float_err = 4567.89
    #
    update_errcnt = 0
    _ss = None
    #
    empty = set()

    def __init__(self, **init):
        # 初始化就檢查info欄位
        self.info: Dict[str, Any] = self.info_default | init

    def __setattr__(self, name, val):
        # 每次info做assign時
        if name == 'info':
            # (0)檢查assign為dict
            if not isinstance(val, dict):
                raise TypeError('assign給info的值不是dict')
            # (1)檢查欄位
            set0 = set(self.info_cols)
            set1 = set(val.keys())
            if (rest := set1 - set0) != self.empty:
                raise KeyError(f'assign給info的欄位{rest}不在BOOKBASE的info_cols裡面')
            # (2)檢查bookid格式
            bid = val.get(self.INFO_COLS.bookid)
            bid_pn = self.bookid_pattern
            if (bid and bid_pn) and not re.match(bid_pn, bid):
                raise ValueError(f'bookid="{bid}" 不符合bookid_pattern="{bid_pn}"')
            # (3)檢查定價售價
            if PL := val.get(self.INFO_COLS.price_list):
                if not isinstance(PL, int) or PL < 0:
                    raise ValueError(f'price_list="{PL}" 需為int，且>0')
            if PS := val.get(self.INFO_COLS.price_sale):
                if not (isinstance(PS, float) or isinstance(PS, int)) or PS < 0:
                    raise ValueError(f'price_sale="{PS}" 需為float/int，且>0')
            #

        self.__dict__[name] = val
        # object.__setattr__(self, name, val)

    @property
    def bid(self):
        '''=bookid'''
        return self.info['bookid']

    @property
    async def proxy(self) -> Union[str, None]:
        '''依序從global/csv/db抓cycle代理，每次get就next'''
        ippt = None
        # 依序從global/csv/db抓cycle
        if ips_cycle := ipscfg.ips_cycle:
            ippt = next(ips_cycle)
        elif os.path.isfile(ipscfg.ips_csv_path):
            rows = pd.read_csv(ipscfg.ips_csv_path, usecols=['ip', 'port']).to_dict('records')
            if rows:
                ipscfg.ips_cycle = itertools.cycle(rows)
                ippt = next(ipscfg.ips_cycle)
        else:
            cs = [
                IPS.ip,
                IPS.port,
            ]
            query = sa.select(cs).order_by('idx')  # .where(tb_ips.columns.id > 100)
            records = await dbwtb.fetch_all(query)
            if records:
                ipscfg.ips_cycle = itertools.cycle([dict(r) for r in records])
                ippt = next(ipscfg.ips_cycle)
        #
        if ippt:
            return f"http://{ippt['ip']}:{ippt['port']}"

    @property
    def ss(self):
        '''session重造或沿用'''
        if self._ss is None:
            connector = aiohttp.TCPConnector(ssl=cacert)
            TO = aiohttp.ClientTimeout(total=timeout)
            self._ss = aiohttp.ClientSession(connector=connector, timeout=TO)
        #
        return self._ss

    @abstractmethod
    def update_info(self):
        '''重新爬蟲，更新self.info'''
        pass

    @abstractmethod
    def save_info(self):
        pass

    # 定價售價統一base處理_________________________________________________________
    def price_list_handle(self, price_list):
        if price_list:
            price_list = not re.match(self.int_pattern, price_list) and self.int_err or int(price_list)
        return price_list

    def price_sale_handle(self, price_sale):
        if price_sale:
            if not re.match(self.float_pattern, price_sale):
                price_sale = self.float_err
            else:
                price_sale = float(price_sale)
                if price_sale == (tmp := int(price_sale)):
                    price_sale = tmp
        return price_sale

    # 爬成功的update統一base處理_________________________________________________________
    def update_handle(self, update, locals_var):
        for col in self.info_cols:
            if (val := locals_var.get(col)) not in ['', None]:
                update[col] = val
        return update

    async def close_ss(self):
        '''關閉session'''
        if self._ss is not None:
            await self._ss.close()
            self._ss = None
