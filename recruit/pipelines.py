# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import pymysql
from scrapy.utils.project import get_project_settings


class RecruitPipeline(object):
    def __init__(self):

        self.settings = get_project_settings()
        self.connect = pymysql.connect(
            host=self.settings['MYSQL_HOST'],
            port=self.settings['MYSQL_PORT'],
            db=self.settings['MYSQL_DBNAME'],
            user=self.settings['MYSQL_USER'],
            passwd=self.settings['MYSQL_PASSWD'],
            charset=self.settings['MYSQL_CHARSET'],
            use_unicode=True
         )
        self.cursor = self.connect.cursor()

    def process_item(self, item, spider):

        # sql = 'insert into recruit.xmrc_details(company,name,phone,fax,address,nature,industry,scale,synopsis,)' \
        #       'values(%s,%s,%s,%s,%s,%s,%s,%s,%s)'
        #
        # self.cursor.execute(sql, (item['company'],item['name'],item['phone'],item['fax'],item['address'],
        #                           item['nature'],item['industry'],item['scale'],item['synopsis']))
        # print("mysql商品详情信息插入成功")
        # self.connect.commit()

        table = 'xmrc_details'
        data = item
        keys = ','.join(data.keys())
        values = ','.join(['%s'] * len(data))

        sql = 'INSERT INTO {table}({keys}) VALUES  ({values}) ON DUPLICATE KEY UPDATE '.format(table=table,
                                                                                               keys=keys,
                                                                                               values=values)
        update = ','.join(["{key} = %s".format(key=key) for key in data])
        sql += update
        try:
            if self.cursor.execute(sql, tuple(data.values()) * 2):
                print('Successful')
                self.connect.commit()
        except:
            print('Failed')
            self.connect.rollback()
        # keys = ','.join(data.keys())
        # values = ','.join(['%s'] * len(data))
        #
        # sql = 'INSERT INTO {table}({keys}) VALUES ({values})'.format(table=table, keys=keys, values=values)
        # try:
        #     if self.cursor.execute(sql, tuple(data.values())):
        #         # print('Successful', data)
        #         self.connect.commit()
        # except:
        #     print('Failed', data)
        #     # self.wrongList.append(data)
        #     self.connect.rollback()

    # def close_spider(self, spider):
    #     # 关闭mysql
    #     self.cursor.close()
    #     self.connect.close()

    def query_mysql(self, a, *args):
        self.cursor.execute(*args)
        result = self.cursor.fetchall()
        # print(len(result))
        for i in result:
            queryUrl = 'https://www.xmrc.com.cn' + i[0]
            a.append(queryUrl)



