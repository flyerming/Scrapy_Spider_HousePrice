# -*- coding: utf-8 -*-
import scrapy
import time
import sys
from tutorial.changeip import ChangeIP

from scrapy.spider import BaseSpider
from scrapy.http import Request
from tutorial.items import SoufangItem
from imp import reload

class SfSpider(scrapy.spider.Spider):
    name = "soufang_old_spider_laoshan"
    allowed_domains = ["fang.com"]

    #    第一层循环，循环每个区县。胶南和即墨先不考虑。网址为精选网址链接
    #    start_urls_list = ['http://esf.qd.fang.com/integrate-a0389/',#市南
    #                       'http://esf.qd.fang.com/integrate-a0390/',#市北
    #                       'http://esf.qd.fang.com/integrate-a0391/',#四方
    #                       'http://esf.qd.fang.com/integrate-a0392/',#李沧
    #                       'http://esf.qd.fang.com/integrate-a0393/',#崂山
    #                       'http://esf.qd.fang.com/integrate-a0394/',#城阳
    #                       'http://esf.qd.fang.com/integrate-a01142/']#黄岛
    #    start_urls = []
    #    for start_url in start_urls_list:
    #        # 第二层循环，遍历每个区县中的列表页面数据
    #        for i in range(1,101):
    #            start_urls.append(start_url+'i3'+str(i)+'/')
    start_urls = []
    base_url = 'http://esf.qd.fang.com'
    handle_httpstatus_list = [404, 403]
    start_urls.append(base_url + '/integrate-a0393/i31')


    def parse(self, response):
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
            # 获取小区列表网页的Response
            hxs = scrapy.Selector(response)
            # 提取小区列表xpath格式数据。针对不同的网页，可能需要提取的class不同
            houselists = hxs.xpath("//dl[@class='list rel']")
            # 当网站验证码登录时，切换IP
            if houselists.extract_first() is None:
                #change ip
                Status = ChangeIP()
                print(Status)
                yield Request(response.url, callback=self.parse)
                return
            # 第三层循环，提取每个小区的数据
            for house in houselists:
                item = SoufangItem()
                # 获取房源描述title
                title = house.xpath(".//p[@class='title']//a/@title").extract_first()
                # 获取房源链接
                link = "http://esf.qd.fang.com" + house.xpath(".//p[@class='title']//a/@href").extract_first()
                # 获取房源类型、楼层、建筑年代等备注信息
                #                   house_type = house.xpath(".//div[@class='mt12']/text()").extract()
                #                   house_type = '|'.join(house_type)
                # 获取房源名称
                xiaoqu = house.xpath(".//p[@class='mt10']//a/@title").extract_first()
                # 获取房源地址
                address = house.xpath(".//p[@class='mt10']//span/text()").extract()
                if (type(address) == list):
                    address = ''.join(address)
                # 获取建筑面积
                #                   jianzhumianji = house.xpath(".//div[@class='area alignR']//p/text()").extract_first()
                # 获取单价
                #                   price = house.xpath(".//div[@class='danjia alignR mt5']/text()").extract()
                item['xiaoqu'] = xiaoqu.encode('utf-8')
                item['title'] = title.encode('utf-8')
                item['address'] = address.encode('utf-8')
                item['link'] = link.encode('utf-8')
                #                   item['price'] = price.encode('utf-8')
                print('小区: %s' % xiaoqu)
                print('标题: %s' % title)
                print('地址: %s' % address)
                print('网址: %s' % link)
                #                   print('价格: %s'% price)
                # 延时三秒，避免机器人检测
                #                time.sleep(randint(2,4))
                # 进入子网址，爬其他信息
                yield Request(link, callback=self.parse_detail, meta={'item': item})
            print('__________')
            next_page = hxs.xpath("//a[@id='PageControl1_hlk_next']/@href").extract_first()
            next_url = SfSpider.base_url + next_page
            yield Request(next_url, callback=self.parse)

    def parse_detail(self, response):
        loc_hxst = scrapy.Selector(response)

        loc_hxs = loc_hxst.xpath("//div[@class='font14' and contains(text(),'户型')]")
        huxing = loc_hxs.xpath("./preceding-sibling::*/text()").extract_first()
        if huxing is None:
            huxing = '信息缺失'
        else:
            huxing = huxing.replace('\r', '').replace('\n', '').replace('\t', '')
        loc_hxs = loc_hxst.xpath("//div[@class='font14' and contains(text(),'建筑面积')]")
        jianzhumianji = loc_hxs.xpath("./preceding-sibling::*/text()").extract_first()
        if jianzhumianji is None:
            jianzhumianji = '信息缺失'
        else:
            jianzhumianji = jianzhumianji.replace('\r', '').replace('\n', '').replace('\t', '')
        loc_hxs = loc_hxst.xpath("//div[@class='font14' and contains(text(),'单价')]")
        danjia = loc_hxs.xpath("./preceding-sibling::*/text()").extract_first()
        if danjia is None:
            danjia = '信息缺失'
        else:
            danjia = danjia.replace('\r', '').replace('\n', '').replace('\t', '')
        loc_hxs = loc_hxst.xpath("//div[@class='font14' and contains(text(),'朝向')]")
        chaoxiang = loc_hxs.xpath("./preceding-sibling::*/text()").extract_first()
        if chaoxiang is None:
            chaoxiang = '信息缺失'
        else:
            chaoxiang = chaoxiang.replace('\r', '').replace('\n', '').replace('\t', '')
        loc_hxs = loc_hxst.xpath("//div[@class='font14' and contains(text(),'楼层')]")
        louceng = loc_hxs.xpath("./preceding-sibling::*/text()").extract_first() + loc_hxst.xpath("//div[@class='font14' and contains(text(),'楼层')]/text()").extract_first()
        if louceng is None:
            louceng = '信息缺失'
        else:
            louceng = louceng.replace('\r', '').replace('\n', '').replace('\t', '')
        loc_hxs = loc_hxst.xpath("//div[@class='font14' and contains(text(),'装修')]")
        zhuangxiu = loc_hxs.xpath("./preceding-sibling::*/text()").extract_first()
        if zhuangxiu is None:
            zhuangxiu = '信息缺失'
        else:
            zhuangxiu = zhuangxiu.replace('\r', '').replace('\n', '').replace('\t', '')
        loc_hxs = loc_hxst.xpath("//span[@class='lab' and contains(text(),'建筑年代')]")
        jianzhuniandai = loc_hxs.xpath("./following-sibling::*/text()").extract_first()
        if jianzhuniandai is None:
            jianzhuniandai = '信息缺失'
        else:
            jianzhuniandai = jianzhuniandai.replace('\r', '').replace('\n', '').replace('\t', '')
        loc_hxs = loc_hxst.xpath("//span[@class='lab' and contains(text(),'有无电梯')]")
        dianti = loc_hxs.xpath("./following-sibling::*/text()").extract_first()
        if dianti is None:
            dianti = '信息缺失'
        else:
            dianti = dianti.replace('\r', '').replace('\n', '').replace('\t', '')
        loc_hxs = loc_hxst.xpath("//span[@class='lab' and contains(text(),'户型结构')]")
        huxingjiegou = loc_hxs.xpath("./following-sibling::*/text()").extract_first()
        if huxingjiegou is None:
            huxingjiegou = '信息缺失'
        else:
            huxingjiegou = huxingjiegou.replace('\r', '').replace('\n', '').replace('\t', '')
        loc_hxs = loc_hxst.xpath("//span[@class='lab' and contains(text(),'产权性质')]")
        chanquanxingzhi = loc_hxs.xpath("./following-sibling::*/text()").extract_first()
        if chanquanxingzhi is None:
            chanquanxingzhi = '信息缺失'
        else:
            chanquanxingzhi = chanquanxingzhi.replace('\r', '').replace('\n', '').replace('\t', '')
        loc_hxs = loc_hxst.xpath("//span[@class='lab' and contains(text(),'物业类型')]")
        wuyeleixing = loc_hxs.xpath("./following-sibling::*/text()").extract_first()
        if wuyeleixing is None:
            wuyeleixing = '信息缺失'
        else:
            wuyeleixing = wuyeleixing.replace('\r', '').replace('\n', '').replace('\t', '')
        loc_hxs = loc_hxst.xpath("//span[@class='lab' and contains(text(),'物业费用')]")
        wuyefeiyong = loc_hxs.xpath("./following-sibling::*/text()").extract_first()
        if wuyefeiyong is None:
            wuyefeiyong = '信息缺失'
        else:
            wuyefeiyong = wuyefeiyong.replace('\r', '').replace('\n', '').replace('\t', '')
        loc_hxs = loc_hxst.xpath("//span[@class='lab' and contains(text(),'产权年限')]")
        chanquannianxian = loc_hxs.xpath("./following-sibling::*/text()").extract_first()
        if chanquannianxian is None:
            chanquannianxian = '信息缺失'
        else:
            chanquannianxian = chanquannianxian.replace('\r', '').replace('\n', '').replace('\t', '')
        loc_hxs = loc_hxst.xpath("//span[@class='lab' and contains(text(),'绿  化  率')]")
        lvhualv = loc_hxs.xpath("./following-sibling::*/text()").extract_first()
        if lvhualv is None:
            lvhualv = '信息缺失'
        else:
            lvhualv = lvhualv.replace('\r', '').replace('\n', '').replace('\t', '')
        loc_hxs = loc_hxst.xpath("//span[@class='lab' and contains(text(),'容  积  率')]")
        rongjilv = loc_hxs.xpath("./following-sibling::*/text()").extract_first()
        if rongjilv is None:
            rongjilv = '信息缺失'
        else:
            rongjilv = rongjilv.replace('\r', '').replace('\n', '').replace('\t', '')

        item = response.meta['item']

        # 检验是否网页读取异常更换IP
        if (jianzhumianji == '信息缺失') and \
                (huxing == '信息缺失') and \
                (chaoxiang == '信息缺失') and \
                (danjia == '信息缺失') and \
                (louceng == '信息缺失') and \
                (zhuangxiu == '信息缺失') and \
                (jianzhuniandai == '信息缺失') and \
                (dianti == '信息缺失') and \
                (huxingjiegou == '信息缺失') and \
                (chanquanxingzhi == '信息缺失') and \
                (wuyeleixing == '信息缺失') and \
                (wuyefeiyong == '信息缺失') and \
                (chanquannianxian == '信息缺失') and \
                (lvhualv == '信息缺失') and \
                (rongjilv == '信息缺失'):
            #change ip

            Status = ChangeIP()
            print(Status)
            yield Request(response.url, callback=self.parse_detail, meta={'item': item})
            return

        item['jianzhumianji'] = jianzhumianji.encode('utf-8')
        item['huxing'] = huxing.encode('utf-8')
        item['chengshi'] = "青岛".encode('utf-8')
        item['quxian'] = "市南".encode('utf-8')
        item['chaoxiang'] = chaoxiang.encode('utf-8')
        item['danjia'] = danjia.encode('utf-8')
        item['louceng'] = louceng.encode('utf-8')
        item['zhuangxiu'] = zhuangxiu.encode('utf-8')
        item['jianzhuniandai'] = jianzhuniandai.encode('utf-8')
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

    def closed(self, reason):  # 爬取结束的时候发送邮件
        from scrapy.mail import MailSender

        # mailer = MailSender.from_settings(settings)# 出错了，没找到原因
        mailer = MailSender(
            smtphost="smtp.sohu.com",  # 发送邮件的服务器
            mailfrom="scrapy@sohu.com",  # 邮件发送者
            smtpuser="scrapy@sohu.com",  # 用户名
            smtppass="scrapy123",  # 发送邮箱的密码不是你注册时的密码，而是授权码！！！切记！
            smtpport=25  # 端口号
        )
        body = u""" 
        青岛崂山完成，请核查是程序是否异常退出，以及程序爬取数目是否正确，若正常，则进行下一个。 
        """
        subject = u'青岛崂山完成'
        # 如果说发送的内容太过简单的话，很可能会被当做垃圾邮件给禁止发送。
#        mailer.send(to=["flyerming@163.com", "mengwmk@163.com"], subject=subject.encode("utf-8"), body=body.encode("utf-8"))
        mailer.send(to=["flyerming@163.com", "mengwmk@163.com"], subject=subject, body=body)
