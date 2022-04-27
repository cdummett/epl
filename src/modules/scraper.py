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


if __name__ == "__main__":
    """"""
    logging.basicConfig(level=logging.WARNING)
    scraper = FbRefScraper(level=logging.DEBUG)

