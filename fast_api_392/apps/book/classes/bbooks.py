# -*- coding: utf-8 -*-
import aiohttp
import asyncio
import re
from pyquery import PyQuery as pq
from datetime import datetime
from time import time
from typing import Dict, Any, Callable, Awaitable, Coroutine, Optional
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
    # 博客來單書頁
    url_target_prefix = "https://www.books.com.tw/products/"
    # 評論及庫存都要ajax
    url_target_comment = 'https://www.books.com.tw/product_show/getCommentAjax/{}:{}:A:M201101_0_getCommentData_P00a400020068:getCommentAjax:M201101_078_view/M201101_078_view'
    url_target_cart = 'https://www.books.com.tw/product_show/getProdCartInfoAjax/{}/M201105_032_view'
    # 登入頁
    url_target_login = 'https://cart.books.com.tw/member/login'
    #
    page_err = [
        '頁面連結錯誤',
        # 'The Event ID',
        '限制級商品'
    ]
    #
    account = login['BOOKS'][0]
    passwd = login['BOOKS'][1]

    def __init__(self, **init):
        super().__init__(**init)
        self.url_target = f"{self.url_target_prefix}{self.info[self.INFO_COLS.bookid]}"

    async def update_info(self, proxy: Optional[str] = None):
        stime = time()
        #
        connector = aiohttp.TCPConnector(ssl=cacert)
        TO = aiohttp.ClientTimeout(total=timeout)
        proxy = proxy or await self.proxy
        update: Dict[str, Any] = self.update_default | {}  # 不加型別提示，後面更新err時會有紅波浪
        #
        enter_bookpage = False
        #
        try:
            async with aiohttp.ClientSession(connector=connector, timeout=TO) as session:
                # 抓單書頁資訊
                async with session.get(self.url_target, headers=headers, proxy=proxy) as r:
                    status = r.status
                    rtext = await r.text(encoding='utf8')
                # 抓ajax 庫存及評論
                enter_bookpage = (status == 200) and self.info[self.INFO_COLS.bookid] in rtext and '商品介紹' in rtext
                if enter_bookpage:
                    await asyncio.sleep(0.15)
                    headers2 = headers | {'Referer': self.url_target}
                    stock = await self.stock_handle(session, headers2, proxy)
                    await asyncio.sleep(0.15)
                    comment = await self.comment_handle(session, headers2, proxy)
        except asyncio.exceptions.TimeoutError as e:
            update['err'] = 'asyncio.exceptions.TimeoutError'
        except Exception as e:
            update['err'] = str(e)
        else:
            if enter_bookpage:
                # 確定進入單書頁
                # print(rtext)
                doc = pq(rtext, parser='html')
                # =========================================================================
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
                url_book = self.url_target
                url_vdo = doc.find('.cont iframe').eq(0).attr('src')  # 沒影片時為None
                url_cover = doc.find(".cover_img > img.cover").attr("src")
                # =========================================================================
                # 由base統一update處理
                update = self.update_handle(update, locals())
            else:
                for pe in self.page_err:
                    if pe in rtext:
                        update['err'] = pe
                        break
                else:
                    update['err'] = f'status={status},rtext={rtext[:100]}'
        finally:
            # 抓成功，或頁面連接錯誤，或到達最多次數，就不再抓
            if not update['err'] or update['err'] in self.page_err or self.update_errcnt == update_errcnt_max:
                update[self.INFO_COLS.create_dt] = datetime.today().strftime(dt_format)
                self.info = self.info | update
                #
                self.update_errcnt = 0
                #
                print(f"update_duration = {time()-stime},final_proxy={proxy}")
                print(f"update_errcnt = {self.update_errcnt}")
            else:
                self.update_errcnt += 1
                print(f"err_proxy={proxy}, update_errcnt={self.update_errcnt}/{update_errcnt_max}, err={update['err']}")
                await self.update_info()

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

    async def stock_handle(self, session, headers, proxy):
        '''抓ajax庫存'''
        bid = self.info['bookid']
        url_target_cart = self.url_target_cart.format(bid)
        #
        async with session.get(url_target_cart, headers=headers, proxy=proxy) as r2:
            status2 = r2.status
            rtext2 = await r2.text(encoding='utf8')
            if (status2 == 200) and rtext2:
                return pq(rtext2, parser='html').find("div.mc002.type02_p008 ul.list li.no").eq(0).text().strip()

    async def comment_handle(self, session, headers, proxy):
        '''抓ajax評論'''
        bid = self.info['bookid']
        url_target_comment = self.url_target_comment.format(bid, 1)
        # 先看第一頁評論結果
        async with session.get(url_target_comment, headers=headers, proxy=proxy) as r2:
            status2 = r2.status
            rtext2 = await r2.text(encoding='utf8')
            # 看一共幾頁
            if (status2 == 200) and rtext2:
                doc2 = pq(rtext2, parser='html')
                pn = doc2.find(".cnt_page > .page > span").eq(0).text().strip()
                pn = pn and int(pn) or 0
                if pn:
                    for p in range(2, pn + 1):
                        await asyncio.sleep(0.15)
                        url_target_comment = self.url_target_comment.format(bid, p)
                        async with session.get(url_target_comment, headers=headers, proxy=proxy) as r:
                            rtext = await r.text(encoding='utf8')
                            rtext2 += rtext
            # 去除js
            return re.sub(self.comment_js_pattern, '', rtext2)

    def save_info(self):
        pass

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
