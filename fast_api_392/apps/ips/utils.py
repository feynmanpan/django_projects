import asyncio
from .config import headers, ipcols, maxN


def write_file(fpath, text):
    with open(fpath, 'w') as f:
        f.write(text)


async def aio_get(session, url: str):
    async with session.get(url, headers=headers) as r:
        status_code = r.status
        # print(f'status_code={status_code}')
        if status_code == 200:
            rep = await r.text(encoding='utf8')
        else:
            rep = None
        return status_code, rep


def csv_update(df1, df2):
    # 保留最新的500筆
    return df1.append(df2).sort_values(by=ipcols, ascending=False).drop_duplicates(subset=ipcols[:2]).reset_index(drop=True)[:maxN]
