"""
"""

import logging

import numpy as np
import pandas as pd
import tkinter as tk

from modules.scraper import FbRefScraper

from matplotlib import pyplot as plt


class FbRefAnalysisGui:
    """ tkinter application for analysing summary data scraped from https://fbref.com/en/.

    Application allows user to select between data for squad and player summaries across a range of categories and
     metrics. Data is scraped, processed, and cached for quick access by an instance of the FbRefScraper.

    Attributes:
        _log: logger object for the class
        _scraper: FbRefScraper object for scraping, processing, and caching data.
        _root: tkinter top-level widget for displaying and running the application.
        _frame_table: custom tkinter Frame widget with controls for selecting whether to display squad or player data.
        _frame_data_x: custom tkinter Frame widget with controls for selecting data for x-axis.
        _frame_data_y: custom tkinter Frame widget with controls for selecting data for y_axis.
        _fig: matplotlib Figure object for containing _ax.
        _ax: matplotlib Axes object for displaying scatter plots.

    """

    # Define external padding for tk widgets
    PAD_X = 2
    PAD_Y = 2

    def __init__(self, level=logging.WARNING):
        """Creates an instance of the FbRefAnalysisGui class.

        Function initialises an instance of the class by creating a logger matching the class name and setting the log
        level at the specified level. Default and custom tkinter widgets are then initialised and packed before the
        application is run.

        Args:
            level: specifies the level of logging messages to record

        """

        # Initialise class logger
        self._log = logging.getLogger("SquadAnalysisGui")
        self._log.setLevel(level=level)

        # Logging message for function call
        self._log.debug(msg="'__init__' method called.")

        # Initialise scraper object
        self._scraper = FbRefScraper(level=logging.DEBUG)

        # Initialise and pack widgets using grid
        self._root = tk.Tk()
        self._frame_table = TableControlFrame(level=level,
                                              master=self._root,
                                              relief='groove',
                                              borderwidth=2,
                                              _callback=self._update)
        self._frame_data_x = DataControlFrame(level=level,
                                              master=self._root,
                                              relief='groove',
                                              borderwidth=2,
                                              _callback=self._update)
        self._frame_data_y = DataControlFrame(level=level,
                                              master=self._root,
                                              relief='groove',
                                              borderwidth=2,
                                              _callback=self._update)
        self._frame_table.grid(row=0, column=0, padx=self.PAD_X, pady=self.PAD_Y, sticky='EW')
        self._frame_data_x.grid(row=1, column=0, padx=self.PAD_X, pady=self.PAD_Y)
        self._frame_data_y.grid(row=2, column=0, padx=self.PAD_X, pady=self.PAD_Y)

        # Initialise analysis figure
        self._fig = plt.figure(num=1)
        self._ax = plt.axes()
        self._update()

        # Run app
        self._root.mainloop()

    def _update(self, *args):
        """Retrieves data from the cache for selected options and updates the application figure.

        Args:
            *args: required for tkinter callback to accept _update as argument.

        Returns:
            None

        """
        self._log.debug("'update' method called.")

        mode = self._frame_table.variable.get()

        x_df = None
        if mode == "squad":
            x_df = self._scraper.get_squad_summaries(stat=self._frame_data_x.stat_menu.variable.get(),
                                                     vs=self._frame_data_x.vs_menu.variable.get())
        if mode == "player":
            x_df = self._scraper.get_player_summaries(stat=self._frame_data_x.stat_menu.variable.get())
        if self._frame_data_x.metric_menu.values != list(x_df.columns):
            self._frame_data_x.metric_menu.update_values(values=list(x_df.columns))
        x = x_df[self._frame_data_x.metric_menu.variable.get()].dropna()
        x.replace('', np.nan, inplace=True)
        x.dropna(inplace=True)

        y_df = None
        if mode == "squad":
            y_df = self._scraper.get_squad_summaries(stat=self._frame_data_y.stat_menu.variable.get(),
                                                     vs=self._frame_data_y.vs_menu.variable.get())
        if mode == "player":
            y_df = self._scraper.get_player_summaries(stat=self._frame_data_y.stat_menu.variable.get())
        if self._frame_data_y.metric_menu.values != list(y_df.columns):
            self._frame_data_y.metric_menu.update_values(values=list(y_df.columns))
        y = y_df[self._frame_data_y.metric_menu.variable.get()]
        y.replace('', np.nan, inplace=True)
        y.dropna(inplace=True)

        if mode == "squad":
            for child in self._frame_data_x.vs_menu.winfo_children():
                child.configure(stat='normal')
            for child in self._frame_data_y.vs_menu.winfo_children():
                child.configure(stat='normal')
        if mode == "player":
            for child in self._frame_data_x.vs_menu.winfo_children():
                child.configure(stat='disable')
            for child in self._frame_data_y.vs_menu.winfo_children():
                child.configure(stat='disable')

        df = pd.merge(x, y, left_index=True, right_index=True)

        self._ax.clear()
        plt.scatter(df[df.columns[0]], df[df.columns[1]])
        if mode == "squad":
            plt.title("FbRef summary analysis - squads")
        if mode == "player":
            plt.title("FbRef summary analysis - players")
        plt.xlabel(self._frame_data_x.metric_menu.variable.get())
        plt.ylabel(self._frame_data_y.metric_menu.variable.get())
        plt.show(block=False)


class TableControlFrame(tk.Frame):
    """Custom tkinter Frame widget for switching between squad and player summary data.

        Application allows user to switch between visualising cached squad and player summary data using tkinter radio
        buttons. Selecting player summary data disables user from interacting with 'vs' menus.

        Attributes:
            _log: logger object for the class.
            variable: tk StringVar object for storing selected radio button value.
            radio_squad: tk Radio widget for selecting squad data.
            radio_player: tk Radio widget for selecting player data.

        """

    # Define external padding for tk widgets
    PAD_X = 1
    PAD_Y = 1

    def __init__(self, level=logging.WARNING, _callback=None, **kw):
        """Creates an instance of the DataControlFrame class.

        Function initialises an instance of the class by creating a logger matching the class name and setting the log
        level at the specified level.

        Args:
            level: specifies the level of logging messages to record
            _callback:
            **kw:

        Returns:
            None

        """
        super().__init__(**kw)

        # Initialise and pack widgets using grid
        self.variable = tk.StringVar()
        self.variable.set('squad')
        self.radio_squad = tk.Radiobutton(master=self,
                                          text='squad',
                                          variable=self.variable,
                                          value='squad',
                                          command=_callback)
        self.radio_player = tk.Radiobutton(master=self,
                                           text='player',
                                           variable=self.variable,
                                           value='player',
                                           command=_callback)
        self.radio_squad.grid(row=0, column=0, padx=self.PAD_X, pady=self.PAD_Y)
        self.radio_player.grid(row=0, column=1, padx=self.PAD_X, pady=self.PAD_Y)


class DataControlFrame(tk.Frame):
    """Custom tkinter Frame widget for selecting specific datasets and metrics from squad and player summary data.

        Application allows user to switch between FbRef datasets using the stat_menu, between 'for' or 'against' data
        using the vs_menu, and select data to visualise on an axis using the metric_menu. Controls allow user to select
        options using a drop down menu or cycle through options using buttons.

        Attributes:
            _log: logger object for the class.
            stat_menu: Custom tkinter Frame object for selecting the FbRef dataset
            vs_menu: Custom tkinter Frame object for selecting either the 'for' or 'against' dataset
            metric_menu: Custom tkinter Frame object for selecting the metric of the dataset to analyse

        """

    # Define external padding for tk widgets.
    PAD_X = 1
    PAD_Y = 1

    def __init__(self, level=logging.WARNING, _callback=None, **kw):
        """Creates an instance of the DataControlFrame class.

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

        # Initialise and pack widgets using grid
        self.stat_menu = MenuFrame(master=self,
                                   level=level,
                                   values=list(FbRefScraper.SUMMARY_STAT_OPTS.keys()),
                                   _callback=_callback)
        self.vs_menu = MenuFrame(master=self,
                                 level=level,
                                 values=['for', 'against'],
                                 _callback=_callback)
        self.metric_menu = MenuFrame(master=self,
                                     level=level,
                                     values=list(["Nope", "Nope"]),
                                     _callback=_callback)
        self.stat_menu.grid(row=1, column=0, padx=self.PAD_X, pady=self.PAD_Y)
        self.vs_menu.grid(row=2, column=0, padx=self.PAD_X, pady=self.PAD_Y)
        self.metric_menu.grid(row=3, column=0, padx=self.PAD_X, pady=self.PAD_Y)


class MenuFrame(tk.Frame):
    """Custom tkinter Frame widget for selecting a value through a menu or cycling through values with buttons.

        Subclass of the tkinter Frame class with prepacked widgets for selecting a value from a list of values. Options
        in the menu can be updated through the update_values method.

        Attributes:
            _log: logger object for the class.
            values: List of values to display in the menu
            variable: Custom tkinter StringVar for storing the currently selected value
            menu: Standard tkinter OptionMenu widget for selecting a value from values
            _button_dw: Standard tkinter Button widget for cycling through values (backwards in list)
            _button_up: Standard tkinter Button widget for cycling through values (forwards in list))

        """

    def __init__(self, level=logging.WARNING, values=None, _callback=None, **kw):
        """
        Creates an instance of the MenuFrame class.

        Function initialises an instance of the class by creating a logger matching the class name and setting the log
        level at the specified level. Tkinter widgets are then initialised and packed into the frame.

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

        # Initialise and pack widgets using grid
        self.values = values
        self.variable = tk.StringVar()
        self.variable.set(values[0])
        if _callback:
            self.variable.trace(mode="w", callback=_callback)
        self._button_bk = tk.Button(master=self, text='<-', command=self._button_bk_callback)
        self.menu = tk.OptionMenu(self, self.variable, *values)
        self.menu.config(width=40)
        self._button_fw = tk.Button(master=self, text='->', command=self._button_fw_callback)
        self._button_bk.grid(row=0, column=0)
        self.menu.grid(row=0, column=1)
        self._button_fw.grid(row=0, column=2)

    def update_values(self, values):
        """Updates the menu options with the specified values.

        Updates the values property with the give values, sets the variable to the first value in values, clears all
        values currently in the menu, and finally adds all the new values to the menu widget.

        Args:
            values: List of values to show in the tkinter menu widget.

        Returns:
            None

        """
        # Function logging message
        self._log.debug(msg="'callback_optionmenu_stat' method called.")
        # Update the menu widget with the given values
        self.values = values
        self.variable.set(self.values[0])
        self.menu["menu"].delete(0, "end")
        for string in self.values:
            self.menu["menu"].add_command(label=string,
                                          command=lambda value=string: self.variable.set(value))

    def _button_bk_callback(self):
        """Callback function for the _button_fw widget.

        Retrieves the index of the value currently set in variable associated with the tkinter menu widget, increments
        the value by +1, and sets the variable to the new value. Function has inbuilt waterfall features.

        Returns:
            None

        """
        # Logging message for function call
        self._log.debug(msg="'_button_dw_callback' method called.")
        # Increment value set in variable associated with menu widget
        index = self.values.index(self.variable.get())
        if index == 0:
            self.variable.set(self.values[-1])
        else:
            self.variable.set(self.values[index - 1])

    def _button_fw_callback(self):
        """Callback function for the _button_fw widget.

        Retrieves the index of the value currently set in variable associated with the tkinter menu widget, increments
        the value by -1, and sets the variable to the new value. Function has inbuilt waterfall features.

        Returns:
            None

        """
        # Logging message for function call
        self._log.debug(msg="'_button_fw_callback' method called.")
        # Increment value set in variable associated with menu widget
        index = self.values.index(self.variable.get())
        if index == len(self.values)-1:
            self.variable.set(self.values[0])
        else:
            self.variable.set(self.values[index + 1])


if __name__ == "__main__":
    logging.basicConfig(level=logging.WARNING)
    app = FbRefAnalysisGui(level=logging.DEBUG)
