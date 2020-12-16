import pandas as pd
import requests
from pyquery import PyQuery as pq

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.135 Safari/537.36',
}
#
url_2020 = 'https://www.kobo.com/tw/zh/p/tw-kobo-2020top100'
#
r = requests.get(url_2020, headers=headers)
r.encoding = 'utf-8'
doc = pq(r.text)
#
books = doc.find('div.item.book.basic-item')
for book in books:
    book = pq(book)
    title = book.find('p.title.product-field').text()
    author = book.find('span.contributor-name').text()
    star = float(book.find('div.kobo.star-rating').attr('aria-label').replace(' out of 5 stars', '').replace('Rated ', ''))

    print(star)
