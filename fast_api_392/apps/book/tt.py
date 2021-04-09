import asyncio


class A:
    @property
    async def a(self):
        await asyncio.sleep(1)
        return 12


async def pp():
    w = A()
    print(await w.a)


asyncio.run(pp())
