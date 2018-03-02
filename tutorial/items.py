# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy
from scrapy.item import Item,Field


class TutorialItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass

class DmozItem(scrapy.Item):
    title = scrapy.Field()
    star = scrapy.Field()
    comment_num = scrapy.Field()
    link = scrapy.Field()
    location = scrapy.Field()

class SoufangItem(scrapy.Item):
    chengshi = scrapy.Field()
    quxian = scrapy.Field()
    xiaoqu = scrapy.Field()
    title = scrapy.Field()
    address = scrapy.Field()
    link = scrapy.Field()
    danjia = scrapy.Field()
    house_type = scrapy.Field()
    jianzhumianji = scrapy.Field()
    huxing = scrapy.Field()
    chaoxiang = scrapy.Field()
    louceng = scrapy.Field()
    zhuangxiu = scrapy.Field()
    jianzhuniandai = scrapy.Field()
    dianti = scrapy.Field()
    huxingjiegou = scrapy.Field()
    chanquanxingzhi = scrapy.Field()
    wuyeleixing = scrapy.Field()
    wuyefeiyong = scrapy.Field()
    chanquannianxian = scrapy.Field()
    lvhualv = scrapy.Field()
    rongjilv = scrapy.Field()

class AgentIPItem(scrapy.Item):
    IP = scrapy.Field()
    PORT = scrapy.Field()
    TYPE = scrapy.Field()
    proxyip = scrapy.Field()
