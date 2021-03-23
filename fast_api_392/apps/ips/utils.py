import asyncio
from .config import headers


def write_file(fpath, text):
    with open(fpath, 'w') as f:
        f.write(text)


async def aio_get(session, url: str):
    async with session.get(url, headers=headers) as r:
        print(f'r.status={r.status}')
        if r.status == 200:
            return await r.text(encoding='utf8')
        else:
            return None
