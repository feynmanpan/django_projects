from typing import Optional, Callable
from typing import get_type_hints
#
from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse, ORJSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from starlette.templating import _TemplateResponse
#
from views_5002 import test
#####################################################


app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")


def path_get(url: str, func: Callable):
    # return_class = get_type_hints(func).get('return')
    # if return_class is not None:
    #     print('this')
    #     return app.get(url, response_class=return_class)(func)
    # else:
    #     print('that')
    #     return app.get(url)(func)
    return app.get(url)(func)


#################### urlpattern ################################
path_get("/test/{p}", test)
