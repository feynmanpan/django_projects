#################### import ################################
import re
#
from fastapi import Request
from fastapi.responses import HTMLResponse
#
import config
from views import maintenance
#


async def check_isMT(request: Request, call_next):
    '''確認執行模式是否維護'''
    print(request.url.path)
    print(request.url)
    if isMT := (config.now_mode.name == 'maintenance'):
        for pattern in config.maintenance_allow_patterns:
            if re.match(pattern, request.url.path):   # DNS以後到?以前
                isMT = False
                break
    #
    if isMT:
        return maintenance()
    else:
        return await call_next(request)


async def mwtest(request: Request, call_next):
    print('中介測試')
    html = '''
        <h1 style="color:blue">中介測試</h1>
    '''
    return HTMLResponse(html)


def trusted_host():
    '''trigger用途而已'''
    pass


#################### app.middleware("http") ################################
# return 都要是response class，不能直接基本類型
# 由後先呼叫
mw_list = [
    check_isMT,
    # mwtest,
    trusted_host,
]
