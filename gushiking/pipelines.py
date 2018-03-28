# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import json


class GushikingPipeline(object):
    def open_spider(self,spider):
        self.fp = open('qutu.json','w',encoding='utf8')
    def process_item(self, item, spider):
        obj = dict(item)
        string = json.dumps(obj,ensure_ascii=False)
        self.fp.write(string)
        print('&'*30)
        return item
    def close_spider(self,spider):
        self.fp.close()
