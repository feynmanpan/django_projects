import graphene
from graphene import ObjectType, Field, String, List, Int, Float
from graphene_django import DjangoObjectType, DjangoListField
#
from .models import Bookinfo, Bookprice, Store
#
import numpy as np
import pandas as pd
import re


# 1.建立各model對應的Type，及客製Type _____________________________


class Store_PriceSale(ObjectType):
    books = Float()
    shopee = Float()
    mollie = Float()
    rtimes = Float()
    ruten = Float()
    momo = Float()
    taaze = Float()
    elite = Float()
    ks = Float()
    tenlong = Float()
    linking = Float()
    cwgv = Float()
    yahoo = Float()
    iread = Float()
    cite = Float()
    sanmin = Float()
    #
    priceSaleMean = Float(description="有查詢的店家且非null售價之平均")


class BookinfoType(DjangoObjectType):
    class Meta:
        model = Bookinfo
        fields = ("bookid", "isbn", "title", "author", "publisher", "price_list")  # 能查詢的field

    # 客製欄位
    priceList = Float(description="定價")
    priceSale = Field(Store_PriceSale, description="各家平台的售價及非負平均(0為免費，null為抓不到售價)")

    def resolve_priceList(self, info, **kwargs):
        # query有查詢此欄位才會執行此resolve，self是resolve_books回傳的queryset中每一個Bookinfo物件
        return self.price_list  # 把字串轉Float

    def resolve_priceSale(self, info, **kwargs):
        df = info.variable_values['df_all_priceSales']
        df = df[df.isbn == self.isbn][['store', 'price_sale']]
        QS = dict(df.to_dict('split')['data'])
        #
        QS['books'] = self.price_sale
        QS = {k: float(v) if v != "" else None for k, v in QS.items()}
        # 實際查詢店家的非None(null)平均
        stores = [f.name.value for f in info.field_asts[0].selection_set.selections]
        stores = list(set(stores) - set(['priceSaleMean']))
        if stores:
            tmp = [v for k, v in QS.items() if v is not None and k in stores]
            if tmp:
                QS['priceSaleMean'] = np.mean(tmp)
        #
        return QS


class BookpriceType(ObjectType):
    isbn = String()
    store = String()
    priceSale = Float()
    urlBook = String()

    def resolve_priceSale(self, info, **kwargs):
        return self['priceSale'] or None  # 把字串轉Float，None>null

    def resolve_urlBook(self, info, **kwargs):
        return self['urlBook'] or None


# 2.建立Query _____________________________


class Query(ObjectType):
    books = List(BookinfoType, title=String(), isbn=String(), description="書籍資訊及各家售價")
    booksCount = Int(description="books查到的筆數")
    priceSales = List(BookpriceType, isbn=String(), description='只查詢售價，isbn參數能以逗號分隔輸入如"9789571371870,9789869435109"')
    serviceMail = String(description="有問題請找: feynmanpan@gmail.com")

    def resolve_books(self, info, **kwargs):
        # 取出query中books中的實際查詢欄位，及參數where
        fields = [f.name.value for f in info.field_asts[0].selection_set.selections]
        fields = map(lambda x: re.sub('([a-z])([A-Z])', r'\1_\2', x).lower(), fields)  # priceList/priceSale還原為price_list/price_sale
        title = kwargs.get('title', '')
        isbn = kwargs.get('isbn', '')
        # ORM篩選欄位及where後回傳
        QS = Bookinfo.objects.filter(title__contains=title, isbn__contains=isbn).only(*fields)
        # 存到info.variable_values
        all_isbn = list(QS.values_list('isbn', flat=True))
        info.variable_values['df_all_priceSales'] = pd.DataFrame(Bookprice.objects.filter(isbn__in=all_isbn).values('isbn', 'store', 'price_sale'))
        info.variable_values['booksCount'] = QS.count()
        return QS

    def resolve_booksCount(self, info, **kwargs):
        try:
            return info.variable_values['booksCount']
        except:
            return 0

    def resolve_priceSales(self, info, **kwargs):
        isbn = kwargs.get('isbn', '')
        fields = ['isbn', 'store', 'price_sale', 'url_book']
        fields2 = ['isbn', 'price_sale', 'bookid']
        fields_final = ['isbn', 'store', 'priceSale', 'urlBook']
        #
        if isbn:
            QS = Bookprice.objects.filter(isbn__in=isbn.split(",")).values(*fields)
        else:
            QS = Bookprice.objects.all().values(*fields)  # 空字串不篩選
        #
        df = pd.DataFrame(QS).rename(columns={'price_sale': fields_final[2], 'url_book': fields_final[3]})
        # 增加博客來的售價
        QS2 = Bookinfo.objects.filter(isbn__in=df['isbn']).values(*fields2)
        df2 = pd.DataFrame(QS2).rename(columns={'price_sale': fields_final[2], 'bookid': fields_final[3]}).assign(store='books')
        df2['urlBook'] = 'https://www.books.com.tw/products/' + df2['urlBook']
        df2 = df2[fields_final]
        df2 = df2.append(df).sort_values('isbn')
        return df2.to_dict('record')

    def resolve_serviceMail(self, info, **kwargs):
        return 'feynmanpan@gmail.com'
