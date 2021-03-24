from datetime import datetime
import asyncio
from time import sleep
#
from config import get_freeproxy_delta
import apps.ips.config
from apps.ips.tasks import get_freeproxy
########################################################


async def loopme(t):
    cnt = 0
    # global ips_cycle
    while 1:
        await asyncio.sleep(t)
        # t += 1
        cnt += 1
        # ips_cycle = cnt
        print(f'cnt_1 = {cnt}')


async def loopme2(t):
    cnt = 0
    while 1:
        await asyncio.sleep(t)
        cnt += 1
        print(f'loopme2 = {cnt}')


async def loop_next_ips(t):
    while 1:
        await asyncio.sleep(t)
        if apps.ips.config.ips_cycle:
            ips = next(apps.ips.config.ips_cycle)
            print(f'next_ips = {ips}')
        else:
            print(f'next_ips = _____')

#################### tasks_list ################################

#
tasks_list = [
    # (loopme, [1]),
    # (loopme2, [1]),
    # (loop_next_ips, [3]),
    (get_freeproxy, [get_freeproxy_delta, False]),
]
