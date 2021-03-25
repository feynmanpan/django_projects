import asyncio
#
from apps.ips.tasks import tasks_list as ips_tasks
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


#################### tasks_list ################################
tasks_list = [
    # (loopme, [1]),
    # (loopme2, [1]),
] + ips_tasks
