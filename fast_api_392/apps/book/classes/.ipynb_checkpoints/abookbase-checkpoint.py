from abc import ABC, abstractmethod
##########################################################


class BOOK_BASE(ABC):
    cols = [
        'store',
        'bookid', 'isbn10', 'isbn13',
        'title', 'title2',
        'author',
        'publisher', 'pub_dt', 'lang',
        'price_list', 'price_sale'
        'price_list_ebook', 'price_sale_ebook',
        'spec', 'intro',
        'url_book', 'url_vdo', 'url_cover',
        'create_dt',
    ]

    def __init__(self, **kwargs):
        for col in self.cols:
            # 先找參數，再找class變數預設值
            if col == 'store':
                val = type(self).__name__
            else:
                val = kwargs.get(col, None) or type(self).__dict__.get(col, None)
            setattr(self, col, val)

    @abstractmethod
    def proxy(self):
        pass

    @abstractmethod
    def get_info(self):
        pass

    @abstractmethod
    def save_info(self):
        pass
