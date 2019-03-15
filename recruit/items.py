# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class RecruitItem(scrapy.Item):
    # define the fields for your item here like:
    company = scrapy.Field()    # 公司名称
    name = scrapy.Field()       # 联系人
    phone = scrapy.Field()      # 联系电话
    fax = scrapy.Field()        # 传真
    address = scrapy.Field()    # 公司地址
    mobile_phone = scrapy.Field()  # 移动电话
    industry = scrapy.Field()   # 行业
    companyId = scrapy.Field()    # 网址
    synopsis = scrapy.Field()   # 简介

