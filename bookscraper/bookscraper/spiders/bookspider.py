import scrapy


class BookspiderSpider(scrapy.Spider):
    name = "bookspider"
    allowed_domains = ["books.toscrape.com"]
    start_urls = ["https://books.toscrape.com"]

    def parse(self, response):
        books = response.css("article.product_pod")
        for book in books:
            book_href = book.css("h3 a").attrib["href"]
            if "catalogue/" in book_href:
                book_url = "https://books.toscrape.com/" + book_href
            else:
                book_url = "https://books.toscrape.com/catalogue/" + book_href
            yield response.follow(book_url, callback=self.parse_book_url)

        next_page = response.css('li.next a').attrib['href']
        if next_page is not None:
            if 'catalogue/' in next_page:
                next_page_url = 'https://books.toscrape.com/' + next_page
            else:
                next_page_url = 'https://books.toscrape.com/catalogue/' + next_page
            yield response.follow(next_page_url, callback=self.parse)

    def parse_book_url(self, response):
        book = response.css('div.product_main')[0]
        table_rows = response.css('table tr')
        yield {
            "url": response.url,
            "title": response.css(".product_main h1::text").get(),
            "product_type": table_rows[1].css('td ::text').get(),
            "price_excl_tax": table_rows[2].css('td ::text').get(),
            "price_incl_tax": table_rows[3].css('td ::text').get(),
            "tax": table_rows[4].css('td ::text').get(),
            "availability": table_rows[5].css('td ::text').get(),
            "num_reviews": table_rows[6].css('td ::text').get(),
            "stars": book.css("p.star-rating").attrib["class"],
            "category": response.xpath("//ul[@class='breadcrumb']/li[2]/a//text()").get(),
            "description": response.xpath("//article/p[1]//text()").get(),
            "price": book.css("p.price_color").get()
        }

