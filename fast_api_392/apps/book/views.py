import json
from typing import Optional
#
from fastapi import Request
from fastapi.responses import HTMLResponse, ORJSONResponse, PlainTextResponse
import pandas as pd
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
#
import sqlalchemy as sa
from apps.sql.config import dbwtb
from apps.book.model import INFO
###############################################


async def show_base(f='r'):
    if f == 'r':
        ans = list(BOOKBASE.register_subclasses.keys())
    else:
        ans = list(BOOKBASE.top_proxy)
    return ORJSONResponse(ans)


async def showbook(request: Request, store: str = 'BOOKS', bookid: str = '0010770978', fd: int = 0):
    result = None
    try:
        init = {
            'bookid': bookid,
        }
        cls_store = BOOKBASE.register_subclasses[store.upper()]
        book = cls_store(**init)
        await book.read_or_update(fd=fd)
    except Exception as e:
        result = HTMLResponse(str(e))
    else:
        context = {
            'request': request,
            'res': json.dumps(book.info, indent=2, ensure_ascii=False),
            'info': book.info,
        }
        result = jinja_templates.TemplateResponse('show_books.html', context)
        # return ORJSONResponse(book.info)
    finally:
        return result


async def show_info(request: Request):
    '''顯示所有書籍資訊'''
    cs = INFO.__table__.columns
    query = sa.select(cs)
    rows = await dbwtb.fetch_all(query)
    # price_list/_sale 為 None 者，pd會轉 float64 變成 np.nan，輸出 html字串 NaN
    # notin = ['intro','comment']
    # cols = ['idx']+[col for col in BOOKBASE.info_cols if col not in notin]
    cols = ['store', 'bookid', 'isbn10', 'isbn13', 'title', 'price_list', 'stock', 'err', 'create_dt']
    df = pd.DataFrame(rows)[cols].to_html()
    #
    context = {
        'request': request,
        'df': df,
    }
    result = jinja_templates.TemplateResponse('show_info.html', context)
    #
    return result
