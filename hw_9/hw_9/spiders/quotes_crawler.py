import scrapy
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from ..items import QuoteItem, AuthorItem


class AuthorsSpider(CrawlSpider):
    name = "quotes_crawler"
    allowed_domains = ["quotes.toscrape.com"]
    start_urls = ["https://quotes.toscrape.com"]

    rules = (
        # Rule(LinkExtractor(allow=(r"/page/",), deny=(r'/tag/',)), callback='parse_quote'),
        # Rule(LinkExtractor(allow=(r"/author/",)), callback="parse_authors"),
        # Rule(LinkExtractor(allow=(r"/",), deny=(r'/tag/',)), callback='parse_quote'),
        # Rule(LinkExtractor(allow=r'page', deny=r'tag'), callback='parse_quote'),
        Rule(LinkExtractor(allow=(r'page', r'/'), deny=r'tag'), callback='parse_quote', follow=True),
    )

    def parse_quote(self, response):
        quote = QuoteItem()
        quote['author'] = response.css('span small.author::text').get()
        quote['quote'] = response.css('span.text::text').get()
        quote['tags'] = response.css('div.tags a.tag::text').getall()
        yield quote

    def parse_authors(self, response):
        author = AuthorItem()
        author['fullname'] = response.css('h3.author-title::text').get()
        author['born_date'] = response.css('span.author-born-date::text').get()
        author['born_location'] = response.css('span.author-born-location::text').get()
        author['description'] = response.css('div.author-description::text').get()
        yield author
