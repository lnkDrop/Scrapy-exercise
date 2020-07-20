# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class ArticlespiderItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass


class cnblogsItem(scrapy.Item):
    title = scrapy.Field()
    create_date = scrapy.Field()

    url = scrapy.Field()
    # MD5加密缩短url长度
    url_object_id = scrapy.Field()
    # 图片自动下载
    front_image_url = scrapy.Field()
    # 图片路径
    front_image_path = scrapy.Field()
    # 点赞数
    praise_nums = scrapy.Field()
    # 评论数
    comment_nums = scrapy.Field()
    # 查看数
    fav_nums = scrapy.Field()
    # 标签
    tags = scrapy.Field()
    # 内容
    content = scrapy.Field()
