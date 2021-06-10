import asyncio
from datetime import datetime
import sqlalchemy as sa
#
from .config import objs_max, del_store_objs_delta, dt_format
from .classes.zimportall import BOOKBASE, BOOKS
#
from apps.book.model import INFO
from apps.book.config import q_size
from apps.sql.config import dbwtb

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
    '''書號queue無窮put'''
    while 1:
        bid = next(cycle)
        await queue.put(bid)
        print(f'bid_Queue_put {bid}')


async def BOOKS_bid_Queue_put(t):
    '''創造博客來三種書號的無窮put'''
    await asyncio.sleep(t)
    #
    prefixes = BOOKS.bid_prefixes
    digits = BOOKS.bid_digits
    # 根據前綴數量，造對應數量的cycle, queue
    BOOKS.bid_Cs = [BOOKS.bid_cycle(prefix=p, digits=digits, start=0) for p in prefixes]
    BOOKS.bid_Qs = [asyncio.Queue(q_size) for _ in prefixes]
    # 每組CQ各自task
    for C, Q in zip(BOOKS.bid_Cs, BOOKS.bid_Qs):
        c = bid_Queue_put(C, Q)
        asyncio.create_task(c)


async def BOOKS_bid_get_loop(t):
    '''對博客來三種書號的無窮爬蟲'''
    await asyncio.sleep(t)
    #
    while 1:
        # 三個書號一組
        bids = [await Q.get() for Q in BOOKS.bid_Qs]
        # 確認DB是否有書號
        cs = [INFO.bookid, INFO.err]
        w1 = INFO.store == 'BOOKS'
        w2 = INFO.bookid.in_(bids)
        #
        query = sa.select(cs).where(w1 & w2)
        rows = await dbwtb.fetch_all(query)
        # DB有已經爬過的書號時，進行篩選，有些不重爬
        if rows:
            tmp = [r['bookid'] for r in rows if r['err'] not in BOOKS.page_err]
            if tmp:
                bids = tmp
            else:
                # 全篩掉就下一組
                continue
        # 剩下的書號進行重爬 ________________________________________________________
        tasks = []
        for bid in bids:
            book = BOOKS(bookid=bid)
            c = book.update_info()
            tasks.append(asyncio.create_task(c))

        await asyncio.wait(tasks)


###############################################################################
tasks_list = [
    (del_store_objs, [del_store_objs_delta]),
    (BOOKS_bid_Queue_put, [0.5]),
    (BOOKS_bid_get_loop, [1]),
]
###############################################################################
