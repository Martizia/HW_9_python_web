# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html
import json

# useful for handling different item types with a single interface
from itemadapter import ItemAdapter


class Hw9Pipeline:
    authors = []
    quotes = []

    def process_item(self, item, spider):
        adapter = ItemAdapter(item)
        if 'fullname' in adapter:
            self.authors.append(dict(adapter))
        elif 'quote' in adapter:
            self.quotes.append(dict(adapter))

    def close_spider(self, spider):
        with open('quotes.json', 'w', encoding='utf-8') as file:
            json.dump(self.quotes, file, ensure_ascii=False, indent=2)
        with open('authors.json', 'w', encoding='utf-8') as file:
            json.dump(self.authors, file, ensure_ascii=False, indent=2)
