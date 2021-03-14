from typing import Optional, Callable
from time import sleep
from datetime import datetime
import asyncio
import nest_asyncio
#
from fastapi import Request, BackgroundTasks
from fastapi.responses import HTMLResponse, ORJSONResponse
from fastapi.templating import Jinja2Templates
from starlette.templating import _TemplateResponse
#####################################################

templates = Jinja2Templates(directory="templates")


def maintenance():
    print('點擊維護')
    html = '''
        <h1 style="color:red">維護中</h1>
    '''
    return HTMLResponse(html)

def test(request: Request, p: str, q: str = 'query') -> _TemplateResponse:
    if (plen := len(p)) > 2:
        print(f'path len={plen}')
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