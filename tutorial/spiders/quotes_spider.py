import scrapy


class QuoteSpider(scrapy.Spider):

    name = 'quotes'
    start_urls = [
        'http://quotes.toscrape.com/page/1/',
        'http://quotes.toscrape.com/page/2/',
    ]

    # 即使没有定义 start_request()方法，也能够默认执行
    def parse(self, response):
        # 将网页爬取到本地
        # page = response.url.split('/')[-2]
        # filename = 'quote-%s.html' % page
        # with open(filename, 'wb') as f:
        #     f.write(response.body)
        #

        for quote in response.css("div.quote"):
            yield {
                'text': quote.css('span.text::text').extract_first(),
                'author': quote.css('small.author::text').extract_first(),
                'tags': quote.css('div.tags a.tag::text').extract_first(),
            }

        next_page = response.css('li.next a::attr(href)').extract_first()
        if next_page is not None:
            # 重新组成可以使用的url
            # next_page = response.urljoin(next_page)
            # print(type(next_page))
            # yield scrapy.Request(url=next_page, callback=self.parse)

            # 一个简便的写法
            yield response.follow(next_page, callback=self.parse)