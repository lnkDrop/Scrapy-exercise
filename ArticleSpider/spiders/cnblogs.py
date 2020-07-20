# -*- coding: utf-8 -*-
from urllib import parse
import re
import scrapy
from scrapy import Request
import requests
import json
from items import cnblogsItem
from utils import common


class CnblogsSpider(scrapy.Spider):
    name = 'cnblogs'
    allowed_domains = ['https://news.cnblogs.com/']
    start_urls = ['https://news.cnblogs.com/']

    def parse(self, response):
        """
        1.获取url并交给scrapy进行解析
        2.获取下一页的url交给scrapy进行下载，下载完成后交给parse继续跟进
        :param response:
        :return:
        """
        # Xpath选择器
        # url = response.xpath('//div[@id="news_list"]//h2[@class="news_entry"]/a/@href').extract()
        # css 选择器
        post_nodes = response.css('#news_list .news_block')[:1]
        for post_node in post_nodes:
            image_url = post_node.css('.entry_summary a img::attr(src)').extract_first("")
            post_url = post_node.css('h2 a::attr(href)').extract_first("")
            # 每遇到url就交出并下载
            yield Request(url=parse.urljoin(response.url, post_url), meta={"front_image_url": image_url},
                          callback=self.parse_detail, dont_filter=True)  # 下载完成后调用的方法

        # 提取下一页并交给scrapy进行下载

        # next_url = response.xpath('//a[contains(text(),"Next >")]/@href').extract_first("")
        # next_url = response.css("div.pager a:last-chile::text").extract_first("")
        # yield Request(url=parse.urljoin(response.url, next_url), callback=
        # self.parse)

    def parse_detail(self, response):
        # article_item = cnblogsItem()
        # 详情页id
        mach_re = re.match(".*?(\d+)", response.url)
        if mach_re:
            post_id = mach_re.group(1)

            article_itm = cnblogsItem()

            # 标题
            title = response.css("#news_title a::text").extract_first("")
            # 创建时间
            create_date = response.css("#news_info .time::text").extract_first("")
            # 正则提取时间数字
            match_re = re.match(".*?(\d+.*)", create_date)
            # 如果有匹配到则生成
            if mach_re:
                create_date = match_re.group(1)
            content = response.css("#news_content").extract()[0]
            tageslist = response.css(".news_tags a::text").extract()
            tags = ",".join(tageslist)

            # html = requests.get(parse.urljoin(response.url,
            #                                   "/NewsAjax/GetAjaxNewsInfo?contentId={}".format(
            #                                       post_id)))
            # j_data = json.loads(html.text)

            article_itm["title"] = title
            article_itm["create_date"] = create_date
            article_itm["content"] = content
            article_itm["tags"] = tags
            article_itm["title"] = title
            article_itm["title"] = title
            article_itm["front_image_url"] = [response.meta.get("front_image_url", "")]
            article_itm["url"] = response.url
            yield Request(url=parse.urljoin(response.url, "/NewsAjax/GetAjaxNewsInfo?contentId={}".format(
                post_id)), meta={"article_itm": article_itm}, callback=self.parse_nums, dont_filter=True)

        # article_item["title"] = title
        # article_item["create_date"] = create_date
        # article_item["content"] = content
        # article_item["tags"] = tags
        #
        # yield Request(url=parse.urljoin(response.url), meta={"article_item": article_item}, callback=self.parse_nums)

    def parse_nums(self, response):
        j_data = json.loads(response.text)
        article_itm = response.meta.get("article_itm", "")

        praise_nums = j_data["DiggCount"]
        fav_nums = j_data["TotalView"]
        comment_nums = j_data["CommentCount"]

        article_itm["praise_nums"] = praise_nums
        article_itm["fav_nums"] = fav_nums
        article_itm["comment_nums"] = comment_nums
        article_itm["url_object_id"] = common.get_Md5(article_itm["url"])


        # yield itm会自动加载pipelines进行入库处理
        yield article_itm
