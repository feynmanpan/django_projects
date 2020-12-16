for book in books:
    book = pq(book)
    title = book.find('p.title.product-field').text()
    author = book.find('span.contributor-name').text()
    star = book.find('div.kobo.star-rating').attr('aria-label').replace(' out of 5 stars', '').replace('Rated ', '')
    star = float(star)
    print(star)
