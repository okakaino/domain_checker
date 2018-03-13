# -*- coding: utf-8 -*-

'''
Mysql database communication
'''

import MySQLdb

from .logger import logger
from .settings import HOST, PORT, USER, PASSWD, DB_NAME, TABLE_NAME


class MysqlClient():
    def __init__(self):
        conn = MySQLdb.connect(
            host=HOST,
            port=PORT,
            user=USER,
            passwd=PASSWD,
            db=DB_NAME
        )

        self.client = conn

    def save_domain(self, domain, expiry_date):
        query_formatter = ('INSERT INTO {table_name} (domain_name, exp_date) '
                        'VALUES ("{domain}", "{expiry_date}") '
                        'ON DUPLICATE KEY UPDATE exp_date="{expiry_date}";')
        query = query_formatter.format(table_name=TABLE_NAME, domain=domain, expiry_date=expiry_date)

        try:
            logger.debug('saving to db, domain is {}, expiry date is {}'.format(domain, expiry_date))
            self.client.cursor().execute(query)
            self.client.commit()
        except Exception as e:
            logger.debug('failed to save info into db, error: {}'.format(repr(e)))
            self.client.rollback()
    
    def close(self):
        self.client.close()