from typing import Optional, Callable
from time import sleep
from datetime import datetime
import asyncio
import nest_asyncio
#
from fastapi import Request
from fastapi.responses import HTMLResponse, ORJSONResponse
from fastapi.templating import Jinja2Templates
from starlette.templating import _TemplateResponse
#####################################################

templates = Jinja2Templates(directory="templates")


def test(request: Request, p: str = 'path', q: str = 'query')->_TemplateResponse:
    print(f"p={p},q={q}")
    print(f'locals()={locals()}')
    # _______________________________________________
    if request.query_params.get('q') is None:
        print('qyery "q" 要有!')
    #
    tmp1 = set(locals().keys())
    tmp2 = set(request.query_params.keys())
    tmpd = tmp2-tmp1
    for k in tmpd:
        print(f'多的query參數: {k}')
    # _______________________________________________
    context = {
        'request': request,  # 一定要有
        'req_str': type(request),
        "p": p,
        "q": q,
    }
    # return f"q={q},a={a}"
    # return ORJSONResponse([{"item_id": "Foo"}])
    # return HTMLResponse("<p>2</p>")
    # print(type(templates.TemplateResponse("test.html", context)))
    return templates.TemplateResponse("test.html", context)

#################### schedule ################################


loopme_count = 0
loopme_count2 = 0


async def loopme(t):
    global loopme_count
    if loopme_count < 1:
        loopme_count = 1
        while 1:
            await asyncio.sleep(t)
            t += 1
            print(f'現在時間 = {datetime.now()}')
    else:
        tmp = f'已有一個loopme: loopme_count={loopme_count}'
        return tmp


async def loopme2(t):
    global loopme_count2
    if loopme_count2 < 1:
        loopme_count2 = 1
        while 1:
            await asyncio.sleep(t)
            print(f'{datetime.now()}')
    else:
        tmp = f'已有一個loopme2: loopme_count2={loopme_count2}'
        return tmp


nest_asyncio.apply()
loop = asyncio.get_event_loop()
tasks_list = [
    (loopme, 1),
    (loopme2, 1),
]
tasks = []


async def runtasks():
    global tasks
    if not tasks:
        tasks = [asyncio.ensure_future(task(t)) for task, t in tasks_list]
        loop.run_until_complete(asyncio.wait(tasks))
    else:
        tmp = f'已有{tasks}執行中'
        print(tmp)
        return tmp
