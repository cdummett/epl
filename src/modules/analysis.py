"""
"""

import logging

import pandas as pd
import tkinter as tk

from modules.scraper import FbRefScraper

from matplotlib import pyplot as plt


class SquadAnalysisGui:
    """"""

    PAD_X = 2
    PAD_Y = 2

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
        self.x_data_control_frame = DataControlFrame(level=level,
                                                     master=self.root,
                                                     relief='groove',
                                                     borderwidth=2,
                                                     callback=self.update)

        self.y_data_control_frame = DataControlFrame(level=level,
                                                     master=self.root,
                                                     relief='groove',
                                                     borderwidth=2,
                                                     callback=self.update)

        # Pack data control frame widgets
        self.x_data_control_frame.grid(row=0, column=0, padx=self.PAD_X, pady=self.PAD_Y)
        self.y_data_control_frame.grid(row=1, column=0, padx=self.PAD_X, pady=self.PAD_Y)

        # Initialise analysis figure
        self.fig = plt.figure(num=1)
        self.ax = plt.axes()
        plt.show(block=False)

        # Run app
        self.root.mainloop()

    def update(self, *args):
        """"""
        self._log.debug(msg="'update' method called.")
        x = self.x_data_control_frame.df[self.x_data_control_frame.metric_menu.variable.get()]
        y = self.y_data_control_frame.df[self.y_data_control_frame.metric_menu.variable.get()]

        df = pd.merge(x, y, left_index=True, right_index=True)

        self.ax.clear()
        plt.scatter(df[df.columns[0]], df[df.columns[1]])
        plt.show(block=False)


class DataControlFrame(tk.Frame):
    """"""

    PAD_X = 1
    PAD_Y = 1

    def __init__(self, level=logging.WARNING, callback=None, **kw):
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
        self.df = self.scraper.scrape_squad_summaries(stat='stats', vs='for')

        #
        self.stat_menu = MenuFrame(master=self,
                                   level=level,
                                   values=list(self.scraper.SUMMARY_STAT_OPTS.keys()),
                                   callback=self.update_metric_menu)
        self.vs_menu = MenuFrame(master=self,
                                 level=level,
                                 values=['for', 'against'],
                                 callback=self.update_metric_menu)
        self.metric_menu = MenuFrame(master=self,
                                     level=level,
                                     values=list(self.df.columns),
                                     callback=callback)

        self.stat_menu.grid(row=0, column=0, padx=self.PAD_X, pady=self.PAD_Y)
        self.vs_menu.grid(row=1, column=0, padx=self.PAD_X, pady=self.PAD_Y)
        self.metric_menu.grid(row=2, column=0, padx=self.PAD_X, pady=self.PAD_Y)

    def update_metric_menu(self, *args):
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

        stat = self.stat_menu.variable.get()
        vs = self.vs_menu.variable.get()

        self.df = self.scraper.scrape_squad_summaries(stat=stat, vs=vs)
        self.metric_menu.update_values(values=list(self.df.columns))


class MenuFrame(tk.Frame):

    def __init__(self, level=logging.WARNING, values=None, callback=None, **kw):
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
        if values is None:
            values = ['No options']
        self._log = logging.getLogger("DataControlFrame")
        self._log.setLevel(level=level)

        # Logging message for function call
        self._log.debug(msg="'__init__' method called.")

        self.values = values

        self.variable = tk.StringVar()
        self.variable.set(values[0])
        if callback:
            self.variable.trace(mode="w", callback=callback)

        self.button_dw = tk.Button(master=self, text='<-', command=self._button_dw)
        self.menu = tk.OptionMenu(self, self.variable, *values)
        self.menu.config(width=40)
        self.button_up = tk.Button(master=self, text='->', command=self._button_up)

        self.button_dw.grid(row=0, column=0)
        self.menu.grid(row=0, column=1)
        self.button_up.grid(row=0, column=2)

    def update_values(self, values):
        """"""
        # Function logging message
        self._log.debug(msg="'callback_optionmenu_stat' method called.")
        self.values = values
        self.variable.set(self.values[0])
        self.menu["menu"].delete(0, "end")
        for string in self.values:
            self.menu["menu"].add_command(label=string,
                                          command=lambda value=string: self.variable.set(value))

    def _button_dw(self):
        """"""
        # Logging message for function call
        self._log.debug(msg="'button_up' method called.")
        index = self.values.index(self.variable.get())
        if index == 0:
            self.variable.set(self.values[-1])
        else:
            self.variable.set(self.values[index - 1])

    def _button_up(self):
        """"""
        # Logging message for function call
        self._log.debug(msg="'button_up' method called.")
        index = self.values.index(self.variable.get())
        if index == len(self.values)-1:
            self.variable.set(self.values[0])
        else:
            self.variable.set(self.values[index + 1])


if __name__ == "__main__":
    """"""
    logging.basicConfig(level=logging.WARNING)
    app = SquadAnalysisGui(level=logging.DEBUG)
