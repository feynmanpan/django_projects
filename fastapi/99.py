import time
import asyncio
# 同步函數


def A(a):
    print(a)
    time.sleep(6/a)
    print(f'over_{a}')
    return [a]


def async_A():
    stime = time.time()
    print(stime)
    #
    loop = asyncio.get_event_loop()
    #

    async def run_A(t):
        return await loop.run_in_executor(None, A, t)
    #
    tasks = []
    for t in range(1, 6):
        task = loop.create_task(run_A(t))
        tasks.append(task)
    #
    result = loop.run_until_complete(asyncio.gather(*tasks))
    loop.close()
    #
    print(time.time() - stime)
    return result


print(async_A())
