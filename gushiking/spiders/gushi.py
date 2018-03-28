# -*- coding: utf-8 -*-
import os
import scrapy

from gushiking.items import GushikingItem


class GushiSpider(scrapy.Spider):
    name = 'gushi'
    allowed_domains = ['www.gushiking.com']
    start_urls = ['http://www.gushiking.com/gaoxiao/index.htm']

    page = 1
    url = 'http://www.gushiking.com/new/p%s.htm'


    def parse(self, response):
        div_list = response.xpath('//div[@id="container"]/div[@class="left"]/div[@class="leftcon"]')
        for div in div_list:
            item = GushikingItem()
            item['title'] = div.xpath('./div[@class="pic"]/h1[@align="left"]/a/text()').extract_first()
            publish_time = div.xpath('./div[@class="pic"]/div[@class="ustag"]/text()').extract_fitst()
            item['time'] = publish_time.strip('\r\n ')
            item['qudu'] = div.xpath('./div[@class="pic"]/div[@class="ustag"]/a[2]/text()').extract_first()
            item['image_url'] = div.xpath().extract_first()
            print(item['image_url'])
            print(item['title'])
            yield item
            # 在这里就可以向图片的地址发送请求，然后下载图片
            # 通过scrapy发送的请求，会自己主动带referer这个参数，
            # 该参数就是response的请求url，所以去下载防盗链图片的时候，在这里进行下载即可
            yield scrapy.Request(url=item['image_url'],callback=self.parse_image)

        self.page+=1
        if self.page<=10:
            url = self.url%self.page
            yield scrapy.Request(url=url,callback=self.parse)
    # 下载图片
    def parse_image(self,response):
        dirname = r'F:/data'
        print(dirname)
        filename = os.path.basename(response.url)
        filepath = os.path.join(dirname,filename)
        print(response.body)
        print('*'*30)
        with open(filepath,'wb') as fp:
            fp.write(response.body)

