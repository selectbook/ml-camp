rule# -*- coding:utf-8 -*-
#by 寒小阳(hanxiaoyang.ml@gmail.com)

import scrapy

from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor


from qqnews.items import *
from misc.log import *
from misc.spider import CommonSpider


class qqnewsSpider(scrapy.Spider):
    name = "qqnews"
    allowed_domains = ["tencent.com", 'qq.com']
    start_urls = [
        'http://news.qq.com/society_index.shtml'
    ]
    rules = [
        Rule(LinkExtractor(allow=('society_index.shtml')), callback='parse_0', follow=True),
        Rule(LinkExtractor(allow=(".*[0-9]{8}.*htm$")), callback='parse_1', follow=True),
    ]

    list_css_rules = { 
        '.linkto': {
            'url': 'a::attr(href)',
            'name': 'a::text',
        }   
    }

    list_css_rules_2 = {
        '#listZone .Q-tpWrap': {
            'url': '.linkto::attr(href)',
            'name': '.linkto::text'
        }
    }

    content_css_rules = {
        'text': '#Cnt-Main-Article-QQ p *::text',
        'images': '#Cnt-Main-Article-QQ img::attr(src)',
        'images-desc': '#Cnt-Main-Article-QQ div p+ p::text',
    }

    def parse_0(self, response):
        info('Parse0 '+response.url)
        x = self.parse_with_rules(response, self.list_css_rules, dict)
        pp.pprint(x)
        #return self.parse_with_rules(response, self.list_css_rules, qqnewsItem)

    def parse_1(self, response):
        info('Parse1 '+response.url)
        x = self.parse_with_rules(response, self.content_css_rules, dict)
        pp.pprint(x)
        #import pdb; pdb.set_trace()

    def parse_2(self, response):
        info('Parse2 '+response.url)




class QQNewsSpider(scrapy.Spider):
    name = 'qqnews'
    start_urls = ['http://news.qq.com/society_index.shtml']

    def parse(self, response):
        for href in response.xpath('//*[@id="news"]/div/div/div/div/em/a/@href'):
            full_url = response.urljoin(href.extract())
            yield scrapy.Request(full_url, callback=self.parse_question)

    def parse_question(self, response):
        print response.xpath('//div[@class="qq_article"]/div/h1/text()').extract_first()
        print response.xpath('//span[@class="a_time"]/text()').extract_first()
        print response.xpath('//span[@class="a_catalog"]/a/text()').extract_first()
        print "\n".join(response.xpath('//div[@id="Cnt-Main-Article-QQ"]/p[@class="text"]/text()').extract())
        print ""
        yield {
            'title': response.xpath('//div[@class="qq_article"]/div/h1/text()').extract_first(),
            'content': "\n".join(response.xpath('//div[@id="Cnt-Main-Article-QQ"]/p[@class="text"]/text()').extract()),
            'time': response.xpath('//span[@class="a_time"]/text()').extract_first(),
            'cate': response.xpath('//span[@class="a_catalog"]/a/text()').extract_first(),
        }
