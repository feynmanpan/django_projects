from tasks import tasks_list
from starlette.templating import _TemplateResponse
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse, ORJSONResponse
from fastapi import Request, BackgroundTasks
from typing import Optional, Callable
from time import sleep
from datetime import datetime
import asyncio
# import nest_asyncio
# nest_asyncio.apply()
#
#
#####################################################

templates = Jinja2Templates(directory="templates")
startBGT_tasks = None


def maintenance():
    print('點擊維護')
    html = '''
        <h1 style="color:red">維護中</h1>
    '''
    return HTMLResponse(html)


# 沒有await就不要async，一般def會加開thread
async def test(request: Request, p: str, q: str = 'query') -> _TemplateResponse:
    if (plen := len(p)) > 2:
        print(f'path len={plen}')
    # sleep(10)
    await asyncio.sleep(0)
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


async def startBGT():
    global startBGT_tasks
    if not startBGT_tasks:
        startBGT_tasks = [asyncio.create_task(task(t)) for task, t in tasks_list]
        #
        print('開始tasks')
        return '開始_幕後排程'
    else:
        return f'已有_幕後排程: {startBGT_tasks}'
