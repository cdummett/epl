"""
"""

import logging

import numpy as np
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

        # Initialise scraper object
        self.scraper = FbRefScraper(level=logging.DEBUG)

        # Initialise widgets
        self.root = tk.Tk()

        self.frame_mode = tk.Frame(master=self.root, relief='groove', borderwidth=2)
        self.variable_mode = tk.StringVar()
        self.variable_mode.set('squad')
        self.radio_squad = tk.Radiobutton(master=self.frame_mode,
                                          text='squad',
                                          variable=self.variable_mode,
                                          value='squad',
                                          command=self.update)
        self.radio_player = tk.Radiobutton(master=self.frame_mode,
                                           text='player',
                                           variable=self.variable_mode,
                                           value='player',
                                           command=self.update)
        self.radio_squad.grid(row=0, column=0)
        self.radio_player.grid(row=0, column=1)

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
        self.frame_mode.grid(row=0, column=0, padx=self.PAD_X, pady=self.PAD_Y, sticky='EW')
        self.x_data_control_frame.grid(row=1, column=0, padx=self.PAD_X, pady=self.PAD_Y)
        self.y_data_control_frame.grid(row=2, column=0, padx=self.PAD_X, pady=self.PAD_Y)

        # Initialise analysis figure
        self.fig = plt.figure(num=1)
        self.ax = plt.axes()
        plt.show(block=False)

        self.update()

        # Run app
        self.root.mainloop()

    def update(self, *args):
        """"""
        self._log.debug("'update' method called.")

        mode = self.variable_mode.get()

        x_df = None
        if mode == "squad":
            x_df = self.scraper.get_squad_summaries(stat=self.x_data_control_frame.stat_menu.variable.get(),
                                                    vs=self.x_data_control_frame.vs_menu.variable.get())
        if mode == "player":
            x_df = self.scraper.get_player_summaries(stat=self.x_data_control_frame.stat_menu.variable.get())
        if self.x_data_control_frame.metric_menu.values != list(x_df.columns):
            self.x_data_control_frame.metric_menu.update_values(values=list(x_df.columns))
        x = x_df[self.x_data_control_frame.metric_menu.variable.get()].dropna()
        x.replace('', np.nan, inplace=True)
        x.dropna(inplace=True)

        y_df = None
        if mode == "squad":
            y_df = self.scraper.get_squad_summaries(stat=self.y_data_control_frame.stat_menu.variable.get(),
                                                    vs=self.y_data_control_frame.vs_menu.variable.get())
        if mode == "player":
            y_df = self.scraper.get_player_summaries(stat=self.y_data_control_frame.stat_menu.variable.get())
        if self.y_data_control_frame.metric_menu.values != list(y_df.columns):
            self.y_data_control_frame.metric_menu.update_values(values=list(y_df.columns))
        y = y_df[self.y_data_control_frame.metric_menu.variable.get()]
        y.replace('', np.nan, inplace=True)
        y.dropna(inplace=True)

        if mode == "squad":
            for child in self.x_data_control_frame.vs_menu.winfo_children():
                child.configure(stat='normal')
            for child in self.y_data_control_frame.vs_menu.winfo_children():
                child.configure(stat='normal')
        if mode == "player":
            for child in self.x_data_control_frame.vs_menu.winfo_children():
                child.configure(stat='disable')
            for child in self.y_data_control_frame.vs_menu.winfo_children():
                child.configure(stat='disable')

        df = pd.merge(x, y, left_index=True, right_index=True)

        self.ax.clear()
        plt.scatter(df[df.columns[0]], df[df.columns[1]])
        if mode == "squad":
            plt.title("FbRef summary analysis - squads")
        if mode == "player":
            plt.title("FbRef summary analysis - players")
        print(vars(x))
        plt.xlabel(self.x_data_control_frame.metric_menu.variable.get())
        plt.ylabel(self.y_data_control_frame.metric_menu.variable.get())
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

        self.stat_menu = MenuFrame(master=self,
                                   level=level,
                                   values=list(FbRefScraper.SUMMARY_STAT_OPTS.keys()),
                                   callback=callback)
        self.vs_menu = MenuFrame(master=self,
                                 level=level,
                                 values=['for', 'against'],
                                 callback=callback)
        self.metric_menu = MenuFrame(master=self,
                                     level=level,
                                     values=list(["Nope", "Nope"]),
                                     callback=callback)

        self.stat_menu.grid(row=1, column=0, padx=self.PAD_X, pady=self.PAD_Y)
        self.vs_menu.grid(row=2, column=0, padx=self.PAD_X, pady=self.PAD_Y)
        self.metric_menu.grid(row=3, column=0, padx=self.PAD_X, pady=self.PAD_Y)


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
