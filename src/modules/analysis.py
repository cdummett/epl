"""
"""

import logging

import pandas as pd
import tkinter as tk

from modules.scraper import FbRefScraper

from matplotlib import pyplot as plt


class SquadAnalysisGui:
    """"""

    def __init__(self, level=logging.WARNING):
        """
        Creates an instance of the SquadAnalysisGui class.

        Function initialises an instance of the class by creating a logger matching the class name and setting the log
        level at the specified level.

        Args:
            level: specifies the level of logging messages to record
        """
        # Initialise class logger
        self._log = logging.getLogger("SquadAnalysisGui")
        self._log.setLevel(level=level)

        # Logging message for function call
        self._log.debug(msg="'__init__' method called.")

        # Initialise widgets
        self.root = tk.Tk()
        self.frame_x_data_controls = DataControlFrame(master=self.root, level=level)
        self.frame_x_data_controls.grid(row=0, column=0)
        self.frame_y_data_controls = DataControlFrame(master=self.root, level=level)
        self.frame_y_data_controls.grid(row=1, column=0)
        self.button_update = tk.Button(master=self.root, text="Update", width=40, command=self.update)
        self.button_update.grid(row=2, column=0)

        # Initialise analysis figure
        self.fig = plt.figure(num=1)
        self.ax = plt.axes()
        plt.show(block=False)

        # Run app
        self.root.mainloop()

    def update(self):
        """"""
        self._log.debug(msg="'update' method called.")
        x = self.frame_x_data_controls.df[self.frame_x_data_controls.variable_metric.get()]
        y = self.frame_y_data_controls.df[self.frame_y_data_controls.variable_metric.get()]

        df = pd.merge(x, y, left_index=True, right_index=True)

        self.ax.clear()
        plt.scatter(df[df.columns[0]], df[df.columns[1]])
        plt.show(block=False)


class DataControlFrame(tk.Frame):
    """"""

    def __init__(self, level=logging.WARNING, **kw):
        """
        Creates an instance of the DataControlFrame class.

        Function initialises an instance of the class by creating a logger matching the class name and setting the log
        level at the specified level.

        Args:
            level: specifies the level of logging messages to record

        Returns:
            None

        """
        super().__init__(**kw)

        # Initialise class logger
        self._log = logging.getLogger("DataControlFrame")
        self._log.setLevel(level=level)

        # Logging message for function call
        self._log.debug(msg="'__init__' method called.")

        # Create a scraper object for the data control frame and initialise the data
        self.scraper = FbRefScraper(level=logging.WARNING)
        self.df = self.scraper.scrape_squad_summaries(stat='stats', vs=False)

        # Initialise the values for the OptionMenu widgets
        self.stat_options = list(self.scraper.SUMMARY_STAT_OPTS.keys())
        self.metric_options = list(self.df.columns)

        # Initialise the variables for the OptionMenu widgets
        self.variable_stat = tk.StringVar()
        self.variable_stat.set(self.stat_options[0])
        self.variable_stat.trace(mode="w", callback=self.callback_optionmenu_stat)
        self.variable_metric = tk.StringVar()
        self.variable_metric.set(self.metric_options[0])

        # Initialise the OptionMenu widgets
        self.optionmenu_stat = tk.OptionMenu(self, self.variable_stat, *self.stat_options)
        self.optionmenu_stat.config(width=40)
        self.optionmenu_stat.grid(row=0, column=0)
        self.optionmenu_metric = tk.OptionMenu(self, self.variable_metric, *self.metric_options)
        self.optionmenu_metric.config(width=40)
        self.optionmenu_metric.grid(row=1, column=0)

    def callback_optionmenu_stat(self, *args):
        """
        Updates values in the metric OptionMenu widget when the selection in the stat OptionMenu widget is changed.

        Function is called when the value of variable_stat is changed by the user. Function scrapes the dataframe for
        the newly selected stat and updates the values of optionmenu_widget with the columns of the new dataframe.

        Args:
            *args: arguments required for callback

        Returns:
            None

        """

        # Function logging message
        self._log.debug(msg="'callback_optionmenu_stat' method called.")

        self.df = self.scraper.scrape_squad_summaries(stat=self.variable_stat.get(), vs=False)
        self.metric_options = list(self.df.columns)
        self.variable_metric.set(self.metric_options[0])

        self.optionmenu_metric["menu"].delete(0, "end")
        for string in self.metric_options:
            self.optionmenu_metric["menu"].add_command(label=string,
                                                       command=lambda value=string: self.variable_metric.set(value))


if __name__ == "__main__":
    """"""
    logging.basicConfig(level=logging.WARNING)
    app = SquadAnalysisGui(level=logging.DEBUG)
