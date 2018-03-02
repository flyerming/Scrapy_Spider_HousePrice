import scrapy
import sys
import time
import requests

from scrapy.spider import BaseSpider
from scrapy.http import Request
from tutorial.items import AgentIPItem
from imp import reload
from random import randint
import requests

class AgentSpider(scrapy.spider.Spider):

    name = "agency_ip2_collector"

    allowed_domains = ["xicidaili.com"]
    url_base = 'http://www.xicidaili.com'
    start_urls = []
    start_urls.append(url_base + "/nn/1")
    handle_httpstatus_list = [404,403]

    #num获取num页 国内高匿ip的网页中代理数据
    def parse(self,response):
        reload(sys)
        print('__________')
        if response.status == 403:
            print('meet 403, sleep 600 sconds')
            time.sleep(1200)
            yield Request(response.url, callback=self.parse)
        # 404,页面不存在，直接范围即可
        elif response.status == 404:
            print('meet 404,return')
        else:
            hxs = scrapy.Selector(response)
            fetchlists = hxs.xpath("//img[@src='http://fs.xicidaili.com/images/flag/cn.png']")
            for fetch in fetchlists:
                item = AgentIPItem()
                fetch_ancestor = fetch.xpath("./parent::*")
                fetch_ancestor_brother = fetch_ancestor.xpath("./following-sibling::*/text()").extract()
                IP = fetch_ancestor_brother[0]
                PORT = fetch_ancestor_brother[1]
                HTYPE = fetch_ancestor_brother[5]
                print("IP:%s" % IP)
                print("PORT:%s" % PORT)
                print("TYPE:%s" % HTYPE)
                try:
                    requests.get('http://wenshu.court.gov.cn/', proxies={"http": "http://" + IP + ":" + PORT})
                except:
                    print('connect failed')
                else:
                    print('success')
                    item['IP'] = IP.encode('utf-8')
                    item['PORT'] = PORT.encode('utf-8')
                    item['TYPE'] = HTYPE.encode('utf-8')
                    item['proxyip'] = "{'ip_port': '" + IP + ":" + PORT + "', 'user_pass': ''},"
    #                time.sleep(2)
                    #本想验证一下代理是否可用，没成功
                    yield item
            next_page = hxs.xpath("//a[@class='next_page']/@href").extract_first()
            next_url = 'http://www.xicidaili.com' + next_page
            yield Request(next_url, callback=self.parse)
            print('__________')
#            time.sleep(3)


