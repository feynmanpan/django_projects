
import os
import django
#####################
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'dashboard.settings')
django.setup()
######################
import time
import operator
from datetime import datetime, timedelta
from time import sleep, time
from django.db.models.expressions import RawSQL

from pandas import DataFrame
from collections import OrderedDict
from functools import reduce

from django.utils.translation import ugettext as _
from django.db.models import Q
from django.db.models import Sum, Avg, F, Func, IntegerField

from apps.dailytrans.models import DailyTran
from apps.configs.api.serializers import TypeSerializer
from apps.watchlists.models import WatchlistItem
from apps.configs.models import AbstractProduct
from apps.watchlists.models import Watchlist, WatchlistItem, MonitorProfile
from apps.flowers.models import Flower
from apps.configs.models import Source
from apps.dailytrans.reports.dailyreport import DailyReportFactory
from apps.configs.models import (
    Config,
    AbstractProduct,
    Source,
    Type,
    Chart,
)

class Day(Func):
    function = 'EXTRACT'
    template = '%(function)s(DAY from %(expressions)s)'
    output_field = IntegerField()


class Month(Func):
    function = 'EXTRACT'
    template = '%(function)s(MONTH from %(expressions)s)'
    output_field = IntegerField()


class Year(Func):
    function = 'EXTRACT'
    template = '%(function)s(YEAR from %(expressions)s)'
    output_field = IntegerField()
# ____________________________________________________________________________________


# 1.放大鏡日期
date = datetime(2020, 4, 8)
this_week_start = date - timedelta(6)
this_week_end = date
last_week_start = this_week_start - timedelta(7)
last_week_end = this_week_start - timedelta(1)
print('=====================================')
print('1.放大鏡日期=', date)


# watchlist = Watchlist.objects.get(id=6)
# items = watchlist.children().filter_by_product(product__id=60002)
# typeid=items.values_list('product__type__id', flat=True)
# types = Type.objects.filter_by_watchlist_items(watchlist_items=items)
# print(items)
# print(typeid)
# print(types)
# a=AbstractProduct.objects.filter(parent=None).select_subclasses()
# b=AbstractProduct.objects.filter(parent=None)#.select_subclasses()

# print(a)
# print('______')
# print(b)

# 產生報表

if __name__ ==  '__main__'
    stime = time()
    factory = DailyReportFactory(specify_day=date)
    file_name, file_path = factory()
    etime = time()
    print('日報表=', file_path)
    print('日報表處理時間=', f'{etime-stime}秒')

# # 2.根據放大鏡日期的年月，查所屬監控清單
# watchlist = Watchlist.objects.filter(
#     start_date__year=date.year,
#     start_date__month__lte=date.month,
#     end_date__month__gte=date.month
# ).first()
# print('=====================================')
# print('2.監控清單=', watchlist)

# # 3.根據監控清單，查屬於該清單的因應措施(需有橫列編號row)
# # row有四筆規格豬為null
# monitor = MonitorProfile.objects.filter(watchlist=watchlist, row__isnull=False)
# monitor_nullok = MonitorProfile.objects.filter(watchlist=watchlist)
# print('___________因應措施總品項___________')
# for idx,i in enumerate(monitor):
#     print(f'{idx+1}.{i.product.name}')
# # 大蒜_id為因應措施的pk，看yaml
# # src\fixtures\watchlists\mp-2020h1.yaml
# id = 404
# item = monitor.filter(id=id).first()
# ms = [int(m.name.replace('月', '')) for m in item.months.all()]
# display = item.months.filter(name__icontains=date.month)
# rn = item.row
# print('=====================================')
# print(f'3.因應措施id為{id}之品項=', item)
# print('其顯示月份=', ms)
# print('其顯示月份包含本月的list=', display)
# print('其excel橫列編號=', rn)
# # print('因應措施總筆數=', monitor.count())
# # print('因應措施總筆數_可null=', monitor_nullok.count())


# # 4.根據因應措施的抽象品項(yaml裡定義)，查詢監控品項
# # 監控品項的product再查外鍵的parent，及篩選所屬監控清單
# # 回傳監控品項的抽象品項 & 來源list
# abproduct = item.product
# # items = WatchlistItem.objects.filter(product__parent=abproduct).filter(parent=watchlist)
# items = WatchlistItem.objects.filter_by_product(product=abproduct).filter(parent=watchlist)
# items_product_list = item.product_list()  # [item.product for item in items]
# item_sources = item.sources()
# # item_sources=[]
# # for i in items:
# #     item_sources += i.sources.all()
# # item_sources=list(set(item_sources))
# print('=====================================')
# print('4.抽象品項=', abproduct)
# print(f'上一層物件(parent)屬於{abproduct}且屬於監控清單{watchlist}的監控品項列表=', items)
# # E:\myOneDrive\OneDrive\03_農委會\pan\aprp-master\src\fixtures\watchlists\2020h1.yaml
# print('監控品項列表第一項的id(pk)=', items.first().id)
# print('監控品項列表的所有抽象品項的第一項的id=', items_product_list[0].id)  # 49005
# print('監控品項列表的所有來源=')
# for idx,s in enumerate(item_sources):
#     print(f'{idx+1}.{s}')


# # 5.查詢日交易
# # 根據4.監控品項列表的對應抽象品項，去查日交易
# # 第一次查出後，再篩選來源
# query_set = DailyTran.objects.filter(product__in=items_product_list)
# # print(query_set.order_by('-update_time').first())
# query_set = query_set.filter(source__in=item_sources)
# print('=====================================')
# print('5.篩選監控品項列表及其來源的日交易第一筆=')
# for k,v in query_set.values()[0].items():
#     print(k,'=',v)


# # 6.get_group_by_date_query_set
# if query_set.count():
#     has_volume = query_set.filter(
#         volume__isnull=False).count() / query_set.count() > 0.8
#     has_weight = query_set.filter(
#         avg_weight__isnull=False).count() / query_set.count() > 0.8
# else:
#     has_volume = False
#     has_weight = False

# query_set = query_set.filter(date__range=[last_week_start, this_week_end])
# # 篩選兩周內的日交易總筆數
# N = query_set.count()
# #
# q1 = query_set.values('date').annotate(
#     year=Year('date'),
#     month=Month('date'),
#     day=Day('date')
# )
# q2 = q1.annotate(avg_price=Avg('avg_price')).order_by('date')

# q3 = q2.order_by('date')

# print('=====================================')
# print('6.篩選兩周內的日交易總筆數=', N)
# print('交易量有無_均重有無=', has_volume, has_weight)
# print('根據日期groupby____________')
# for idx,q in enumerate(q3):
#     print(f'{idx+1}.{q}')


