# -*- coding: utf-8 -*-
from scrapy_redis.spiders import RedisSpider
import scrapy
from recruit.items import RecruitItem
from scrapy.utils.project import get_project_settings
from recruit.pipelines import RecruitPipeline
import re
import time

a = RecruitPipeline()
sql = 'select companyId from xmrc_list where companyId not in (select companyId from xmrc_details);;'
aList = []
a.query_mysql(aList, sql)


class XmrcSpider(scrapy.Spider):
    name = 'xmrc'
    allowed_domains = ['xmrc.com']
    # redis_key = 'xmrcUrl'
    # settings = get_project_settings()
    # price_url = settings['PRICE_URL']
    # price_request = scrapy.Request(price_url.format(num), callback=self.get_price)
    start_urls = aList

    def parse(self, response):
        # with open("xmrc.html", "w", encoding="utf-8") as f:
        #     f.write(response.text)
        # items = []

        eachre = response.xpath('//*[@id="container"]/table[2]/tr/td[3]/table[4]/tr[1]/td[2]/table//text()').extract()
        phone2 = re.findall(r"1\d{10}", str(eachre))
        # print(set(eachre))
        # print(phone2)
        each = response.xpath('//*[@id="container"]/table[2]/tr/td[3]/table[4]/tr[1]/td[2]/table')

        item = RecruitItem()
        company = response.xpath('//*[@id="logo_td2"]/text()').extract()
        name = each.xpath('./tr[2]//text()').extract()
        phone = each.xpath('./tr[3]//text()').extract()

        item['company'] = None      #company[0].strip()
        item['name'] = name[3].strip()[7:]
        item['phone'] = phone[3].strip()[6:]
        # try:
        #     fax = each.xpath('./tr[4]//text()').extract()
        #     int(fax[3].strip()[6:9])
        #     address = each.xpath('./tr[5]//text()').extract()
        #     # nature = each.xpath('./tr[11]//text()').extract()
        #     industry = each.xpath('./tr[12]//text()').extract()
        #     # scale = each.xpath('./tr[13]//text()').extract()
        #     synopsis = each.xpath('./tr[15]//text()').extract()
        #
        #     item['fax'] = fax[3].strip()[6:]
        #     item['address'] = address[3].strip()[6:]
        #     # item['nature'] = nature[3].strip()[6:]
        #     item['industry'] = industry[3].strip()[6:]
        #     # item['scale'] = scale[3].strip()[6:]
        #     # item['mobile_phone'] = None
        #     # if len(address[3].strip()[6:]) < 12:
        #     #     address = each.xpath('./tr[5]//text()').extract()
        #     #     item['address'] = address[3].strip()[6:]
        #
        # except:
        item['fax'] = None
        address = each.xpath('./tr[4]//text()').extract()
        item['address'] = address[3].strip()[6:]
        if address[3].strip()[6:7] == '1':
            address = each.xpath('./tr[5]//text()').extract()
            item['address'] = address[3].strip()[6:]
        industry = each.xpath('./tr[10]//text()').extract()

        synopsis = each.xpath('./tr[12]//text()').extract()
        item['address'] = address[3].strip()[6:]
        item['industry'] = industry[3].strip()[6:]

        if len(set(phone2)) == 1:
            item['mobile_phone'] = phone2[0]
            if phone2[0] == item['fax']:
                item['fax'] = None
        elif len(set(phone2)) == 2:
            item['fax'] = phone2[0]
            item['mobile_phone'] = phone2[1]

        synopsis2 = ''
        for synopsis_each in range(len(synopsis)):
            synopsis2 += synopsis[synopsis_each].strip()
            if synopsis2[:5] == '$(fun' or synopsis2[:6] == '单位其它详情' or synopsis2[:4] == '点击查看':
                synopsis2 = ''

        # print(item)
        if len(synopsis2) < 20:
            synopsis = each.xpath('./tr[14]//text()').extract()
            synopsis2 = ''
            for synopsis_each in range(len(synopsis)):
                synopsis2 += synopsis[synopsis_each].strip()
            if synopsis2[:5] == '$(fun' or synopsis2[:6] == '单位其它详情' or synopsis2[:4] == '点击查看':
                synopsis2 = ''
        if len(synopsis2) < 20:
            synopsis = each.xpath('./tr[13]//text()').extract()
            synopsis2 = ''
            for synopsis_each in range(len(synopsis)):
                synopsis2 += synopsis[synopsis_each].strip()
            if synopsis2[:5] == '$(fun' or synopsis2[:6] == '单位其它详情' or synopsis2[:4] == '点击查看':
                synopsis2 = ''
        if len(synopsis2) < 20:
            synopsis = each.xpath('./tr[11]//text()').extract()
            synopsis2 = ''
            for synopsis_each in range(len(synopsis)):
                synopsis2 += synopsis[synopsis_each].strip()
            if synopsis2[:5] == '$(fun' or synopsis2[:6] == '单位其它详情' or synopsis2[:4] == '点击查看':
                synopsis2 = ''
        if len(synopsis2) < 20:
            synopsis = each.xpath('./tr[10]//text()').extract()
            synopsis2 = ''
            for synopsis_each in range(len(synopsis)):
                synopsis2 += synopsis[synopsis_each].strip()
            if synopsis2[:5] == '$(fun' or synopsis2[:6] == '单位其它详情' or synopsis2[:4] == '点击查看':
                synopsis2 = ''
        if len(synopsis2) < 20:
            synopsis = each.xpath('./tr[15]//text()').extract()
            synopsis2 = ''
            for synopsis_each in range(len(synopsis)):
                synopsis2 += synopsis[synopsis_each].strip()
            if synopsis2[:5] == '$(fun' or synopsis2[:6] == '单位其它详情' or synopsis2[:4] == '点击查看':
                synopsis2 = ''
        if phone[3].strip()[6:9] == '(合则':
            item['phone'] = None
        item['synopsis'] = synopsis2
        item['companyId'] = response.url[23:]
        item['industry'] = None
        print(item)
        yield item



