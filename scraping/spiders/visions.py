# -*- coding: utf-8 -*-
import scrapy


class VisionsSpider(scrapy.Spider):
    name = "visions"
    allowed_domains = ["visions.ca"]
    start_urls = (
        'http://www.visions.ca/',
    )

    def parse(self, response):
        pass
