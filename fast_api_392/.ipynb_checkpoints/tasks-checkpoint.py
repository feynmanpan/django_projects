from datetime import datetime
import asyncio
from time import sleep
# import nest_asyncio


async def loopme(t):
    while 1:
        await asyncio.sleep(t)
        t += 1
        print(f'現在時間 = {datetime.now()}')


async def loopme2(t):
    while 1:
        await asyncio.sleep(t)
#         t += 1
        print(f'loopme2')

#################### tasks_list ################################

tasks_list = [
    (loopme, 1),
    (loopme2, 1),
]
