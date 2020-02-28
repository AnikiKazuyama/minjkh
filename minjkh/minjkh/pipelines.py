# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html
import csv
import json
import os
from pathlib import Path
import shutil

from scrapy.exceptions import DropItem
from scrapy import signals
from scrapy.exporters import CsvItemExporter

my_path = os.path.abspath(os.path.dirname(__file__))


class FilePipeline(object):
    extension = 'json'
    name = ''
    suffics = ''
    path = './results'
    file_mode = 'w+'
    black_list_spiders = ()
    file = None

    def get_dir_path(self, spider):
        name = self.name if self.name else spider.name
        return os.path.join(my_path, Path(self.path) / name)

    def do_file(self, spider):
        path_to_dir = self.get_dir_path(spider)
        try:
            os.makedirs(path_to_dir, exist_ok=True)
        except:
            pass

        path_to_file = os.path.join(
            my_path, f"{path_to_dir}/{self.file_name(spider)}{self.suffics}.{self.extension}")

        self.file = open(path_to_file, self.file_mode)

    def file_name(self, spider):
        name = self.name if self.name else spider.name
        try:
            return f"{name}-{spider.id}"
        except:
            return f"{name}"

    def open_spider(self, spider):
        if (spider.name not in self.black_list_spiders):
            if (os.path.isdir(self.get_dir_path(spider)) and False):
                shutil.rmtree(self.get_dir_path(spider))

            self.do_file(spider)

    def close_spider(self, spider):
        if (spider.name not in self.black_list_spiders):
            self.file.close()


class JsonWriterPipeline(FilePipeline):
    def __init__(self):
        self.count = 0
        self.file_count = 0

        self.suffics = f"{self.file_count}"
        self.black_list_spiders = ('proxy')

    @property
    def suffics(self):
        return self._suffics

    @suffics.setter
    def suffics(self, value):
        self._suffics = f"_{value}"

    def rotate_file(self, spider):
        self.file_count = self.file_count + 1
        self.suffics = self.file_count
        self.count = 0

        super().do_file(spider)

    def process_item(self, item, spider):
        if(item and self.file):
            if (self.count >= 20000):
                self.rotate_file(spider)

            self.file.seek(0)
            file_out = self.file.read()
            file_out_decode = [] if len(
                file_out) == 0 else json.loads(file_out)
            file_out_decode.append(dict(item))

            try:
                json.dumps(file_out_decode)
                result_arr = json.dumps(file_out_decode)
            except:
                self.count = self.count + 1
                return item

            self.file.seek(0)
            self.file.truncate()
            self.file.write(result_arr)

            self.count = self.count + 1
        return item
