import pandas as pd
import os
from time import time, sleep
#
from .utils import isocheck, get_miss_ds
from .config import (
    date_format,
    month_format,
    year_format,
    pig_csv_path,
)


async def pig_d(sd: str = '2021-03-01', ed: str = '2021-03-17'):
    stime = time()
    # _________________________________________________
    # (1)檢查日期字串格式
    OK, errmsg = isocheck(sd, ed, date_format)
    if not OK:
        print(errmsg)
        return errmsg
    # (2)篩選日期
    df = pd.read_csv(pig_csv_path.d)
    where = (sd <= df['date']) & (df['date'] <= ed)
    df_in = df[where]
    # (3)找出miss date，有就重爬
    miss_date = pd.date_range(start=sd, end=ed).astype(str).difference(df_in['date']).tolist()
    if miss_date:
        resdata = await get_miss_ds(miss_date)
    else:
        resdata = df_in.to_dict('records')
    # _________________________________________________
    duration = time() - stime
    print(f'duration={duration}')
    return resdata
