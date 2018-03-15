# -*- coding: utf-8 -*-

'''
Crawlder class
'''

# standard libraries
import re

# third party libraries
import requests

from random import choice

from .logger import logger
from .user_agent import UserAgent

class CrawlerMeta(type):
    def __new__(cls, name, bases, attrs):
        count = 0
        attrs['__CrawlFunc__'] = []
        for k, v in attrs.items():
            if k.startswith('_whois'):
                attrs['__CrawlFunc__'].append(v)
                count += 1
        attrs['__CrawlFuncCount__'] = count
        return type.__new__(cls, name, bases, attrs)


class Crawler(object, metaclass=CrawlerMeta):
    def __init__(self):
        self.success_str = 'OK'
        self.error_str = 'Error'
    
    def crawl(self, domain):
        self.__class__.crawl_func = choice(self.__CrawlFunc__)
        logger.debug('checking {} with method {}'.format(domain, self.crawl_func.__name__))
        return self.crawl_func(domain)

    def fetch_html(self, url, headers, data=None, timeout=None):
        '''download html'''
        try:
            if data:
                r = requests.post(url, headers=headers, data=data, timeout=timeout)
            else:
                r = requests.get(url, headers=headers, timeout=timeout)
            if r.status_code == 200:
                logger.debug('html downloaded')
                return r.text
            else:
                logger.debug('failed to fetch html with status code {}'.format(r.status_code))
        except Exception as e:
            logger.error('http request failed, error: {}'.format(repr(e)))

    def _whois__whois_com(self, domain):
        '''lookup whois from whois.com'''
        url = 'https://www.whois.com/whois/{}'.format(domain)

        headers = {
            'User-Agent': UserAgent().get(),
            'Referer': 'https://www.whois.com/whois/',
        }

        response = self.fetch_html(url, headers, timeout=5)
        if response:
            e_date_re = re.compile('Expiration\s+Date:\s+([\d-]*)T', re.S)
            result = e_date_re.findall(response)
            if result and result[0]:
                logger.debug('got expiry date: {}'.format(result))
                return self.success_str, result[0]
            else:
                logger.info('unable to parse date from html')

        return self.error_str, ''
    
    def _whois__chinaz_com(self, domain):
        '''lookup whois from whois.chinaz.com'''
        url = 'http://whois.chinaz.com/{}'.format(domain)

        headers = {
            'User-Agent': UserAgent().get(),
            'Referer': 'http://whois.chinaz.com',
        }

        response = self.fetch_html(url, headers, timeout=5)
        if response:
            e_date_re = re.compile(r'过期时间.*?<span>(.*?)</span>', re.S)
            expiry_date_lst = e_date_re.findall(response)
            if expiry_date_lst and expiry_date_lst[0]:
                expiry_date_chn = expiry_date_lst[0]
                logger.debug('got date string: {}'.format(expiry_date_chn))
                expiry_trans_re = re.compile('(\d+)', re.S) # get date 0000-00-00 from Chinese string
                expiry_date_grp = expiry_trans_re.findall(expiry_date_chn)
                expiry_date_str = '-'.join(expiry_date_grp)
                logger.debug('got expiry date: {}'.format(expiry_date_str))
                return self.success_str, expiry_date_str
            else:
                logger.info('unable to parse date from html')

        return self.error_str, ''
    
    def _whois__sosite_cn(self, domain):
        '''lookup whois from http://sosite.cn/'''
        url = 'http://sosite.cn/domain.php'

        headers = {
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
            'Accept-Encoding': 'gzip, deflate',
            'Accept-Language': 'en-US,en;q=0.9,zh-CN;q=0.8,zh;q=0.7',
            'Content-Type': 'application/x-www-form-urlencoded',
            'Host': 'sosite.cn',
            'Origin': 'http://sosite.cn',
            'Referer': 'http://sosite.cn/domain.php?goto=metarefresh&formaction=domain.php',
            'User-Agent': UserAgent().get(),
        }

        data = {
            'action': 'process_whois',
            'compulsory': '',
            'query': domain,
            'goRhUe86a0': 'bff57b9950',
            'formaction': 'domain.php',
            'comingfrom': 'metarefresh',
            'goRhUe86a0': '7e8744370f',
        }

        response = self.fetch_html(url, headers, data=data, timeout=5)
        if response:
            e_date_re = re.compile('Expiration\s+Date:\s+([\d-]*)T', re.S)
            result = e_date_re.findall(response)
            if result and result[0]:
                logger.debug('got expiry date: {}'.format(result))
                return self.success_str, result[0]
            else:
                logger.info('unable to parse date from html')

        return self.error_str, ''
    
    def _whois__tophostingco_com(self, domain):
        '''lookup whois from http://tophostingco.com/'''
        url = 'http://tophostingco.com/domain.php'

        headers = {
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
            'Accept-Encoding': 'gzip, deflate',
            'Accept-Language': 'en-US,en;q=0.9,zh-CN;q=0.8,zh;q=0.7',
            'Content-Type': 'application/x-www-form-urlencoded',
            'Host': 'tophostingco.com',
            'Origin': 'http://tophostingco.com',
            'Referer': 'http://tophostingco.com/domain.php?goto=metarefresh&formaction=domain.php',
            'User-Agent': UserAgent().get(),
        }

        data = {
            'action': 'process_whois',
            'compulsory': '',
            'query': domain,
            'goRhUe86a0': '0541eca88b',
            'formaction': 'domain.php',
            'comingfrom': 'metarefresh',
            'goRhUe86a0': '7179ebb93a',
        }

        response = self.fetch_html(url, headers, data=data, timeout=5)
        if response:
            e_date_re = re.compile('Expiration\s+Date:\s+([\d-]*)T', re.S)
            result = e_date_re.findall(response)
            if result and result[0]:
                logger.debug('got expiry date: {}'.format(result))
                return self.success_str, result[0]
            else:
                logger.info('unable to parse date from html')

        return self.error_str, ''

    def _whois__whois365_com(self, domain):
        '''lookup whois from https://www.whois365.com/tw/'''
        url = 'https://www.whois365.com/tw/domain/{}'.format(domain)

        headers = {
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
            'Accept-Encoding': 'gzip, deflate, br',
            'Accept-Language': 'en-US,en;q=0.9,zh-CN;q=0.8,zh;q=0.7',
            'Cache-Control': 'max-age=0',
            'Host': 'www.whois365.com',
            'Referer': 'https://www.whois365.com/tw/',
            'User-Agent': UserAgent().get(),
        }

        response = self.fetch_html(url, headers, timeout=5)
        if response:
            e_date_re = re.compile('Expiry\s+Date:\s+([\d-]*)T', re.S)
            result = e_date_re.findall(response)
            if result and result[0]:
                logger.debug('got expiry date: {}'.format(result))
                return self.success_str, result[0]
            else:
                logger.info('unable to parse date from html')

        return self.error_str, ''

    def _whois__sojson_com(self, domain):
        '''lookup whois from https://www.sojson.com/whois/'''
        url = 'https://www.sojson.com/whois/{}'.format(domain)

        headers = {
            'Referer': ':https://www.sojson.com/whois/',
            'User-Agent': UserAgent().get(),
        }

        response = self.fetch_html(url, headers, timeout=5)
        if response:
            e_date_re = re.compile(r'过期时间.*?<span>(.*?)</span>', re.S)
            expiry_date_lst = e_date_re.findall(response)
            if expiry_date_lst and expiry_date_lst[0]:
                expiry_date_chn = expiry_date_lst[0]
                logger.debug('got date string: {}'.format(expiry_date_chn))
                expiry_trans_re = re.compile('(\d+)', re.S) # get date 0000-00-00 from Chinese string
                expiry_date_grp = expiry_trans_re.findall(expiry_date_chn)
                expiry_date_str = '-'.join(expiry_date_grp)
                logger.debug('got expiry date: {}'.format(expiry_date_str))
                return self.success_str, expiry_date_str
            else:
                logger.info('unable to parse date from html')

        return self.error_str, ''

    def _whois_dnsquery_org(self, domain):
        '''lookup whois from https://dnsquery.org/'''
        url = 'https://dnsquery.org/whois/{}'.format(domain)

        headers = {
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
            'Accept-Encoding': 'gzip, deflate, br',
            'Accept-Language': 'en-US,en;q=0.9,zh-CN;q=0.8,zh;q=0.7',
            'Referer': 'https://dnsquery.org/',
            'User-Agent': UserAgent().get()
        }

        response = self.fetch_html(url, headers, timeout=5)
        if response:
            e_date_re = re.compile('Expiry\s+Date:\s+([\d/]*)T', re.S)
            result = e_date_re.findall(response)
            if result and result[0]:
                expiry_date_forward = result[0]
                logger.debug('got date string: {}'.format(expiry_date_forward))
                expiry_trans_re = re.compile('(\d+)', re.S) # get date 0000-00-00 from Chinese string
                expiry_date_grp = expiry_trans_re.findall(expiry_date_forward)
                expiry_date_str = '-'.join(expiry_date_grp)
                logger.debug('got expiry date: {}'.format(expiry_date_str))
                return self.success_str, expiry_date_str
            else:
                logger.info('unable to parse date from html')

        return self.error_str, ''