from scrapy import cmdline
#首先，获取代理IP地址.注意代理IP的种类和爬虫网址的种类，区分HTTP和HTTPS,在代码中已经集成了HTTP筛选
#爬取完成代理IP需要将代理ip地址填写到setting中，注意填写的时候，根据访问网址HTTP还是HTTPS进行筛选
#注意，爬取的网址不易使用太多，否则程序莫名异常
#cmdline.execute("scrapy crawl agency_ip2_collector -t csv -o IpAgent.csv --loglevel=INFO".split())
#然后，使用代理IP地址进行爬虫。
cmdline.execute("scrapy crawl soufang_old_spider -t csv -o sfqdes20180301.csv --loglevel=INFO".split())
#cmdline.execute("scrapy crawl soufang_old_spider_shinan -t csv -o sfqdes20180301sn.csv --loglevel=INFO".split())
#cmdline.execute("scrapy crawl soufang_old_spider_shibei -t csv -o sfqdes20180301sb.csv --loglevel=INFO".split())
#cmdline.execute("scrapy crawl soufang_old_spider_sifang -t csv -o sfqdes20180301sf.csv --loglevel=INFO".split())
#cmdline.execute("scrapy crawl soufang_old_spider_licang -t csv -o sfqdes20180301lc.csv --loglevel=INFO".split())
#cmdline.execute("scrapy crawl soufang_old_spider_laoshan -t csv -o sfqdes20180301ls.csv --loglevel=INFO".split())
#cmdline.execute("scrapy crawl soufang_old_spider_huangdao -t csv -o sfqdes20180301hd.csv --loglevel=INFO".split())
