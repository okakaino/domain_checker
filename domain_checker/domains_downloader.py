# -*- coding: utf-8 -*-

import io
import os
import zipfile

import requests

from .logger import logger

def get_top_domains_csv():
    logger.debug('sending request for domain names csv file')
    url = 'http://s3.amazonaws.com/alexa-static/top-1m.csv.zip'

    try:
        r = requests.get(url)
        if r.status_code == 200:
            z = zipfile.ZipFile(io.BytesIO(r.content))
            z.extractall()
            current_dir = os.path.dirname(__file__)
            logger.debug('csv file saved to {}'.format(current_dir))
            return current_dir
        else:
            logger.debug('fail to download csv file, got status code {}'.format(r.status_code))
    except Exception as e:
        logger('failed to download csv file, error: {}'.format(repr(e)))