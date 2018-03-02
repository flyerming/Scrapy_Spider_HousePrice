# -*- coding: utf-8 -*-
import scrapy
import re
import sys
import urllib
import urllib.request
import json

from scrapy.spider import BaseSpider
from scrapy.selector import HtmlXPathSelector
from scrapy.http import Request
from tutorial.items import SoufangItem
from imp import reload

class SfSpider(scrapy.spider.Spider):
    
    name = "soufang_new_spider"
    allowed_domains = ["fang.com"]

    #start_urls = ['http://newhouse.qd.fang.com/house/s/b99/?ctm=1.qd.xf_search.page.10']
    start_urls = []
    for i in range(1,24):
        start_urls.append('http://newhouse.qd.fang.com/house/s/b9'+str(i)+'/?ctm=1.qd.xf_search.page.10/')

    handle_httpstatus_list = [404,403]

    def parse(self,response):
        reload(sys)
        #sys.setdefaultencoding('utf8')

        print('__________')
        if response.status == 403:
            print('meet 403, sleep 600 sconds')
            import time
            time.sleep(1200)
            yield Request(response.url,callback=self.parse)
        #404,页面不存在，直接范围即可
        elif response.status == 404:
            print('meet 404,return')
        else:
            
            hxs = scrapy.Selector(response)
            houselists = hxs.xpath("//div[@class='nlc_details']")
            for house in houselists:
                item = SoufangItem()
                name = house.xpath(".//div[@class='nlcd_name']//a/text()").extract_first().replace('\r','').replace('\n','').replace('\t','')
                link = house.xpath(".//div[@class='nlcd_name']//a/@href").extract_first()
#                house_status = house.xpath(".//div[@class='fangyuan pr']/text()").extract()
                house_type = house.xpath(".//div[@class='house_type clearfix']//a/text()").extract()
                house_type = '|'.join(house_type)
                address = house.xpath(".//div[@class='address']//a/@title").extract()
                address = ''.join(address)
                jianzhumianji = house.xpath(".//div[@class='house_type clearfix']/text()").extract()
                if(type(jianzhumianji) == list):
                    jianzhumianji = ''.join(jianzhumianji).replace('\r','').replace('\n','').replace('\t','').replace('/','').replace('－','')
                price = house.xpath(".//div[@class='nhouse_price']//span/text()").extract() + house.xpath(".//div[@class='nhouse_price']//em/text()").extract()
                price = ''.join(price)
                print(name)
                print(address)
                print(link)
                print(price)
                print(house_type)
                print(jianzhumianji)
                print(link)

                item['name'] = name.encode('utf-8')
                item['address'] = address.encode('utf-8')
                item['link'] = link.encode('utf-8')
                item['price'] = price.encode('utf-8')
                item['house_type'] = house_type.encode('utf-8')
                item['jianzhumianji'] = jianzhumianji.encode('utf-8')

                yield item
            print('__________')
