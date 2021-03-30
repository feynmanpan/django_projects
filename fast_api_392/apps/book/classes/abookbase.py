from abc import ABC, abstractmethod
##########################################################


class BOOKBASE(ABC):
    info_cols = [
        'store',
        'bookid', 'isbn10', 'isbn13',
        'title', 'title2',
        'author',
        'publisher', 'pub_dt', 'lang',
        'price_list', 'price_sale'
        'price_list_ebook', 'price_sale_ebook',
        'spec', 'intro',
        'url_book', 'url_vdo', 'url_cover',
        'err',
        'create_dt',
    ]
    #
    info_class = dict(zip(info_cols, [None]*len(info_cols)))
    info_default = {}
    empty = set()

    def __init__(self, **init):
        set0 = set(self.info_cols)
        set1 = set(init.keys())
        set2 = set(self.info_default.keys())
        if (rest := set1-set0) != self.empty:
            raise KeyError(f'初始化欄位{rest}名稱或不合法')
        if (rest := set2-set0) != self.empty:
            raise KeyError(f'info_default欄位{rest}名稱不合法')
        #
        self.info = {**self.info_class, **self.info_default, **init}
        self.info['store'] = type(self).__name__

    @abstractmethod
    def proxy(self):
        pass

    @abstractmethod
    def update_info(self):
        pass

    @abstractmethod
    def save_info(self):
        pass
