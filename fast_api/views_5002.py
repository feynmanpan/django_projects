from typing import Optional, Callable
from fastapi import Request
from fastapi.templating import Jinja2Templates
#####################################################

templates = Jinja2Templates(directory="templates")


def test(request: Request, p: str = 'path', q: str = 'query'):
    print(f"p={p},q={q}")
    #
    context = {
        'request': request,  # 一定要有
        'req_str': type(request),
        "p": p,
        "q": q,
    }
    # return f"q={q},a={a}"
    return templates.TemplateResponse("test.html", context)
