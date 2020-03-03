import re
import time
import urllib.parse as urlparse


import scrapy
from scrapy.loader import ItemLoader
from minjkh.items import OurHouseItem, Founder, Beneficiar
from scrapy_splash import SplashRequest as Request
# scrapy crawl minjkh

main_script = """
    function main(splash, args)
    assert(splash:go(args.url))
    assert(splash:wait(0.8))
    return {
        html = splash:html()
    }
    end
"""

open_tab_script = """
    function main(splash, args)
    assert(splash:go(args.url))
    assert(splash:wait(0.8))
    local tab_el = splash:select(args.selector)
    tab_el:mouse_click()
    return {
        html = splash:html()
    }
    end
"""


class OurHouse(scrapy.Spider):
    def __init__(self, selectors_dict={}, **kwargs):
        self.selectors = selectors_dict
        self.set_default_selectors()
        self.start_urls = ['https://xn--80az8a.xn--d1aqf.xn--p1ai/%D1%81%D0%B5%D1%80%D0%B2%D0%B8%D1%81%D1%8B/%D0%B5%D0%B4%D0%B8%D0%BD%D1%8B%D0%B9-%D1%80%D0%B5%D0%B5%D1%81%D1%82%D1%80-%D0%B7%D0%B0%D1%81%D1%82%D1%80%D0%BE%D0%B9%D1%89%D0%B8%D0%BA%D0%BE%D0%B2?page=0&limit=100&sortName=devShortNm&sortDirection=desc']

        super().__init__(**kwargs)

    name = "our_house"

    def set_default_selectors(self):
        self.selectors.setdefault('text', 'td a::text')
        self.selectors.setdefault(
            'link', '.styles__Container-qpwb36-3.cHZRte > a::attr(href)')
        self.selectors.setdefault(
            'row', '.styles__Row-sc-13ibavg-0')
        self.selectors.setdefault(
            'company_name', '.styles__Ellipsis-sc-1fw79ul-0.cDcbYl.styles__Child-qpwb36-0.styles__Primary-qpwb36-1.daoZod::text')
        self.selectors.setdefault(
            'company_group_name', '.styles__Ellipsis-sc-1fw79ul-0.cDcbYl.styles__Child-qpwb36-0.styles__Secondary-qpwb36-2.hAkugr::text')
        self.selectors.setdefault(
            'inn', '.styles__Ellipsis-sc-1fw79ul-0.cDcbYl.styles__Child-qpwb36-0.styles__Primary-qpwb36-1.bsJNWs::text')
        self.selectors.setdefault(
            'ogrn', '.styles__Ellipsis-sc-1fw79ul-0.cDcbYl.styles__Child-qpwb36-0.styles__Secondary-qpwb36-2.dhRtZa::text')
        self.selectors.setdefault(
            'next_company_page_link', '.pagination  li.active + li>a::attr(href)')
        self.selectors.setdefault(
            'garant', '.styles__BuilderCardStatusesItem-sc-2d4k8h-0.cjUshu::text')
        self.selectors.setdefault(
            'region', '.styles__TypographyP-sc-1txyxb-4.gvsbif::text')
        self.selectors.setdefault(
            'requisits', '.styles__BuilderCardRequisites-p65t3v-0.gElznm')
        self.selectors.setdefault(
            'requisits_row', '.styles__BuilderCardRequisitesRow-p65t3v-2.hQVDsN')
        self.selectors.setdefault(
            'requisits_title', '.styles__TypographyP-sc-1txyxb-4.kBcioH')
        self.selectors.setdefault(
            'contacts', '.styles__BuilderCardContacts-erzrc1-0.kgSjnF')
        self.selectors.setdefault(
            'contacts_row', '.styles__BuilderCardContactsBlock-erzrc1-2.fDCwME')
        self.selectors.setdefault(
            'contacts_title', '.styles__TypographyP-sc-1txyxb-4.KKFVD')
        self.selectors.setdefault(
            'company_city', 'td:nth-child(3)::text')
        self.selectors.setdefault(
            'company_adress', 'td:nth-child(5)::text')
        self.selectors.setdefault(
            'company_phone', 'td:nth-child(6)::text')
        self.selectors.setdefault(
            'beneficiar_row', '.styles__BuilderCardBeneficiariesWrapper-olcucx-0.dCbnZz:nth-child(1)'
        )
        self.selectors.setdefault(
            'founder_row', '.styles__BuilderCardBeneficiariesWrapper-olcucx-0.dCbnZz:nth-child(2)'
        )
        self.selectors.setdefault(
            'man_name', '.styles__Name-olcucx-3.jwMQlP'
        )
        self.selectors.setdefault(
            'benif_cell', '.styles__Cell-sc-7809tj-0.styles__CustomCell-sc-1ds3wkf-0.havoDo'
        )
        self.selectors.setdefault(
            'bank_row', '.styles__Row-sc-13ibavg-0.lkYbwl'
        )
        self.selectors.setdefault(
            'bank_cell', '.styles__Cell-sc-7809tj-0.ibavEN'
        )

    def parse(self, response):
        rows = response.css(self.selectors.get('row'))
        for row in rows:
            company_name = row.css(self.selectors.get('company_name')).get()
            company_group_name = row.css(
                self.selectors.get('company_group_name')).get()
            inn = row.css(self.selectors.get('inn')).get()
            ogrn = row.css(self.selectors.get('ogrn')).get()
            company_link = row.css(self.selectors.get('link')).get()
            company_id = company_link.split('/')[-1]
            if (company_name == 'ООО ЯРУС'):
                yield Request(
                    url=response.urljoin(company_link),
                    callback=self.parse_company,
                    endpoint="execute",
                    args={'lua_source': main_script},
                    meta={**response.meta,
                          'company_pre_info': {
                              'company_name': company_name,
                              'company_group_name': company_group_name,
                              'inn': inn,
                              'ogrn': ogrn,
                              'company_id': company_id
                          }}
                )

        # next_page = response.css(self.selectors.get(
        #     'next_company_page_link')).get()
        # if (next_page):
        #     yield Request(
        #         url=response.urljoin(next_page),
        #         callback=self.parse,
        #         meta={**response.meta}
        #     )

    def parse_company(self, response):
        requisits_information = response.css(self.selectors.get('requisits'))
        requisits_data = self.get_data_from_block(
            requisits_information, self.selectors.get('requisits_row'), self.selectors.get('requisits_title'))

        contacts_information = response.css(self.selectors.get('contacts'))
        contacts_data = self.get_data_from_block(
            contacts_information, self.selectors.get('contacts_row'), self.selectors.get('contacts_title'))
        kpp = self.get_kpp(response)
        pre_info = response.meta.get('company_pre_info')

        loader = ItemLoader(item=OurHouseItem(), response=response)
        loader.add_value('id', pre_info.get('company_id'))
        loader.add_value('name', pre_info.get('company_name'))
        loader.add_value('company_group_name',
                         pre_info.get('company_group_name'))
        loader.add_value('inn', pre_info.get('inn'))
        loader.add_value('ogrn', pre_info.get('ogrn'))
        loader.add_value('adress', requisits_data.get('adress'))
        loader.add_value('ur_adress', requisits_data.get('ur_adress'))
        loader.add_value('kpp', kpp)
        loader.add_css('garant', self.selectors.get('garant'))
        # loader.add_value('new_apartments', )
        loader.add_value('company_manager',
                         contacts_data.get('company_manager'))
        loader.add_value('company_phone', contacts_data.get('company_phone'))
        loader.add_value('email', contacts_data.get('email'))
        loader.add_value('site', contacts_data.get('site'))
        loader.add_css('region', self.selectors.get('region'))
        # loader.add_value('founders', )

        yield loader.load_item()

    def parse_banks(self, response):
        banks_elems = response.css(self.selectors.get('bank_row'))

        for bank in banks_elems:
            name = bank.css(
                f"{self.selectors.get('bank_cell')}:nth-child(1)").get()
            raschet_schet = bank.css(
                f"{self.selectors.get('bank_cell')}:nth-child(2)").get()
            rnc = bank.css(
                f"{self.selectors.get('bank_cell')}:nth-child(3)").get()
            inn = bank.css(
                f"{self.selectors.get('bank_cell')}:nth-child(4)").get()
            ogrn = bank.css(
                f"{self.selectors.get('bank_cell')}:nth-child(5)").get()
            bik = bank.css(
                f"{self.selectors.get('bank_cell')}:nth-child(6)").get()

    def parse_benef_founder(self, response):
        founder_loader = ItemLoader(item=Founder(), response=response)
        beneficiar_loader = ItemLoader(item=Beneficiar(), response=response)

        founder_elems = response.css(self.selectors.get('founder_row'))
        beneficiar_elems = response.css(self.selectors.get('beneficiar_row'))

        for founder in founder_elems:
            name = founder.css(self.selectors.get('man_name')).get()
            inn = founder.css(
                f"{self.selectors.get('benif_cell')}:nth-child(3)").get()
            votes = founder.css(
                f"{self.selectors.get('benif_cell')}:nth-child(2)").get()
            grazhdanstvo_registration = founder.css(
                f"{self.selectors.get('benif_cell')}:nth-child(4)").get()

        for beneficiar in beneficiar_elems:
            name = beneficiar.css(self.selectors.get('man_name')).get()
            inn = beneficiar.css(
                f"{self.selectors.get('benif_cell')}:nth-child(3)").get()
            share = beneficiar.css(
                f"{self.selectors.get('benif_cell')}:nth-child(2)").get()
            grazhdanstvo_registration = beneficiar.css(
                f"{self.selectors.get('benif_cell')}:nth-child(4)").get()

    def get_data_from_block(self, block, row_selector, title_selector):
        data = {}
        rows = block.css(row_selector)
        for row in rows:
            title = row.css(f"{title_selector}::text").get()
            next_to_title = row.css(f"{title_selector} + p::text").get()
            if (title == 'Юридический адрес'):
                data['ur_adress'] = next_to_title
            elif (title == 'Фактический адрес'):
                data['adress'] = next_to_title
            elif (title == 'Руководитель компании'):
                data['company_manager'] = next_to_title
            elif (title == 'Контактный телефон'):
                data['company_phone'] = next_to_title
            elif (title == 'E-mail застройщика'):
                data['email'] = row.css(
                    f"{title_selector} + a > span::text").get()
            elif (title == 'Web-сайт застройщика'):
                data['site'] = row.css(
                    f"{title_selector} + div > a::attr(href)").get()
        return data

    def get_kpp(self, response):
        titles = response.css(self.selectors.get('requisits_title'))
        for index, title in enumerate(titles):
            title_text = title.css('::text').get()
            if (title_text == 'КПП'):
                return response.css(f"{self.selectors.get('requisits_title')} + p::text").getall()[index]
