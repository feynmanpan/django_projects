import asyncio
from datetime import datetime
#
from .config import objs_max, del_store_objs_delta, dt_format
from .classes.zimportall import BOOKBASE, BOOKS
from apps.book.config import q_size
###############################################################################


async def del_store_objs(t):
    '''各家class.objs的元素數量限制最多objs_max個'''
    del_cnt = 0
    while 1:
        # T = bool(del_cnt) * t
        await asyncio.sleep(t)
        print(f'\n開始處理各家class.objs的元素數量，最多{objs_max}個')
        for store_name, store_cls in BOOKBASE.register_subclasses.items():
            n1 = len(store_cls.objs)
            for bid in list(store_cls.objs.keys()):
                if len(store_cls.objs) > objs_max:
                    # 刪去沒有在執行update_info的
                    if store_cls.objs[bid].uids == 0:
                        del store_cls.objs[bid]
                else:
                    break
            #
            print(f'{store_name}的objs數量: {n1:>3} >> {len(store_cls.objs):>3}')
        del_cnt += 1
        now = datetime.today().strftime(dt_format)
        print(f'del_store_objs 第{del_cnt}次處理完畢:{now}\n')


async def bid_Queue_put(cycle, queue):
    '''書號queue 無窮 put'''
    while 1:
        bid = next(cycle)
        await queue.put(bid)
        print(f'bid_Queue_put {bid}')


async def BOOKS_bid_Queue_put(t):
    '''博客來三種書號的無窮輸出'''
    await asyncio.sleep(t)
    #
    bid_pattern = BOOKS.bookid_pattern
    prefixs = [p[1:3] for p in bid_pattern.split('|')]
    # 根據前綴數量，造對應數量的cycle, queue
    BOOKS.bid_Cs = [BOOKS.bid_cycle(prefix=p, digits=8, start=0) for p in prefixs]
    BOOKS.bid_Qs = [asyncio.Queue(q_size) for _ in prefixs]
    # 每組CQ各自task
    for C, Q in zip(BOOKS.bid_Cs, BOOKS.bid_Qs):
        c = bid_Queue_put(C, Q)
        asyncio.create_task(c)


###############################################################################
tasks_list = [
    (del_store_objs, [del_store_objs_delta]),
    (BOOKS_bid_Queue_put, [0.5]),
]
###############################################################################
