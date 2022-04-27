import logging

import tkinter as tk

from modules.scraper import FbRefScraper


class SquadAnalysisGui:
    """"""

    def __init__(self, level=logging.WARNING):
        """
        Creates an instance of the SquadAnalysisGui class.

        Function initialises an instance of the class by creating a logger matching the class name and setting the log
        level at the specified level.

        Args:
            level:
        """
        self._log = logging.getLogger("SquadAnalysisGui")
        self._log.setLevel(level=level)
        self._log.debug(msg="'__init__' method called.")

        self.scraper = FbRefScraper(level=logging.WARNING)


if __name__ == "__main__":
    """"""
    logging.basicConfig(level=logging.WARNING)
    scraper = SquadAnalysisGui(level=logging.DEBUG)
