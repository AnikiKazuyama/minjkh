# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy
from scrapy.loader.processors import TakeFirst


class MinjkhItem(scrapy.Item):
    company_description = scrapy.Field(output_processor=TakeFirst())
    company_working_time = scrapy.Field(output_processor=TakeFirst())
    company_name = scrapy.Field(output_processor=TakeFirst())
    company_city = scrapy.Field(output_processor=TakeFirst())
    company_adress = scrapy.Field(output_processor=TakeFirst())
    company_phone = scrapy.Field(output_processor=TakeFirst())
    company_manager = scrapy.Field(output_processor=TakeFirst())
    dispetcher_phone = scrapy.Field(output_processor=TakeFirst())
    inn = scrapy.Field(output_processor=TakeFirst())
    ogrn = scrapy.Field(output_processor=TakeFirst())
    email = scrapy.Field(output_processor=TakeFirst())
    site = scrapy.Field(output_processor=TakeFirst())
    region_name = scrapy.Field(output_processor=TakeFirst())
    region_fond = scrapy.Field(output_processor=TakeFirst())
