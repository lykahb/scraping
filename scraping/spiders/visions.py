# -*- coding: utf-8 -*-
from urlparse import urljoin
import itertools

import scrapy
from scrapy.utils.response import get_base_url

from scraping.items import CategoryItem, ProductItem


class VisionsSpider(scrapy.Spider):
    name = "visions"
    allowed_domains = ["visions.ca"]
    start_urls = (
        'http://www.visions.ca/',
    )

    def parse(self, response):
        for dep in response.css('#mastermenu-dropdown > li'):
            dep_name = extract_string(dep.xpath('a'))
            categories = dep.css('div.mastermenu-bigsub') or dep.xpath('a')

            for cat in categories:
                for link in cat.css('a[href^="/Catalogue/"]'):
                    url = urljoin(get_base_url(response), link.xpath('@href').extract()[0])
                    name = extract_string(link.css(".mastermenu-bigsub-title") or link)
                    yield CategoryItem(department=dep_name, name=name, link=url)
                    yield scrapy.Request(url, callback=self.parse_products)

    @staticmethod
    def parse_products(response):
        def product(product_sel, title_sel, price_sel):
            for prod in response.css(product_sel):
                title = prod.css(title_sel)
                url = urljoin(get_base_url(response), title.xpath('@href').extract()[0])
                item = ProductItem(name=extract_string(title),
                                   price=extract_string(prod.css(price_sel)),
                                   link=url)
                if prod.css('img[src*=final_clearance_box]').extract():
                    item['availability'] = 'limited'
                yield item

        return itertools.chain(product('.productresult-itembox', 'h2 a', '.price'),
                               product('.bundleItemTable', '.name a', '.price .regPrice, .price .salePrice'),
                               product('.productItemMain', '.productName a', '.price'))


def extract_string(sel):
    return ''.join(sel.css('::text').extract()).strip()
