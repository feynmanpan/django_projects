from typing import Optional, Callable
#
from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
#
from views_5002 import test
#####################################################


app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")


def path_get(url: str, func: Callable):
    # return app.get(url, response_class=HTMLResponse)(func)
    return app.get(url)(func)


# urlpattern
path_get("/test/{p}", test)
