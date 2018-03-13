# -*- coding: utf-8 -*-

from domain_checker.checker import Checker
from domain_checker.domains_downloader import get_top_domains_csv


def main():
    csv_dir = get_top_domains_csv()

    if csv_dir:
        c = Checker()
        c.run()


if __name__ == '__main__':
    main()