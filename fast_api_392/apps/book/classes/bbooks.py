# -*- coding: utf-8 -*-
import aiohttp
import aiofiles
import asyncio
import re
import json
import os
from pyquery import PyQuery as pq
from datetime import datetime
from time import time
from typing import Dict, Any, Callable, Awaitable, Coroutine, Optional
from PIL import Image
import pytesseract
#
from apps.book.classes.abookbase import BOOKBASE
import apps.ips.config as ipscfg
from apps.ips.config import ips_csv_path, dtype, cacert, headers
from apps.book.config import (
    dt_format,
    pub_dt_format,
    timeout,
    update_errcnt_max,
    login,
)
###################################################


class BOOKS(BOOKBASE):
    info_default = {
        "bookid": "0010770978"  # 刺殺騎士團長
    }
    bookid_pattern = '^[a-zA-Z0-9]{10}$'  # 博客來書號格式
    comment_js_pattern = '<script type="text/javascript">(.|\n)+?</script>'
    #
    url_home = 'https://www.books.com.tw'
    # 博客來單書頁
    url_prod_prefix = f"{url_home}/products/"
    # 評論及庫存都要ajax
    url_comment_ajax = 'https://www.books.com.tw/product_show/getCommentAjax/{}:{}:A:M201101_0_getCommentData_P00a400020068:getCommentAjax:M201101_078_view/M201101_078_view'
    url_cart_ajax = 'https://www.books.com.tw/product_show/getProdCartInfoAjax/{}/M201105_032_view'
    # 登入頁
    url_cart_dns = 'https://cart.books.com.tw'
    url_login = f'{url_cart_dns}/member/login'
    url_loginpost = f'{url_cart_dns}/member/login_do/'
    #
    page_err = [
        '頁面連結錯誤',
        # 'The Event ID',
        '限制級商品'
    ]
    #
    account = login['BOOKS'][0]
    passwd = login['BOOKS'][1]
    #
    cwd = os.path.dirname(os.path.realpath(__file__))

    def __init__(self, **init):
        super().__init__(**init)
        self.url_prod = f"{self.url_prod_prefix}{self.bid}"
        self.headers_Referer = headers | {'Referer': self.url_prod}
        self.headers_Referer_login = headers | {'Referer': f'{self.url_cart_dns}/member/login?url={self.url_prod}'}

    async def update_info(self, proxy: Optional[str] = None):
        stime = time()
        #
        self.now_proxy = proxy or await self.proxy
        enter_bookpage = False
        enter_18 = False
        login_success = False
        update: Dict[str, Any] = self.update_default | {}  # 不加型別提示，後面更新err時會有紅波浪
        #
        try:
            # 抓單書頁資訊
            async with self.ss.get(self.url_prod, headers=headers, proxy=self.now_proxy) as r:
                status = r.status
                rtext = await r.text(encoding='utf8')
            #
            if (status == 200) and (self.bid in rtext):
                enter_bookpage = '商品介紹' in rtext
                if not enter_bookpage:
                    enter_18 = '限制級商品' in rtext
                print(f'進入單書頁={enter_bookpage}, 進入18禁={enter_18}')
        except asyncio.exceptions.TimeoutError as e:
            update['err'] = 'asyncio.exceptions.TimeoutError'
        except Exception as e:
            update['err'] = str(e)
        else:
            if enter_bookpage:
                # 確定進入單書頁
                try:
                    result = await self.bookpage_handle(rtext)
                    update = self.update_handle(update, result)
                except asyncio.exceptions.TimeoutError as e:
                    update['err'] = 'asyncio.exceptions.TimeoutError'
                except Exception as e:
                    update['err'] = str(e)
            elif enter_18:
                # 18禁，直到登入成功
                try:
                    while not login_success:
                        print('login_success=', login_success)
                        capcha = await self.get_capcha()
                        if capcha:
                            login_success = await self.loginpost(capcha)
                            if login_success:
                                print('登入capcha=', capcha)
                except asyncio.exceptions.TimeoutError as e:
                    update['err'] = 'asyncio.exceptions.TimeoutError'
                except Exception as e:
                    update['err'] = str(e)
            else:
                for pe in self.page_err:
                    if pe in rtext:
                        update['err'] = pe
                        break
                else:
                    update['err'] = f'status={status},rtext={rtext[:100]}'
        finally:
            if enter_18 and login_success:
                self.update_errcnt = 0
                print('登入成功，重抓18禁單書頁')
                await self.update_info(proxy=self.now_proxy)
            else:
                await self.close_ss()
                # 抓成功，或頁面連接錯誤，或到達最多次數，就不再抓
                if not update['err'] or update['err'] in self.page_err or self.update_errcnt == update_errcnt_max:
                    update[self.INFO_COLS.create_dt] = datetime.today().strftime(dt_format)
                    #
                    self.info |= update
                    self.update_errcnt = 0
                    #
                    print(f"final_proxy={self.now_proxy}, update_duration = {time()-stime}")
                else:
                    self.update_errcnt += 1
                    print(f"err_proxy={self.now_proxy}, update_errcnt={self.update_errcnt}/{update_errcnt_max}, err={update['err']}")
                    await self.update_info()

    async def bookpage_handle(self, rtext):
        '''單書頁處理'''
        # (1) ajax 抓庫存及評論 =========================================================================
        stock = await self.stock_handle()
        comment = await self.comment_handle()
        # (2) 單書頁 =========================================================================
        doc = pq(rtext, parser='html')
        #
        isbn = doc.find(".mod_b.type02_m058.clearfix .bd ul li").eq(0).text().replace("ISBN：", "").strip()
        if (len_isbn := len(isbn)) >= 10:
            isbn10 = (len_isbn == 10 and isbn) or None
            isbn13 = (len_isbn == 13 and isbn) or None
        # _________________________________________________________________________
        title = doc.find('.mod.type02_p002.clearfix > h1').eq(0).text().strip()
        title2 = doc.find(".mod.type02_p002.clearfix > h2").eq(0).text().strip()
        # _________________________________________________________________________
        el = doc.find(".type02_p003.clearfix ul").eq(0)
        author = self.author_handle(el)
        publisher = self.publisher_handle(el)
        pub_dt = self.pub_dt_handle(el)
        lang = el.find("li:Contains('語言')").eq(0).text().replace('語言：', '').strip()
        # _________________________________________________________________________
        el = doc.find(".prod_cont_a ul.price").eq(0)
        price_list, price_sale = self.price_handle(el)
        spec = doc.find(".mod_b.type02_m058.clearfix .bd li:Contains('規格')").eq(0).text().replace(" ", "").replace("規格：", "").strip()
        intro = doc.find(".bd .content").eq(0).html()
        # _________________________________________________________________________
        url_book = self.url_prod
        url_vdo = doc.find('.cont iframe').eq(0).attr('src')  # 沒影片時為None
        url_cover = doc.find(".cover_img > img.cover").attr("src")
        #
        return locals()

    def author_handle(self, el):
        authors = el.find("li").find("a[href*='adv_author']")
        author = ''
        for au in authors:
            parenttext = pq(au).parent().text().strip()
            name = pq(au).text().strip()
            #
            if '作者' in parenttext and '原文作者' not in parenttext:
                author += f'作者：{name}/'
            elif '原文作者' in parenttext:
                author += f'原文作者：{name}/'
            elif '譯者' in parenttext:
                author += f'譯者：{name}/'
            elif '編者' in parenttext:
                author += f'編者：{name}/'
        #
        author = author.strip('/')
        return author

    def publisher_handle(self, el):
        publisher = el.find("a[href*='sys_puballb']").eq(0).text().strip()
        # --原文出版社
        if not publisher:
            publisher = el.find("li:Contains('原文出版社')").eq(0).text().replace('原文出版社：', '').strip()
        return publisher

    def pub_dt_handle(self, el):
        pub_dt = el.find("li:Contains('出版日期')").eq(0).text().replace('出版日期：', '').replace('/', '-').strip()
        # pub_dt = datetime.strptime(pub_dt, pub_dt_format).date()
        return pub_dt

    def price_handle(self, el):
        price_list = el.find("em").eq(0).text().strip()
        price_sale = el.find("strong.price01").eq(-1).find("b").eq(0).text().strip()  # 有優惠價跟特價，要找最後一個
        # 定價售價統一base處理
        price_list = self.price_list_handle(price_list)
        price_sale = self.price_sale_handle(price_sale)
        #
        return price_list, price_sale

    async def stock_handle(self):
        '''抓ajax庫存'''
        await asyncio.sleep(0.05)
        url_cart_ajax = self.url_cart_ajax.format(self.bid)
        #
        async with self.ss.get(url_cart_ajax, headers=self.headers_Referer, proxy=self.now_proxy) as r2:
            status2 = r2.status
            rtext2 = await r2.text(encoding='utf8')
            if (status2 == 200) and rtext2:
                return pq(rtext2, parser='html').find("div.mc002.type02_p008 ul.list li.no").eq(0).text().strip()

    async def comment_handle(self):
        '''抓ajax評論'''
        await asyncio.sleep(0.15)
        url_comment_ajax = self.url_comment_ajax.format(self.bid, 1)
        # 先看第一頁評論結果
        async with self.ss.get(url_comment_ajax, headers=self.headers_Referer, proxy=self.now_proxy) as r2:
            status2 = r2.status
            rtext2 = await r2.text(encoding='utf8')
            # 看一共幾頁
            if (status2 == 200) and rtext2:
                pn = pq(rtext2, parser='html').find(".cnt_page > .page > span").eq(0).text().strip()
                pn = pn and int(pn) or 0
                if pn:
                    for p in range(2, pn + 1):
                        await asyncio.sleep(0.15)
                        url_comment_ajax = self.url_comment_ajax.format(self.bid, p)
                        async with self.ss.get(url_comment_ajax, headers=self.headers_Referer, proxy=self.now_proxy) as r:
                            rtext = await r.text(encoding='utf8')
                            rtext2 += rtext
                # 去除js
                return re.sub(self.comment_js_pattern, '', rtext2)

    def save_info(self):
        pass

    async def loginpost(self, capcha):
        '''遞交登入'''
        formdata = {
            'captcha': capcha,
            'login_id': self.account,
            'login_pswd': self.passwd,
        }
        #
        async with self.ss.post(self.url_loginpost, headers=self.headers_Referer_login, proxy=self.now_proxy, data=formdata) as r:
            if r.status == 200:
                rtext = await r.text(encoding='utf8')
                return json.loads(rtext)['success']

    async def get_capcha(self):
        '''從登入頁面抓capcha圖檔'''
        async with self.ss.get(self.url_login, headers=headers, proxy=self.now_proxy) as r:
            if r.status == 200:
                rtext = await r.text(encoding='utf8')
                doc = pq(rtext, parser='html')
                url_capcha = self.url_cart_dns + doc.find("#captcha_img img").attr('src')
                # OCR
                async with self.ss.get(url_capcha, headers=headers, proxy=self.now_proxy) as r:
                    if r.status == 200:
                        jpg = os.path.join(self.cwd, url_capcha.split('?')[-1] + '.jpg')
                        print(f'儲存capcha: {jpg}')
                        f = await aiofiles.open(jpg, mode='wb')
                        await f.write(await r.read())
                        await f.close()
                        #
                        img = Image.open(jpg)
                        img = self.convert_img(img)
                        capcha = pytesseract.image_to_string(img).strip()
                        #
                        os.rename(jpg, os.path.join(self.cwd, 'last_capcha.jpg'))
                        #
                        return capcha

    def convert_img(self, img):
        '''登入的驗證碼圖片轉成黑白'''
        pixels = img.load()
        R, G, B = [87, 98, 201]
        for x in range(img.width):
            for y in range(img.height):
                r, g, b = pixels[x, y]
                delta = abs(R - r) + abs(G - g) + abs(B - b)
                if delta < 30:
                    pixels[x, y] = (0, 0, 0)
                else:
                    pixels[x, y] = (255, 255, 255)
        return img
