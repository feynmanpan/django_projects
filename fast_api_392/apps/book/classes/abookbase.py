from abc import ABC, ABCMeta, abstractmethod
import re
#
import apps.ips.config as ipscfg
##########################################################


class VALIDATE(ABCMeta):
    def __new__(cls, name, bases, class_dict):
        # 不驗證 BOOKBASE
        if (base := bases[0]) != object:
            # 從 BOOKBASE 抽info_cols
            info_cols = base.info_cols
            # 檢查info_default的key
            info_default = class_dict.get('info_default', {})
            set0 = set(info_cols)
            set1 = set(info_default.keys())
            if (rest := set1-set0) != base.empty:
                raise KeyError(f'info_default中，欄位{rest}不在BOOKBASE的info_cols裡面')
            # 造子類的預設info並assign，以子類類名為store名稱
            info_default = dict(zip(info_cols, [None]*len(info_cols))) | class_dict.get('info_default', {})
            info_default['store'] = name
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
    #
    info_default = {}
    empty = set()
    #
    bookid_pattern = {
        'BOOKS': '^[a-zA-Z0-9]{10}$',  # 博客來書號格式
    }
    int_pattern = '^[0-9]+$'
    float_pattern = r'^[0-9]*\.*[0-9]*$'
    comment_js_pattern = '<script type="text/javascript">(.|\n)+?</script>'

    def __init__(self, **init):
        # 檢查初始化引數
        set0 = set(self.info_cols)
        set1 = set(init.keys())
        if (rest := set1-set0) != self.empty:
            raise KeyError(f'初始化欄位{rest}不在BOOKBASE的info_cols裡面')
        # 更新初始化
        self.info = self.info_default | init
        # 檢查bookid格式
        bid = self.info['bookid']
        bid_pn = self.bookid_pattern[self.info['store']]
        if not re.match(bid_pn, bid):
            raise ValueError(f'bookid="{bid}" 不符合bookid_pattern="{bid_pn}"')

    @property
    def proxy(self):
        if ips_cycle := ipscfg.ips_cycle:
            tmp = next(ips_cycle)
            return f"http://{tmp['ip']}:{tmp['port']}"

    @abstractmethod
    def update_info(self):
        pass

    @abstractmethod
    def save_info(self):
        pass
