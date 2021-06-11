import asyncio


def A(q: asyncio.Queue):
    print(q)


def B(n: int):
    print(1 + n)


A(asyncio.Queue(1))

B(2)
