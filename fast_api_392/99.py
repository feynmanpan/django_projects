import asyncio
import time
from time import sleep


async def say_after(delay,   what):
    await asyncio.sleep(delay)
    print(what)


async def main1(a, b):
    print(f"started at {time.strftime('%X')}")
    loop = asyncio.get_event_loop()
    print(12345, loop.is_running())
    # time.sleep

    task1 = asyncio.create_task(say_after(2, 'AA'))
    task2 = asyncio.create_task(say_after(1, 'BBB'))
    # await task2
    # await task1
    # await asyncio.sleep(1)
    print(f"finished at {time.strftime('%X')}")


# async def out():
#     await main1(1, 'ww')

loop = asyncio.get_event_loop()

# loop.create_task(main1(1, 'ww'))
# task1 = loop.create_task(say_after(2, 'AA'))
# task2 = loop.create_task(say_after(1, 'BBB'))
loop.run_until_complete(main1(1, 'ww'))
# loop.run_until_complete(asyncio.wait([task1, task2]))
print(888)
print(f'loop.is_running={loop.is_running()}')
# loop.run_forever()
print(999)
