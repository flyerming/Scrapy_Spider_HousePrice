from scrapy import cmdline
#cmdline.execute("scrapy crawl soufang_old_spider -t csv -o sfqdes20180302.csv --loglevel=INFO".split())
cmdline.execute("scrapy crawl soufang_old_spider_shinan -t csv -o sfqdes20180302sn.csv --loglevel=INFO".split());
#cmdline.execute("scrapy crawl soufang_old_spider_shibei -t csv -o sfqdes20180302sb.csv --loglevel=INFO".split());
#cmdline.execute("scrapy crawl soufang_old_spider_laoshan -t csv -o sfqdes20180302ls.csv --loglevel=INFO".split());
#cmdline.execute("scrapy crawl soufang_old_spider_huangdao -t csv -o sfqdes20180302hd.csv --loglevel=INFO".split());
#cmdline.execute("scrapy crawl soufang_old_spider_sifang -t csv -o sfqdes20180302sf.csv --loglevel=INFO".split());
#cmdline.execute("scrapy crawl soufang_old_spider_licang -t csv -o sfqdes20180302lc.csv --loglevel=INFO".split());
