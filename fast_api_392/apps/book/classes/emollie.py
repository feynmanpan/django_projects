from apps.book.classes.abookbase import BOOKBASE


###################################################


class MOLLIE(BOOKBASE):
    '''茉莉'''
    info_default = {
        "bookid": "9789571345826",  # 大騙局
    }
    #
    url_search = 'http://www.mollie.com.tw/Mobile/Books.asp'

    # __________________________________________________________

    def __init__(self, **init):
        super().__init__(**init)

    def update_info(self):
        pass
