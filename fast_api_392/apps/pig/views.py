import pandas as pd
import os
from time import time, sleep
from datetime import datetime, timedelta
from fastapi import Request
#
from .utils import (
    floatint, zero, isocheck,
    get_miss_ds, df_miss_7595,
)
from .config import (
    date_format,
    month_format,
    year_format,
    time_format,
    pig_csv_path,
)

pig_d_count = 0


async def pig_d(request: Request, sd: str = '2021-03-01', ed: str = '2021-03-17'):
    global pig_d_count
    if pig_d_count == 1:
        return 'pig_d 執行中'
    pig_d_count = 1
    #
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
        # 缺少的日期去爬蟲，包括單日多市場價量T
        day_data, day_data_T = await get_miss_ds(miss_date)
        #
        df_miss = pd.DataFrame(day_data)
        df_miss_T = pd.DataFrame(day_data_T).applymap(floatint)
        #
        df_miss.iloc[:, 2:] = df_miss.iloc[:, 2:].applymap(floatint)
        df_miss = df_miss_7595(df_miss)  # 進行7595兩種標準之計算
        #
        cols = ['1_tw@', '2@', '3_tw@', '3@']
        for col_pre in list('ABC'):
            cols_ = [f'{col_pre}{col}' for col in cols]
            df_miss.loc[:, cols_] = df_miss_T.loc[:, cols_]
        df_miss['C375D'] = df_miss['C375'] - df_miss['C3@']
        df_miss['C395D'] = df_miss['C395'] - df_miss['C3@']
        df_miss.iloc[:, 2:] = df_miss.iloc[:, 2:].applymap(floatint)
        print('單日多市場價量插入df_miss完成')
        # 加新資料重存csv
        df.append(df_miss).sort_values('date').drop_duplicates(subset=['date']).reset_index(drop=True).applymap(zero).round(2).to_csv(pig_csv_path.d, index=False)
        print(f'{pig_csv_path.d}更新完成')
        # 組織回傳
        resdata = df_in.append(df_miss).sort_values('date').drop_duplicates(subset=['date']).reset_index(drop=True).applymap(zero).round(2).to_dict('records')
    else:
        resdata = df_in.to_dict('records')
    # _________________________________________________
    res = {
        'log': {
            'now': datetime.now().strftime(f'{date_format}_{time_format}'),
            'duration': time() - stime,
            'query': f'sd={sd}&ed={ed}',
            'query_params': request.query_params,
            'miss_date': miss_date,
        },
        'resdata': resdata,
    }
    print(res['log'])
    pig_d_count = 0
    return res
