from abc import ABC, ABCMeta, abstractmethod
import re
from collections import namedtuple
import os
import itertools
from typing import Dict, Any
#
import pandas as pd
#
import apps.ips.config as ipscfg
##########################################################


class VALIDATE(ABCMeta):
    def __new__(cls, name, bases, class_dict):
        # 不驗證 BOOKBASE
        if (base := bases[0]) != object:
            # 檢查子類info_default的key
            info_cols = base.info_cols
            info_default = class_dict.get('info_default', {})
            set0 = set(info_cols)
            set1 = set(info_default.keys())
            if (rest := set1-set0) != base.empty:
                raise KeyError(f'info_default中，欄位{rest}不在BOOKBASE的info_cols裡面')
            # 造子類的預設info並assign，以子類類名為store名稱
            info_default = base.info_default | info_default
            info_default[base.INFO_COLS.store] = name
            class_dict['info_default'] = info_default
        #
        return super().__new__(cls, name, bases, class_dict)


class BOOKBASE(object, metaclass=VALIDATE):
    info_cols = [
        'store',
        'bookid', 'isbn10', 'isbn13',
        'title', 'title2',
        'author',
        'publisher', 'pub_dt', 'lang',
        'price_list', 'price_sale',
        'spec', 'intro', 'comment',
        'url_book', 'url_vdo', 'url_cover',
        'err',
        'create_dt',
    ]
    INFO_COLS = namedtuple('INFO_COLS', info_cols)(*info_cols)
    #
    info_default = dict.fromkeys(info_cols, None)  # dict(zip(info_cols, [None]*len(info_cols)))
    #
    bookid_pattern = ''
    int_pattern = '^[0-9]+$'
    float_pattern = r'^[0-9]*\.*[0-9]*$'
    int_err = 1234567
    float_err = 4567.89
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
            if (rest := set1-set0) != self.empty:
                raise KeyError(f'assign給info的欄位{rest}不在BOOKBASE的info_cols裡面')
            # (2)檢查bookid格式
            bid = val.get(self.INFO_COLS.bookid)
            bid_pn = self.bookid_pattern
            if (bid and bid_pn) and not re.match(bid_pn, bid):
                raise ValueError(f'bookid="{bid}" 不符合bookid_pattern="{bid_pn}"')
            # (3)檢查定價售價
            if (PL := val.get(self.INFO_COLS.price_list)) and not isinstance(PL, int):
                raise ValueError(f'price_list="{PL}" 不為int')
            if (PS := val.get(self.INFO_COLS.price_sale)) and not (isinstance(PS, float) or isinstance(PS, int)):
                raise ValueError(f'price_sale="{PS}" 不為float/int')
        #
        self.__dict__[name] = val
        # object.__setattr__(self, name, val)

    @property
    def proxy(self):
        ippt = None
        if ips_cycle := ipscfg.ips_cycle:
            ippt = next(ips_cycle)
        elif os.path.isfile(ipscfg.ips_csv_path):
            df = pd.read_csv(ipscfg.ips_csv_path, usecols=['ip', 'port'])
            ipscfg.ips_cycle = itertools.cycle(df.to_dict('records'))
            ippt = next(ipscfg.ips_cycle)
        #
        return ippt and f"http://{ippt['ip']}:{ippt['port']}" or None

    @abstractmethod
    def update_info(self):
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
