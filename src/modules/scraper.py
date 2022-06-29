"""
"""

import re
import logging
import requests

import pandas as pd

from bs4 import BeautifulSoup


class FbRefScraper:
    """"""

    SUMMARY_STAT_OPTS = {'stats': 'standard',
                         'keepers': 'keeper',
                         'keeprsadv': 'keeper_adv',
                         'shooting': 'shooting',
                         'passing': 'passing',
                         'passing_types': 'passing_types',
                         'gca': 'gca',
                         'defense': 'defense',
                         'possession': 'possession',
                         'playingtime': 'playing_time',
                         'misc': 'misc'}

    def __init__(self, level=logging.WARNING):
        """Creates an instance of the FbRefScraper class.

        Function initialises an instance of the class by creating a logger matching the class name and setting the log
        level at the specified level.

        Args:
            level:
        """
        self._log = logging.getLogger("FbRefScraper")
        self._log.setLevel(level=level)
        self._log.debug(msg="'__init__' method called.")

        # Initialise dataframe dictionaries
        self._squad_summaries = dict()
        self._player_summaries = dict()

    def scrape_squad_codes(self):
        """Scrapes a dictionary mapping squad names to FbRef squad codes.

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

    def scrape_player_codes(self):
        """Scrapes a dictionary mapping player names to FbRef player codes.

        Function makes a request to the url "https://fbref.com/en/comps/9/stats/Premier-League-Stats" and processes the
        "Player Standard Stats" table into a dictionary with player names as keys and player codes as values. Player
        codes can be used to access player stat pages (e.g. https://fbref.com/en/players/774cf58b/Max-Aarons).

        Returns:
            A dictionary mapping squad names to FbRef player codes.
        """
        # Logging message for function call
        self._log.debug("'scrape_player_codes' method called.")

        # Define the url to request from and the html table_id to process, then scrape the table
        url = "https://fbref.com/en/comps/9/stats/Premier-League-Stats"
        table_id = "stats_standard"
        table = self._scrape_table(url=url, table_id=table_id)

        # Extract the codes from the hyperlinks in the table.
        player_codes = dict()
        for tr in table.find_all('tr'):
            th = tr.find('th')
            if (th['class'] == ['left']) or (th['class'] == ['right']):
                td = tr.find_all('td')[0]
                a = tr.find_all('a')[0]
                player_codes[td.text] = a['href'].split('/')[3]

        # Return a dictionary
        return player_codes

    def get_squad_summaries(self, stat: str, vs: str):
        """Recalls a squad summaries dataframe for the specified arguments.

        Function attempts to recall a previously scraped and stored squad summaries dataframe from the objects memory.
        If the dataframe for the specified arguments does not exist, the function instead scrapes the dataframe, stores
        it in the objects memory, and then returns the dataframe.

        Args:
            stat:
            vs:

        Returns:
            A pandas dataframe of squad summary information.

        """
        # Logging message for function call
        self._log.debug("'get_squad_summaries' method called.")

        if stat not in self._squad_summaries:
            self._squad_summaries[stat] = dict()
        if vs not in self._squad_summaries[stat]:
            self._squad_summaries[stat][vs] = self.scrape_squad_summaries(stat=stat, vs=vs)

        return self._squad_summaries[stat][vs]

    def get_player_summaries(self, stat: str):
        """Recalls a player summaries dataframe for the specified arguments.

        Function attempts to recall a previously scraped and stored player summaries dataframe from the objects memory.
        If the dataframe for the specified arguments does not exist, the function instead scrapes the dataframe, stores
        it in the objects memory, and then returns the dataframe.

        Args:
            stat:

        Returns:
            A pandas dataframe of player summary information.

        """
        # Logging message for function call
        self._log.debug("'get_squad_summaries' method called.")

        if stat not in self._player_summaries:
            self._player_summaries[stat] = self.scrape_player_summaries(stat=stat)

        return self._player_summaries[stat]

    def scrape_squad_summaries(self, stat: str = 'stats', vs: str = 'for'):
        """Scrapes a dataframe summarising each squads performance metrics for the specified category.

        Function makes a request to a url (e.g. "https://fbref.com/en/comps/9/stats/Premier-League-Stats") which
        contains the squad summaries data for the specified stat category (e.g. 'shooting'). The table containing either
        the 'for' or 'against' data is then scraped and processed into a dataframe.

        Args:
            stat: specifies the category of performance metrics to scrape.
            vs: specifies whether to scrape the 'for' or 'against' table.

        Returns:
            A pandas dataframe with squad names as the index and performance metrics as the columns.

        """
        # Logging message for function call
        self._log.debug("'_scrape_squad_summaries' method called.")

        # Define the url to request from and the html table_id to process, then scrape the table
        url = f"https://fbref.com/en/comps/9/{stat}/Premier-League-Stats"
        table_id = f"stats_squads_{self.SUMMARY_STAT_OPTS[stat]}_{vs}"

        table = self._scrape_table(url=url, table_id=table_id)
        df = self._process_table(table=table, index='squad', include_row_header=True)

        new_index = {}
        if vs == 'against':
            for label in df.index:
                new_index[label] = label[3:]
        df.rename(index=new_index, inplace=True)

        # Return a dataframe
        return df

    def scrape_player_summaries(self, stat: str = 'stats'):
        """Scrapes a dataframe summarising each players performance metrics for the specified category.

        Function makes a request to a url (e.g. "https://fbref.com/en/comps/9/stats/Premier-League-Stats") which
        contains the player summaries data for the specified stat category (e.g. 'shooting').

        Args:
            stat: specifies the category of performance metrics to scrape.

        Returns:
            A pandas dataframe with player names as the index and performance metrics as the columns.

        """
        # Logging message for function call
        self._log.debug("'_scrape_squad_summaries' method called.")

        # Define the url to request from and the html table_id to process, then scrape the table
        url = f"https://fbref.com/en/comps/9/{stat}/Premier-League-Stats"
        table_id = f"stats_{self.SUMMARY_STAT_OPTS[stat]}"

        table = self._scrape_table(url=url, table_id=table_id)
        df = self._process_table(table=table, index='player', include_row_header=False)

        # Return a dataframe
        return df

    def _scrape_table(self, url: str, table_id: str):
        """Scrapes the specified table from the specified url.

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

    def _process_table(self, table, index: str = None, include_row_header: bool = False) -> pd.DataFrame:
        """Process a html table tag into a pandas dataframe object.

        Function loops through all table rows in a table and then all table data in a table row, inserting the datapoint
        into a data dictionary. The dictionary is converted into a pandas dataframe and returned.

        Args:
            table ():
            index (str):
            include_row_header (bool):

        Returns:
            pd.DataFrame:
        """
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

