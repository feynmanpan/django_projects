import asyncio
#


async def a(y):
    await asyncio.sleep(y)
    if y == 0:
        raise ValueError(1111)
        print(2222222222)
    print(999, y)
    return y


async def b(tasks):
    print(await asyncio.gather(*tasks))
#
loop = asyncio.get_event_loop()
#
t1 = loop.create_task(a(1))
t2 = loop.create_task(a(0))
#
loop.run_until_complete(b([t1, t2]))
# loop.run_until_complete(asyncio.wait([t1, t2]))
print(222)
