# netstat -ltnp | grep 6001
# 顯示第一個監聽6001的process
# ps -aux | grep main
# 顯示一共連續三個process，都要kill
# uvicorn main:app --host 0.0.0.0 --port 6001 --reload --ssl-keyfile=/etc/letsencrypt/live/wtb.wtbwtb.tk/privkey.pem --ssl-certfile=/etc/letsencrypt/live/wtb.wtbwtb.tk/cert.pemcrypt/live/wtb.wtbwtb.tk/privkey.pem --ssl-certfile=/etc/letsencrypt/l
#################### import ################################
from typing import Optional, Callable
import asyncio
import os
# _____________________________________________________________________
from fastapi import FastAPI, Request, Depends, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.trustedhost import TrustedHostMiddleware
from fastapi.responses import HTMLResponse, ORJSONResponse
# _____________________________________________________________________
import config
from views import test, startBGT
from middlewares import mw_list
from utils import MSG
# apps
from apps.pig.views import pig_d
#
from apps.ips.config import get_freeproxy_delta
from apps.ips.views import show_freeproxy, get_next_ip, check_proxy
#
from apps.book.classes import zimportall  # 載入所有subclass，使其註冊入BOOKBASE
from apps.book.views import show_books, show_register_subclasses
#
import apps.sql.config as sqlcfg
from apps.sql.views import dbwtb_isconnected
#################### app ################################
app = FastAPI()
app.mount(f"/{config.static}", StaticFiles(directory=config.static), name=config.static)
#


def path_get(url: str, func: Callable):
    return app.get(url)(func)


def path_MW(func: Callable):
    if func.__name__ == config.check_isTH_name:
        if func():
            return app.add_middleware(TrustedHostMiddleware, allowed_hosts=config.allowed_hosts)
    else:
        return app.middleware("http")(func)


#################### PG_DBWTB ################################
@app.on_event("startup")
async def startup():
    await sqlcfg.dbwtb.connect()
    print(f">>>>>>>>>>>>>>> sqlcfg.dbwtb 連線 = {sqlcfg.dbwtb.is_connected} <<<<<<<<<<<<<<<")


@app.on_event("shutdown")
async def shutdown():
    await sqlcfg.dbwtb.connect()

#################### middlewares ################################
for mw in mw_list:
    path_MW(mw)


#################### urlpattern ################################
# path_get("/test/{p}", test)
path_get("/pig_d", pig_d)
#
path_get("/proxy", show_freeproxy)
path_get("/nextip", get_next_ip)
path_get("/check_proxy", check_proxy)
#
path_get("/books/{bookid}", show_books)
path_get("/srs", show_register_subclasses)
#
path_get("/dbwtb", dbwtb_isconnected)


#################### schedule ################################
path_get("/startBGT", startBGT)
if config.startBGT_atonce:
    asyncio.create_task(startBGT())


#################### MSG ################################
msgs = [
    f'頂層工作目錄:【{config.top_dir}】',
    f'執行模式:【{config.now_mode}】',
    f'檢查trusted_host: 【{config.trusted_host}】 / allowed_hosts: {config.allowed_hosts}',
    f'在main啟動時執行排程startBGT: 【{config.startBGT_atonce}】',
    f'get_freeproxy 代理ip更新週期(秒): {get_freeproxy_delta}',
]

MSG.prt_msgs(msgs)
