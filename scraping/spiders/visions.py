# -*- coding: utf-8 -*-
from urlparse import urljoin

import scrapy
from scrapy.utils.response import get_base_url

from scraping.items import CategoryItem


class VisionsSpider(scrapy.Spider):
    name = "visions"
    allowed_domains = ["visions.ca"]
    start_urls = (
        'http://www.visions.ca/',
    )

    def parse(self, response):
        for dep in response.css('#mastermenu-dropdown > li'):
            dep_name = dep.xpath('a').css('::text').extract()
            categories = dep.css('div.mastermenu-bigsub') or dep.xpath('a')

            for cat in categories:
                for link in cat.css('a[href^="/Catalogue/"]'):
                    url = urljoin(get_base_url(response), link.xpath('@href').extract()[0])
                    name = (link.css(".mastermenu-bigsub-title") or link).css('::text').extract()
                    yield CategoryItem(department=dep_name, name=name, link=url)