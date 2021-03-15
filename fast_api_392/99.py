import asyncio
# import nest_asyncio
import time
from time import sleep

async def say_after(delay, what):
    print('sss1',delay,id(asyncio.get_event_loop()))
    print('sss2',delay,id(asyncio.get_running_loop()))
    print(789,len([task for task in asyncio.all_tasks()]))
    await asyncio.sleep(delay)
    print(222,delay)
#     asyncio.get_event_loop().stop()

async def main1(a,b):
    print(a,b)
    print('main1',id(asyncio.get_event_loop()))
    loop = asyncio.get_event_loop()
#     print(456,asyncio.all_tasks.__sizeof__())
    
#     loop.run_forever()
    print(12345,loop.is_running())

    task1 = loop.create_task(
        say_after(1, a))

    task2 = loop.create_task(
        say_after(2, b))
#     await task2
#     await task1
    print(f"started at {time.strftime('%X')}")
#     loop.run_until_complete(say_after(1,'ww'))



    
    print(f"finished at {time.strftime('%X')}")

async def out():
    await main1(1,'ww')

loop = asyncio.get_event_loop()
loop.run_until_complete(out())
print(999)
