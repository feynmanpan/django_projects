# netstat -ltnp | grep 6001
# 顯示第一個監聽6001的process
# ps -aux | grep main
# 顯示一共連續三個process，都要kill
#################### import ################################
from typing import Optional, Callable
from typing import get_type_hints
from time import sleep
import asyncio
# import nest_asyncio
#
from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse, ORJSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from starlette.templating import _TemplateResponse
#
import config
from views import maintenance, test


#################### app ################################
app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")
#
def path_get(url: str, func: Callable):
    return app.get(url)(func)


#################### urlpattern ################################
now_mode = config.now_mode
print(f'進入【{now_mode}】模式')
# 維護模式時，所有url都先一律匹配
if now_mode == 'maintenance':
    path_get("/{allurl:path}", maintenance)
#
path_get("/test/{p}", test)