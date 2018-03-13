# -*- coding: utf-8 -*-

import csv
import os

from .crawler import Crawler
from .db import MysqlClient
from .logger import logger

from .settings import MAX_RETRY

class Checker(object):
    def __init__(self):
        self.crawler = Crawler()
        self.client = MysqlClient()

    def run(self):
        root_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        unzipped_filename = os.path.join(root_dir, 'top-1m.csv')

        with open(unzipped_filename, 'r') as f:
            reader = csv.reader(f)
            for count, row in enumerate(reader, 1):
                result = ''
                logger.debug('checking the {} - th row'.format(count))
                domain = row[1]
                for _ in range(MAX_RETRY):
                    msg, result = self.crawler.crawl(domain)
                    if result:
                        break
                
                self.client.save_domain(domain, result)
    
    def __del__(self):
        self.client.close()
