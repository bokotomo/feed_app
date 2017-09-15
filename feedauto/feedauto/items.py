# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class FeedItem(scrapy.Item):
    title = scrapy.Field()
    url = scrapy.Field()
    time = scrapy.Field()
    story_id = scrapy.Field()
    score = scrapy.Field()
    user = scrapy.Field()
    category = scrapy.Field()
    site = scrapy.Field()

