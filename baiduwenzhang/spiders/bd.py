# -*- coding: utf-8 -*-
import scrapy
from baiduwenzhang.items import BaiduwenzhangItem


class BdSpider(scrapy.Spider):
    name = 'bd'
    allowed_domains = ['baidu.com']
    start_urls = [
        'https://mbd.baidu.com/newspage/data/landingsuper?context=%7B%22nid%22%3A%22news_10130336363786944244%22%7D&n_type=0&p_from=1',
        'https://mbd.baidu.com/newspage/data/landingsuper?context=%7B%22nid%22%3A%22news_9700910256209338841%22%7D&n_type=0&p_from=1',
        'https://mbd.baidu.com/newspage/data/landingsuper?context=%7B%22nid%22%3A%22news_10228862819041146370%22%7D&n_type=0&p_from=1',
        ]

    def parse(self, response):
        next_pages = response.xpath('//h3/a[@class="upgrade"]/@href').extract()
        for page in next_pages:
            yield scrapy.Request(url=page, callback=self.parse_detial)

    def parse_detial(self, response):
        print(response.status)
        title = response.xpath('//h2/text()').extract_first()
        # print(title)
        # contents = response.xpath('')
        try:
            author = response.xpath('//p[@class="author-name"]/text()').extract_first()
        except:
            author = '未填写'
        # print(author)
        try:
            release_data = response.xpath('//span[@class="date"]/text()').extract_first()[5:]
        except:
            release_data = '未填写'
        try:
            release_time = response.xpath('//span[@class="time"]/text()').extract_first()
        except:
            release_time = '未填写'
        # print(release_data, release_time)
        try:
            release_account = response.xpath('//span[@class="account-authentication"]/text()').extract_first()
        except:
            release_account = '未填写'
        # print(release_account)
        try:
            contents = response.xpath('//div[@class="article-content"]//text()').extract()
        except:
            contents = '未填写'
        # print(len(contents))
        content = ' '.join(x for x in contents)
        # print(len(content))
        # print(content)
        # print('*' * 30)
        item = BaiduwenzhangItem()
        item['author'] = author
        item['release_data'] = release_data
        item['release_time'] = release_time
        item['release_account'] = release_account
        item['content'] = content
        item['title'] = title
        yield item

        next_pages = response.xpath('//h3/a[@class="upgrade"]/@href').extract()
        for page in next_pages:
            yield scrapy.Request(url=page, callback=self.parse_detial)
