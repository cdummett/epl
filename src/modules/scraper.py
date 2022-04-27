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

    def scrape_squad_codes(self):
        """
        Scrapes a dictionary mapping squad names to FbRef squad codes.

        Function makes a request to the url "https://fbref.com/en/comps/9/stats/Premier-League-Stats" and processes the
        "Squad Standard Stats" table into a dictionary with squad names as keys and squad codes as values. Squad codes
        can be used to access squad stat pages (e.g. https://fbref.com/en/squads/18bb7c10/Arsenal-Stats).

        Returns:
            A dictionary mapping squad names to FbRef squad codes.
        """
        # Logging message for function call
        self._log.debug("'scrape_squad_codes' method called.")

        # Define the url to request from and the html table_id to process, then scrape the table
        url = "https://fbref.com/en/comps/9/stats/Premier-League-Stats"
        table_id = "stats_squads_standard_for"
        table = self._scrape_table(url=url, table_id=table_id)

        # Extract the codes from the hyperlinks in the table.
        squad_codes = dict()
        for tr in table.find_all('tr'):
            th = tr.find('th')
            if (th['class'] == ['left']) or (th['class'] == ['right']):
                a = tr.find_all('a')[0]
                squad_codes[th.text] = a['href'].split('/')[3]

        # Return a dictionary
        return squad_codes

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


    def _process_table(self, table, index: str = None, include_row_header: bool = False):
        """"""
        self._log.debug("'_process_data' method called.")

        data_dict = dict()
        for tr in table.find_all('tr'):
            th = tr.find('th')
            if (th['class'] == ['left']) or (th['class'] == ['right']):
                if include_row_header:
                    data_dict.setdefault(th['data-stat'], []).append(th.text)
                for td in tr.find_all('td'):
                    try:
                        data_dict.setdefault(td['data-stat'], []).append(float(td.text))
                    except ValueError:
                        data_dict.setdefault(td['data-stat'], []).append(td.text)

        if not isinstance(index, type(None)):
            return pd.DataFrame(data=data_dict, index=data_dict[index]).drop(labels=[index], axis=1)
        else:
            return pd.DataFrame(data=data_dict)


if __name__ == "__main__":
    """"""
    logging.basicConfig(level=logging.WARNING)
    scraper = FbRefScraper(level=logging.DEBUG)

