import scrapy
from ..items import QuoteItem, AuthorItem


class QuotesCrawlerSpider(scrapy.Spider):
    name = "quotes_crawler"
    allowed_domains = ["quotes.toscrape.com"]
    start_urls = ["https://quotes.toscrape.com"]

    def parse(self, response, **kwargs):
        quotes = response.css('div.quote')
        for q in quotes:
            author = q.css('span small.author::text').get()
            quote = q.css('span.text::text').get()
            tags = q.css('div.tags a.tag::text').getall()
            yield QuoteItem(author=author, quote=quote, tags=tags)
            yield response.follow(url=self.start_urls[0] + q.css('span a::attr(href)').get(), callback=self.parse_author)

        next_page = response.css('li.next a::attr(href)').get()
        if next_page:
            yield scrapy.Request(response.urljoin(next_page), callback=self.parse)

    def parse_author(self, response):
        content = response.css("div.author-details")
        fullname = content.css('h3.author-title::text').get()
        born_date = content.css('p span.author-born-date::text').get()
        born_location = content.css('p span.author-born-location::text').get()
        description = content.css('div.author-description::text').get().strip()
        yield AuthorItem(fullname=fullname, born_date=born_date, born_location=born_location, description=description)
