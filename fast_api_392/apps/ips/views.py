import asyncio
import requests
import aiohttp
from pyquery import PyQuery as pq
import pandas as pd
import os
#
from fastapi import Request
from fastapi.responses import HTMLResponse
#
from .config import jinja_templates, ips_csv_path, ips_html, ips_csv_tb_html, ips_html_path
########################################################


def show_freeproxy(request: Request, f: str = 'csv'):
    context = {
        'request': request,
    }
    rep = HTMLResponse('請啟動startBGT，撈取csv')
    if f == 'html':
        # 每次抓取的原始頁
        if os.path.isfile(ips_html_path):
            rep = jinja_templates.TemplateResponse(ips_html, context)
    else:
        # 顯示持續擴充更新的csv
        if os.path.isfile(ips_csv_path):
            context['ips_csv_tb_html'] = pd.read_csv(ips_csv_path).to_html()
            rep = jinja_templates.TemplateResponse(ips_csv_tb_html, context)
    #
    return rep
