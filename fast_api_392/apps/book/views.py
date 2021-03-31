import json
#
from fastapi import Request
from fastapi.responses import HTMLResponse, ORJSONResponse, PlainTextResponse
#
from .classes.bbooks import BOOKS
from .config import jinja_templates
###############################################


async def show_books(request: Request, bookid: str = '0010770978'):
    init = {
        'bookid': bookid,
    }
    try:
        book = BOOKS(**init)
    except Exception as e:
        return HTMLResponse(str(e))
    #
    await book.update_info()
    context = {
        'request': request,
        'res': json.dumps(book.info, indent=2, ensure_ascii=False),
        'info': book.info,
    }
    return jinja_templates.TemplateResponse('show_books.html', context)
    # return ORJSONResponse(book.info)
