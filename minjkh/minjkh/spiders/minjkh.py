import re
import time
import urllib.parse as urlparse


import scrapy
from scrapy.loader import ItemLoader
from minjkh.items import MinjkhItem


class Minjkh(scrapy.Spider):
    def __init__(self, selectors_dict={}, **kwargs):
        self.selectors = selectors_dict
        self.set_default_selectors()
        self.start_urls = ['http://mingkh.ru/region/']

        super().__init__(**kwargs)

    name = "minjkh"

    def set_default_selectors(self):
        self.selectors.setdefault('text', 'td a::text')
        self.selectors.setdefault('link', 'td a::attr(href)')
        self.selectors.setdefault(
            'region_fond', 'td:nth-child(5)::text')
        self.selectors.setdefault(
            'row', '.table tbody tr')
        self.selectors.setdefault(
            'company_name', 'td:nth-child(2) > a::text')
        self.selectors.setdefault(
            'company_city', 'td:nth-child(3)::text')
        self.selectors.setdefault(
            'company_adress', 'td:nth-child(5)::text')
        self.selectors.setdefault(
            'company_phone', 'td:nth-child(6)::text')
        self.selectors.setdefault(
            'next_company_page_link', '.pagination  a[rel=next]::attr(href)')
        self.selectors.setdefault(
            'company_description', '.seo-text::text')
        self.selectors.setdefault(
            'company', '.company'
        )

    def parse(self, response):
        loader = ItemLoader(item=MinjkhItem(), response=response)
        loader.add_css('region_name', self.selectors.get('text'))
        loader.add_css('region_fond', self.selectors.get('region_fond'))

        rows = response.css(self.selectors.get('row')).getall()
        for row in rows:
            region_name = row.css(self.selectors.get('text')).get()
            region_fond = row.css(self.selectors.get('region_fond')).get()
            region_link = row.css(self.selectors.get('link')).get()
            if (region_name == "Еврейская Автономная область"):
                yield scrapy.Request(response.urljoin(region_link),
                                     callback=self.parse_region_pages,
                                     meta={'region': {'name': region_name, 'found': region_fond}})

    def parse_region_pages(self, response):
        rows = response.css(self.selectors.get('row'))
        for row in rows:
            company_name = row.css(self.selectors.get('company_name')).get()
            company_city = row.css(self.selectors.get('company_city')).get()
            company_adress = row.css(
                self.selectors.get('company_adress')).get()
            company_phone = row.css(self.selectors.get('company_phone')).get()
            company_link = row.css(self.selectors.get('link')).get()

            yield scrapy.Request(
                url=response.urljoin(company_link),
                callback=self.parse_company,
                meta={**response.meta,
                      'company_pre_info': {
                          'company_name': company_name,
                          'company_city': company_city,
                          'company_adress': company_adress,
                          'company_phone': company_phone
                      }}
            )

        next_page = response.css(self.selectors.get(
            'next_company_page_link')).get()

        if (next_page):
            yield scrapy.Request(
                url=response.urljoin(next_page),
                callback=self.parse_region_pages,
                meta={**response.meta}
            )

    def parse_company(self, response):
        loader = response.meta.get('loader')

        description = response.css(
            self.selectors.get('company_description')).get()
        company_inforamtion = response.css(self.selectors.get('company'))
        company_data = self.get_data_from_company(company_inforamtion)
        working_time = self.get_text_from_heading(response, 'Режим работы')
        pre_info = response.meta.get('company_pre_info')
        region = response.meta.get('region')

        loader = ItemLoader(item=MinjkhItem(), response=response)
        loader.add_value('company_description', description)
        loader.add_value('company_working_time', working_time)
        loader.add_value('company_name', pre_info.get('company_name'))
        loader.add_value('company_city', pre_info.get('company_city'))
        loader.add_value('company_adress', pre_info.get('company_adress'))
        loader.add_value('company_phone', pre_info.get('company_phone'))
        loader.add_value('company_manager', company_data.get('manager'))
        loader.add_value('dispetcher_phone',
                         company_data.get('dispetcher_phone'))
        loader.add_value('inn', company_data.get('inn'))
        loader.add_value('ogrn', company_data.get('ogrn'))
        loader.add_value('email', company_data.get('email'))
        loader.add_value('site', company_data.get('site'))
        loader.add_value('region_name', region.get('name'))
        loader.add_value('region_fond', region.get('found'))

        yield loader.load_item()

    def get_data_from_company(self, company):
        data = {}
        names = company.css('dt')
        for index, name in enumerate(names):

            name_text = name.css('::text').get()
            next_to_name = company.css(
                '.company dt:nth-of-type({}) + dd::text'.format(index + 1)).get()
            if (name_text == 'Руководитель'):
                data['manager'] = next_to_name
            elif (name_text == 'Диспетчерская служба'):
                data['dispetcher_phone'] = next_to_name
            elif (name_text == 'ИНН'):
                data['inn'] = next_to_name
            elif (name_text == 'ОГРН'):
                data['ogrn'] = next_to_name
            elif (name_text == 'E-mail'):
                data['email'] = next_to_name
            elif (name_text == 'Веб-сайт'):
                data['site'] = next_to_name
        return data

    def get_text_from_heading(self, response, name):
        headings = response.css('.block-heading-two')
        for heading in headings:
            heading_text = heading.css('::text').get()
            if (heading_text == name):
                return heading.css('.block-heading-two + *::text')
        return None
