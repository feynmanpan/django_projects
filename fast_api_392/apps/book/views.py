
import json
from typing import Optional
#
from fastapi import Request
from fastapi.responses import HTMLResponse, ORJSONResponse, PlainTextResponse
#
from .config import jinja_templates
# from .classes.abookbase import BOOKBASE
# from .classes.bbooks import BOOKS
# 載入所有subclass，使其註冊入BOOKBASE，main.py也有import
from .classes.zimportall import (
    BOOKBASE,
    BOOKS,
    TAAZE,
    ELITE,
)
###############################################


async def show_base(f='r'):
    if f == 'r':
        ans = list(BOOKBASE.register_subclasses.keys())
    else:
        ans = list(BOOKBASE.top_proxy)
    return ORJSONResponse(ans)


async def show_books(request: Request, bookid: str = '0010770978'):
    init = {
        'bookid': bookid,
    }
    try:
        book = BOOKS(**init)
        #
        if not book.info['create_dt']:
            if info := await book.db_info():
                print('從db抓')
                book.info = info
            else:
                print('重新爬蟲')
                await book.update_info()
        else:
            print('沿用cls.objs裡面')
    except Exception as e:
        return HTMLResponse(str(e))
    #
    context = {
        'request': request,
        'res': json.dumps(book.info, indent=2, ensure_ascii=False),
        'info': book.info,
    }
    return jinja_templates.TemplateResponse('show_books.html', context)
    # return ORJSONResponse(book.info)
