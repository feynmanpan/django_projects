# netstat -ltnp | grep 6001
# 顯示第一個監聽6001的process
# ps -aux | grep main
# 顯示一共連續三個process，都要kill
#################### import ################################
from typing import Optional, Callable
import asyncio
#
from fastapi import FastAPI, Request, Depends, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.trustedhost import TrustedHostMiddleware
from fastapi.responses import HTMLResponse, ORJSONResponse
#
import config
from views import test, startBGT
from middlewares import mw_list


#################### app ################################
app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")
#


def path_get(url: str, func: Callable):
    return app.get(url)(func)


def path_MW(func: Callable):
    if func.__name__ == 'trusted_host' and config.allowed_hosts:
        return app.add_middleware(TrustedHostMiddleware, allowed_hosts=config.allowed_hosts)
    return app.middleware("http")(func)


#################### middlewares ################################
print(f'進入【{config.now_mode}】模式')
print(f"allowed_hosts={config.allowed_hosts}")

for mw in mw_list:
    path_MW(mw)


#################### urlpattern ################################
path_get("/test/{p}", test)


#################### schedule ################################
print(f'在main啟動時執行排程: {config.startBGT_atonce}')
if config.startBGT_atonce:
    asyncio.create_task(startBGT())
else:
    path_get("/startBGT", startBGT)
