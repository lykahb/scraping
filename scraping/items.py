# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class CategoryItem(scrapy.Item):
    department = scrapy.Field()
    category_id = scrapy.Field()
    name = scrapy.Field()
    link = scrapy.Field()