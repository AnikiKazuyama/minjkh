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

# Founders info


class FounderOrBenefItem(scrapy.Item):
    company_id = scrapy.Field(output_processor=TakeFirst())
    name = scrapy.Field(output_processor=TakeFirst())
    inn = scrapy.Field(output_processor=TakeFirst())
    grazhdanstvo_registration = scrapy.Field(output_processor=TakeFirst())


class Founder(FounderOrBenefItem):
    votes = scrapy.Field(output_processor=TakeFirst())


class Beneficiar(FounderOrBenefItem):
    share = scrapy.Field(output_processor=TakeFirst())


# Banks info
class Bank():
    company_id = scrapy.Field(output_processor=TakeFirst())
    name = scrapy.Field(output_processor=TakeFirst())
    payment_account = scrapy.Field()
    pnc = scrapy.Field()
    inn = scrapy.Field(output_processor=TakeFirst())
    ogrn = scrapy.Field(output_processor=TakeFirst())
    bik = scrapy.Field(output_processor=TakeFirst())


class Associacions(FounderOrBenefItem):
    company_id = scrapy.Field(output_processor=TakeFirst())
    name = scrapy.Field(output_processor=TakeFirst())
    inn = scrapy.Field(output_processor=TakeFirst())
    org_type = scrapy.Field(output_processor=TakeFirst())


# Main info


class OurHouseItem(scrapy.Item):
    id = scrapy.Field(output_processor=TakeFirst())
    name = scrapy.Field(output_processor=TakeFirst())
    company_group_name = scrapy.Field(output_processor=TakeFirst())
    adress = scrapy.Field(output_processor=TakeFirst())
    ur_adress = scrapy.Field(output_processor=TakeFirst())
    inn = scrapy.Field(output_processor=TakeFirst())
    ogrn = scrapy.Field(output_processor=TakeFirst())
    kpp = scrapy.Field(output_processor=TakeFirst())
    garant = scrapy.Field(output_processor=TakeFirst())
    new_apartments = scrapy.Field(output_processor=TakeFirst())
    company_manager = scrapy.Field(output_processor=TakeFirst())
    company_phone = scrapy.Field(output_processor=TakeFirst())
    email = scrapy.Field(output_processor=TakeFirst())
    site = scrapy.Field(output_processor=TakeFirst())
    region = scrapy.Field(output_processor=TakeFirst())
    founders = scrapy.Field()
