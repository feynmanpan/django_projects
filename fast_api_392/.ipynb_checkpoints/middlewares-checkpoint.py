#################### import ################################
from fastapi import Request
import config
import re
from views import maintenance
#


async def check_isMT(request: Request, call_next):
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