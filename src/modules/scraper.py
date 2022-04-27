"""
"""

import re
import logging
import requests

import pandas as pd

from bs4 import BeautifulSoup


class FbRefScraper:
    """"""

    def __init__(self, level=logging.WARNING):
        """
        Creates an instance of the FbRefScraper class.

        Function initialises an instance of the class by creating a logger matching the class name and setting the log
        level at the specified level.

        Args:
            level:
        """
        self._log = logging.getLogger("FbRefScraper")
        self._log.setLevel(level=level)
        self._log.debug(msg="'__init__' method called.")

    def _scrape_table(self, url: str, table_id: str):
        """
        Scrapes the specified table from the specified url.

        Function makes a request to the specified url, coverts the html response into a BeautifulSoup object, parses
        through each table in the soup until a match is found.

        Args:
            url:
            table_id:

        Returns:
            A BeautifulSoup object containing the html data for the specified table.

        Raises:
            ValueError: If no table with an id matching table_id can be found.

        """
        self._log.debug("'scrape_table' method called.")

        res = requests.get(url)
        comm = re.compile("<!--|-->")
        soup = BeautifulSoup(comm.sub("", res.text), 'lxml')
        all_tables = soup.find_all('table')

        for table in all_tables:
            if 'id' not in table.attrs:
                continue
            if table['id'] == table_id:
                return table

        error_msg = f"Invalid argument 'table_id'. A table with id '{table_id}' was not found in any table tag."
        raise ValueError(error_msg)

if __name__ == "__main__":
    """"""
    logging.basicConfig(level=logging.WARNING)
    scraper = FbRefScraper(level=logging.DEBUG)

