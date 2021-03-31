# -*- coding: utf-8 -*-
import aiohttp
import asyncio
import re
from pyquery import PyQuery as pq
from datetime import datetime
from time import time
#
from apps.book.classes.abookbase import BOOKBASE
import apps.ips.config as ipscfg
from apps.ips.config import ips_csv_path, dtype, cacert, headers
from apps.book.config import (
    dt_format,
    pub_dt_format,
    timeout,
    update_errcnt_max,
)
###################################################


class BOOKS(BOOKBASE):
    info_default = {
        "bookid": "0010770978"  # 刺殺騎士團長
    }
    # 博客來單書頁
    url_target_prefix = "https://www.books.com.tw/products/"
    update_errcnt = 0

    def __init__(self, **init):
        super().__init__(**init)
        self.url_target = f"{self.url_target_prefix}{self.info['bookid']}"

    async def update_info(self):
        stime = time()
        #
        connector = aiohttp.TCPConnector(ssl=cacert)
        TO = aiohttp.ClientTimeout(total=timeout)
        proxy = self.proxy
        update = {}
        update['err'] = None
        #
        try:
            async with aiohttp.ClientSession(connector=connector, timeout=TO) as session:
                async with session.get(self.url_target, headers=headers, proxy=proxy) as r:
                    status = r.status
                    rtext = await r.text(encoding='utf8')
        except asyncio.exceptions.TimeoutError as e:
            update['err'] = 'asyncio.exceptions.TimeoutError'
        except Exception as e:
            update['err'] = str(e)
        else:
            if (status == 200) and re.search(self.info['bookid'], rtext) is not None:
                doc = pq(rtext, parser='html')
                # _________________________________________________________________________
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
                for col in self.info_cols:
                    if (val := locals().get(col)) not in ['', None]:
                        update[col] = val
            else:
                update['err'] = f'status={status},rtext={rtext[:100]}'
        finally:
            # 抓成功，或到達最多次數，就不再抓
            if not update['err'] or self.update_errcnt == update_errcnt_max:
                update['create_dt'] = datetime.today().strftime(dt_format)
                self.info = self.info | update
                #
                print(self.info)
                print(f"update_duration = {time()-stime}")
                print(f"update_errcnt = {self.update_errcnt}")
            else:
                self.update_errcnt += 1
                print(f"err_proxy={proxy}, update_errcnt={self.update_errcnt}, err={update['err']}")
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
        #
        if price_list:
            price_list = not re.match(self.int_pattern, price_list) and 123456 or int(price_list)
        #
        if price_sale:
            if not re.match(self.float_pattern, price_sale):
                price_sale = 123.456
            else:
                price_sale = float(price_sale)
                if price_sale == (tmp := int(price_sale)):
                    price_sale = tmp

        return price_list, price_sale

    def save_info(self):
        pass
