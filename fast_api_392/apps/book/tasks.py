import asyncio
from datetime import datetime
#
from .config import objs_max, del_store_objs_delta, dt_format
from .classes.zimportall import BOOKBASE

###############################################################################


async def del_store_objs(t):
    '''各家class.objs的元素數量限制最多objs_max個'''
    del_cnt = 0
    while 1:
        T = bool(del_cnt) * t
        await asyncio.sleep(T)
        print(f'\n開始處理各家class.objs的元素數量，最多{objs_max}個')
        for store_name, store_cls in BOOKBASE.register_subclasses.items():
            n1 = len(store_cls.objs)
            for bid in list(store_cls.objs.keys()):
                if len(store_cls.objs) > objs_max:
                    if store_cls.objs[bid].uids == 0:
                        del store_cls.objs[bid]
                else:
                    break
            # print(list(store_cls.objs.keys()))
            print(f'{store_name}的objs數量: {n1:>3} >> {len(store_cls.objs):>3}')
        del_cnt += 1
        now = datetime.today().strftime(dt_format)
        print(f'del_store_objs 第{del_cnt}次處理完畢:{now}\n')


###############################################################################
tasks_list = [
    (del_store_objs, [del_store_objs_delta]),
]
###############################################################################
