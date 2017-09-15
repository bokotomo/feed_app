# -*- coding: utf-8 -*-
import scrapy
import re
import json
import os
from os import path
from datetime import datetime as dt
from scrapy import Selector
from scrapy import signals
from scrapy.selector import HtmlXPathSelector
from feedauto.items import FeedItem
from feedauto.spiders.message_manager import MessageManager
from scrapy.spidermiddlewares.httperror import HttpError
from twisted.internet.error import DNSLookupError
from twisted.internet.error import TimeoutError, TCPTimedOutError

class FeedSpider(scrapy.Spider):
    '''
    スクレイピングしてdataフォルダに保存する
    '''
    name = 'feed'
    debug_flag = False
    #debug_flag = True
    def start_requests(self):
        '''
        リクエストを送るときに呼び出される
        '''
        APP_ROOT = path.dirname(path.abspath( __file__ ))
        #url = "https://hacker-news.firebaseio.com/v0/topstories.json?print=pretty"
        url = "https://hacker-news.firebaseio.com/v0/newstories.json?print=pretty"
        metas = {
        }
        res = scrapy.Request(
            url=url,
            method="GET",
            callback=self.parse,
            errback=self.errback,
            meta=metas
        )
        yield res
        url = "https://github.com/trending"
        metas = {
        }
        res = scrapy.Request(
            url=url,
            method="GET",
            callback=self.parse3,
            errback=self.errback,
            meta=metas
        )
        yield res

    def errback(self, failure):
        # error処理
        if failure.check(HttpError):
            response = failure.value.response
            text = "200以外のリクエスト : "+response.url
            print(text)
        elif failure.check(DNSLookupError):
            text = "DNSLookupError : "
            print(text)
        elif failure.check(TimeoutError, TCPTimedOutError):
            text = "TimeoutError : "
            print(text)
        else:
            text = "Error : "+str(failure)
            print(text)
    
    def parse(self, response):
        '''
        非同期でリクエストすると呼び出される
        '''
        print("----------------------------------=")
        html = response.text
        d = json.loads(html)
        count = 0
        for v in d:
            url = "https://hacker-news.firebaseio.com/v0/item/%s.json?print=pretty" % v
            metas = {
            }
            res = scrapy.Request(
                url=url,
                callback=self.parse2,
                errback=self.errback,
                meta=metas
            )
            count += 1
            max_count = 500
            if count <= max_count:
                yield res

    def parse2(self, response):
        '''
        非同期でリクエストすると呼び出される
        '''
        self.response_params = response.meta
        d = json.loads(response.text)
        title = ""
        k = "title"
        if k in d:
            title = d[k]
        url = ""
        k = "url"
        if k in d:
            url = d[k]
        time = ""
        k = "time"
        if k in d:
            time = d[k]
        story_id = 0
        k = "id"
        if k in d:
            story_id = d[k]
        score = 0
        k = "score"
        if k in d:
            score = d[k]
        user = ""
        k = "user"
        if k in d:
            user = d[k]
        category = self.__get_category(url)
        if not category:
            category = self.__get_category(title)
        item = FeedItem(
            title = title,
            url = url,
            time = time,
            story_id = story_id,
            score = score,
            user = user,
            category = category,
            site = "hacker"
        )
        yield item

    def parse3(self, response):
        '''
        非同期でリクエストすると呼び出される
        '''
        print("----------------------------------=")
        #print(response.text)
        li_tags = response.xpath("//ol[@class='repo-list']/li").extract()
        for li in li_tags:
            li_sel = Selector(text=li, type="html")
            a = li_sel.xpath("//h3/a/@href").extract_first()
            url = "https://github.com/"+a
            star = li_sel.xpath("//div[@class='f6 text-gray mt-2']/a/text()").extract_first()
            title = li_sel.xpath("//div[@class='py-1']/p/text()").extract_first()
            title = title.replace("\n", "")
            title = title.replace("\t", "")
            title = title.replace("\r", "")
            if not title:
                title = li_sel.xpath("//h3/a/span/text()").extract_first()
            item = FeedItem(
                title = title,
                url = url,
                time = 0,
                story_id = 0,
                score = star,
                user = "",
                category = "",
                site = "github"
            )
            yield item

    def __get_category(self, text):
        # カテゴリーを返す
        c = ""
        text = text.lower()
        if "github" in text:
            c = "IT"
        elif "michaelburge.us" in text:
            c = "IT"
        elif "insightdatascience.com" in text:
            c = "IT"
        elif "uxmag.com" in text:
            c = "UI/UX"
        elif "atom.io" in text:
            c = "IT"
        elif "techmeme.com" in text:
            c = "IT"
        elif "cybertriage.com" in text:
            c = "IT"
        elif "unubo.com" in text:
            c = "IT"
        elif "engadget.com" in text:
            c = "IT"
        elif "userlytics.com" in text:
            c = "IT"
        elif "robotics.ovh" in text:
            c = "IT"
        elif "emlid.com" in text:
            c = "IT"
        elif "kickstarter" in text:
            c = "IT"
        elif "developer" in text:
            c = "IT"
        elif "arxiv" in text:
            c = "IT"
        elif "node.js" in text:
            c = "IT"
        elif "threads" in text:
            c = "IT"
        elif "database" in text:
            c = "IT"
        elif "machine" in text:
            c = "IT"
        elif "amazon" in text:
            c = "IT"
        elif "ceo" in text:
            c = "IT"
        elif "redshift" in text:
            c = "IT"
        elif "java" in text:
            c = "IT"
        elif "deeplearning" in text:
            c = "IT"
        elif "tech" in text:
            c = "IT"
        elif "tomdale" in text:
            c = "IT"
        elif "medium" in text:
            c = "Medium"
        elif "arstechnica" in text:
            c = "IT"
        elif "gridlesskits" in text:
            c = "IT"
        elif "techdirt" in text:
            c = "IT"
        elif "siliconangle" in text:
            c = "IT"
        elif "yanisvaroufakis" in text:
            c = "IT"
        elif "quora" in text:
            c = "IT"
        elif "hack" in text:
            c = "IT"
        elif "program" in text:
            c = "IT"
        elif "bitcoin" in text:
            c = "IT"
        elif "cpu" in text:
            c = "IT"
        elif "blockchain" in text:
            c = "IT"
        elif "youtube" in text:
            c = "IT"
        elif "aws" in text:
            c = "IT"
        elif "python" in text:
            c = "IT"
        elif "docker" in text:
            c = "IT"
        elif "google" in text:
            c = "IT"
        elif "swift" in text:
            c = "IT"
        elif "apple" in text:
            c = "IT"
        elif "windows" in text:
            c = "IT"
        elif "snapchat" in text:
            c = "IT"
        elif "vps" in text:
            c = "IT"
        elif "microsoft" in text:
            c = "IT"
        elif "php" in text:
            c = "IT"
        elif "rust" in text:
            c = "IT"
        elif "linux" in text:
            c = "IT"
        elif "instagram" in text:
            c = "IT"
        elif "facebook" in text:
            c = "IT"
        elif "hasaranga" in text:
            c = "IT"
        elif "firebase" in text:
            c = "IT"
        elif "Tesla" in text:
            c = "IT"
        elif "hdmi" in text:
            c = "IT"
        elif "ghz" in text:
            c = "IT"
        elif "tesla" in text:
            c = "IT"
        elif "security" in text:
            c = "IT"
        elif "clubhouse" in text:
            c = "IT"
        elif "software" in text:
            c = "IT"
        elif "apps" in text:
            c = "IT"
        elif "xcode" in text:
            c = "IT"
        elif "server" in text:
            c = "IT"
        elif "cto" in text:
            c = "IT"
        elif "slack" in text:
            c = "IT"
        elif "device" in text:
            c = "IT"
        elif "chrome" in text:
            c = "IT"
        elif "safari" in text:
            c = "IT"
        elif "ascII" in text:
            c = "IT"
        elif "cern" in text:
            c = "IT"
        elif "bloomberg" in text:
            c = "Market"
        elif "marketing" in text:
            c = "Market"
        elif "pdca" in text:
            c = "Market"
        elif "branding" in text:
            c = "Market"
        elif "electronic" in text:
           c = "UI/UX"
        elif "thecollegefix" in text:
            c = "Student"
        return c

    def delete_dust_text(self, text):
        # 必要のない文字を削除
        if text is None:
            return ""
        t = text.replace(" ", "") 
        t = t.replace("　", "") 
        t = t.replace("\n", "") 
        t = t.replace("\t", "") 
        t = t.replace("\r", "") 
        return t

