# -*- coding: utf-8 -*-
import scrapy
import re
import sys
import urllib
import urllib.request
import json
import time

from scrapy.spider import BaseSpider
from scrapy.selector import HtmlXPathSelector
from scrapy.http import Request
from tutorial.items import SoufangItem
from imp import reload
from random import randint

class SfSpider(scrapy.spider.Spider):
    
    name = "soufang_old_spider_shinan"
    allowed_domains = ["fang.com"]

    start_urls = []
    # 市南
    for i in range(1,101):
        start_urls.append('http://esf.qd.fang.com/integrate-a0389/'+'/i3'+str(i)+'/')

    handle_httpstatus_list = [404,403]

    def parse_detail(self, response):
        loc_hxst = scrapy.Selector(response)

#        loc_hxs = loc_hxst.xpath("//div[@class='trl-item1 w130']//div[contains(text(),'户型')]")
        loc_hxs = loc_hxst.xpath("//div[@class='font14' and contains(text(),'户型')]")
        huxing = loc_hxs.xpath("./preceding-sibling::*/text()").extract()
        if (type(huxing) == list):
            huxing = ''.join(huxing).replace('\r','').replace('\n','').replace('\t','')
        elif huxing is None:
            huxing = '信息缺失'

        loc_hxs = loc_hxst.xpath("//div[@class='font14' and contains(text(),'建筑面积')]")
        jianzhumianji = loc_hxs.xpath("./preceding-sibling::*/text()").extract()
        if (type(jianzhumianji) == list):
            jianzhumianji = ''.join(jianzhumianji).replace('\r','').replace('\n','').replace('\t','')
        elif jianzhumianji is None:
            jianzhumianji = '信息缺失'

        loc_hxs = loc_hxst.xpath("//div[@class='font14' and contains(text(),'单价')]")
        danjia = loc_hxs.xpath("./preceding-sibling::*/text()").extract()
        if (type(danjia) == list):
            danjia = ''.join(danjia).replace('\r','').replace('\n','').replace('\t','')
        elif danjia is None:
            danjia = '信息缺失'

        loc_hxs = loc_hxst.xpath("//div[@class='font14' and contains(text(),'朝向')]")
        chaoxiang = loc_hxs.xpath("./preceding-sibling::*/text()").extract()
        if (type(chaoxiang) == list):
            chaoxiang = ''.join(chaoxiang).replace('\r','').replace('\n','').replace('\t','')
        elif chaoxiang is None:
            chaoxiang = '信息缺失'

        loc_hxs = loc_hxst.xpath("//div[@class='font14' and contains(text(),'楼层')]")
        louceng = loc_hxs.xpath("./preceding-sibling::*/text()").extract()
        if (type(louceng) == list):
            louceng = ''.join(louceng).replace('\r','').replace('\n','').replace('\t','')
        elif louceng is None:
            louceng = '信息缺失'

        loc_hxs = loc_hxst.xpath("//div[@class='font14' and contains(text(),'装修')]")
        zhuangxiu = loc_hxs.xpath("./preceding-sibling::*/text()").extract()
        if (type(zhuangxiu) == list):
            zhuangxiu = ''.join(zhuangxiu).replace('\r','').replace('\n','').replace('\t','')
        elif zhuangxiu is None:
            zhuangxiu = '信息缺失'


        loc_hxs = loc_hxst.xpath("//span[@class='lab' and contains(text(),'物业类型')]")
        jianzhuniandai = loc_hxs.xpath("./following-sibling::*/text()").extract()
        if (type(jianzhuniandai) == list):
            jianzhuniandai = ''.join(jianzhuniandai).replace('\r','').replace('\n','').replace('\t','')
        elif jianzhuniandai is None:
            jianzhuniandai = '信息缺失'

        loc_hxs = loc_hxst.xpath("//span[@class='lab' and contains(text(),'有无电梯')]")
        dianti = loc_hxs.xpath("./following-sibling::*/text()").extract()
        if (type(dianti) == list):
            dianti = ''.join(dianti).replace('\r','').replace('\n','').replace('\t','')
        elif dianti is None:
            dianti = '信息缺失'

        loc_hxs = loc_hxst.xpath("//span[@class='lab' and contains(text(),'户型结构')]")
        huxingjiegou = loc_hxs.xpath("./following-sibling::*/text()").extract()
        if (type(huxingjiegou) == list):
            huxingjiegou = ''.join(huxingjiegou).replace('\r','').replace('\n','').replace('\t','')
        elif huxingjiegou is None:
            huxingjiegou = '信息缺失'

        loc_hxs = loc_hxst.xpath("//span[@class='lab' and contains(text(),'产权性质')]")
        chanquanxingzhi = loc_hxs.xpath("./following-sibling::*/text()").extract()
        if (type(chanquanxingzhi) == list):
            chanquanxingzhi = ''.join(chanquanxingzhi).replace('\r','').replace('\n','').replace('\t','')
        elif chanquanxingzhi is None:
            chanquanxingzhi = '信息缺失'


        loc_hxs = loc_hxst.xpath("//span[@class='lab' and contains(text(),'物业类型')]")
        wuyeleixing = loc_hxs.xpath("./following-sibling::*/text()").extract()
        if (type(wuyeleixing) == list):
            wuyeleixing = ''.join(wuyeleixing).replace('\r','').replace('\n','').replace('\t','')
        elif wuyeleixing is None:
            wuyeleixing = '信息缺失'

        loc_hxs = loc_hxst.xpath("//span[@class='lab' and contains(text(),'物业费用')]")
        wuyefeiyong = loc_hxs.xpath("./following-sibling::*/text()").extract()
        if (type(wuyefeiyong) == list):
            wuyefeiyong = ''.join(wuyefeiyong).replace('\r','').replace('\n','').replace('\t','')
        elif wuyefeiyong is None:
            wuyefeiyong = '信息缺失'

        loc_hxs = loc_hxst.xpath("//span[@class='lab' and contains(text(),'产权年限')]")
        chanquannianxian = loc_hxs.xpath("./following-sibling::*/text()").extract()
        if (type(chanquannianxian) == list):
            chanquannianxian = ''.join(chanquannianxian).replace('\r','').replace('\n','').replace('\t','')
        elif chanquannianxian is None:
            chanquannianxian = '信息缺失'

        loc_hxs = loc_hxst.xpath("//span[@class='lab' and contains(text(),'绿  化  率')]")
        lvhualv = loc_hxs.xpath("./following-sibling::*/text()").extract()
        if (type(lvhualv) == list):
            lvhualv = ''.join(lvhualv).replace('\r','').replace('\n','').replace('\t','')
        elif lvhualv is None:
            lvhualv = '信息缺失'

        loc_hxs = loc_hxst.xpath("//span[@class='lab' and contains(text(),'容  积  率')]")
        rongjilv = loc_hxs.xpath("./following-sibling::*/text()").extract()
        if (type(rongjilv) == list):
            rongjilv = ''.join(rongjilv).replace('\r','').replace('\n','').replace('\t','')
        elif rongjilv is None:
            rongjilv = '信息缺失'


        item = response.meta['item']
        item['jianzhumianji'] = jianzhumianji.encode('utf-8')
        item['huxing'] = huxing.encode('utf-8')
        item['chaoxiang'] = chaoxiang.encode('utf-8')
        item['danjia'] = danjia.encode('utf-8')
        item['louceng'] = louceng.encode('utf-8')
        item['zhuangxiu'] = zhuangxiu.encode('utf-8')
        item['jianzhuniajdai'] = jianzhuniandai.encode('utf-8')
        item['dianti'] = dianti.encode('utf-8')
        item['huxingjiegou'] = huxingjiegou.encode('utf-8')
        item['chanquanxingzhi'] = chanquanxingzhi.encode('utf-8')
        item['wuyeleixing'] = wuyeleixing.encode('utf-8')
        item['wuyefeiyong'] = wuyefeiyong.encode('utf-8')
        item['chanquannianxian'] = chanquannianxian.encode('utf-8')
        item['lvhualv'] = lvhualv.encode('utf-8')
        item['rongjilv'] = rongjilv.encode('utf-8')

        print('面积: %s' % jianzhumianji)
        print('户型: %s' % huxing)
        print('朝向: %s' % chaoxiang)
        print('楼层: %s' % louceng)
        print('装修: %s' % zhuangxiu)
        print('建筑年代: %s' % jianzhuniandai)
        print('电梯: %s' % dianti)
        print('户型结构: %s' % huxingjiegou)
        print('产权性质: %s' % chanquanxingzhi)
        print('物业类型: %s' % wuyeleixing)
        print('物业费用: %s' % wuyefeiyong)
        print('产权年限: %s' % chanquannianxian)
        print('绿化率: %s' % lvhualv)
        print('容积率: %s' % rongjilv)

        yield item

    def parse(self,response):
        reload(sys)
        print('__________')
        if response.status == 403:
            print('meet 403, sleep 600 sconds')
            time.sleep(1200)
            yield Request(response.url,callback=self.parse)
        #404,页面不存在，直接范围即可
        elif response.status == 404:
            print('meet 404,return')
        else:
            #获取小区列表网页的Response
            hxs = scrapy.Selector(response)
            #提取小区列表xpath格式数据。针对不同的网页，可能需要提取的class不同
            houselists = hxs.xpath("//dl[@class='list rel']")
            #第三层循环，提取每个小区的数据
            for house in houselists:
                item = SoufangItem()
                #获取房源描述title
                title = house.xpath(".//p[@class='title']//a/@title").extract_first()
                #获取房源链接
                link = "http://esf.qd.fang.com" + house.xpath(".//p[@class='title']//a/@href").extract_first()
                #获取房源类型、楼层、建筑年代等备注信息
#                   house_type = house.xpath(".//div[@class='mt12']/text()").extract()
#                   house_type = '|'.join(house_type)
                #获取房源名称
                xiaoqu = house.xpath(".//p[@class='mt10']//a/@title").extract_first()
                #获取房源地址
                address = house.xpath(".//p[@class='mt10']//span/text()").extract()
                if (type(address) == list):
                    address = ''.join(address)
                #获取建筑面积
#                   jianzhumianji = house.xpath(".//div[@class='area alignR']//p/text()").extract_first()
                #获取单价
#                   price = house.xpath(".//div[@class='danjia alignR mt5']/text()").extract()
                item['chengshi'] = '青岛'.encode('utf-8')
                item['quxian'] = '市南'.encode('utf-8')
                item['xiaoqu'] = xiaoqu.encode('utf-8')
                item['title'] = title.encode('utf-8')
                item['address'] = address.encode('utf-8')
                item['link'] = link.encode('utf-8')
#                   item['price'] = price.encode('utf-8')
                print('小区: %s'% xiaoqu)
                print('标题: %s'% title)
                print('地址: %s'% address)
                print('网址: %s'% link)
#                   print('价格: %s'% price)
                #进入子网址，爬其他信息
                yield  Request(link, callback=self.parse_detail, meta={'item': item})
                #延时三秒，避免机器人检测
                time.sleep(randint(2,4))
            print('__________')

