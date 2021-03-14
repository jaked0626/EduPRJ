# Output2.py
from ui_util import VerticalScrolledFrame
import tkinter as tk
from tkinter import ttk
import pandas as pd
import basic_regression as b
import ui_plot as u
import nctq
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from pandastable import Table
import numpy as np


class Output2:
    def __init__(self, master, nces, avg_nctq, outcome, policies):
        self.master = master
        self.nces = nces
        self.nctq = avg_nctq
        self.outcome = outcome
        self.policies = policies
        self.y = self.nces[self.outcome]
        self.x = self.nctq[self.policies]
        self.centered_x = nctq.center_df(self.nctq)[self.policies]
        self.frame = VerticalScrolledFrame(
            master, 
            bg="white",
            cursor="arrow",
            height= self.master.winfo_screenheight(),
            width= self.master.winfo_screenwidth()
        )
        self.title_frame()
        self.plot_reg_table()
        self.plot_scplot()
        if len(self.policies) > 1:
            self.plot_corr_df()

        self.quitButton = tk.Button(self.frame, text = 'Quit', width = 25, height=2, command = self.close_windows)
        self.quitButton.pack() # show at bottom
        self.frame.pack()
    
    def title_frame(self):
        title_frame = tk.Frame(self.frame, bg = "pink")
        title_frame.pack(expand=True, fill='x')
        exp_title = ttk.Label(title_frame, text = "Description of Output:", font = ("Ariel", "18", "bold"))
        exp_title.grid(column=0, row=0, padx = 35, pady = 25)
        intro = """
        This page shows the results of a regression between the selected variables. Below, you see: \n 
            1. A table containing the results of a simple or multilinear regression
               where the rows are each policy plus the intercept and R2, and the column
               holds the coefficients and values of the variables. \n
            2. A plot of the most powerful explanatory variable in the selected policies
               against the outcome variable. \n
            3. If mutliple variables are selected, a correlation matrix of all variables 
               in the analysis.
        """
        exp = ttk.Label(title_frame, background = "pink", borderwidth = 5, font= ('Times', '16'), text = intro, relief = tk.GROOVE)
        exp.grid(column = 0, row = 1)
        #exp.insert(tk.END, intro)
        #exp.configure(state='disabled')
        reg_title = ttk.Label(title_frame, text = "Regression Details:", font = ("Ariel", "18", "bold"))
        reg_title.grid(column=0, row=2, padx = 35, pady = 25)
        reg = tk.Text(title_frame, height = 10, bg = "white", bd = 0, relief = tk.FLAT, wrap = tk.WORD)
        reg.grid(column = 0, row = 3)
        regression = "Running regression on:"
        eq = "{} ~ {}".format(self.outcome, " + ".join(self.policies))
        reg.insert(tk.END, regression + "\n" * 2 + "           " + eq)
        reg.configure(state='disabled')

    def plot_reg_table(self):
        reg_table_frame = tk.Frame(self.frame, bg = "green")
        reg_table_frame.pack(expand=True, fill="x")
        title = ttk.Label(reg_table_frame, text = "Regression Results on \n [{}]:".format(self.outcome), font = ("Ariel", "18", "bold"))
        title.grid(column=0, row = 0, padx = 35, pady = 25)
        tableframe = tk.Frame(reg_table_frame, bg = "green")
        tableframe.grid(column=0, row=1)
        reg = b.run_regression(self.centered_x, self.y)
        reg.reset_index(level=0, inplace=True)
        table = pt = Table(tableframe, dataframe = reg, showtoolbar=False, showstatusbar=True)
        table.show()
        #table = u.dat_df(reg, self.outcome)
        #table = u.dat_df(centered_nctq[self.policies].corr(), "Correlation Matrix", "orange")
        #canvas = FigureCanvasTkAgg(table, master=reg_table_frame)
        #canvas.draw()
        #canvas.get_tk_widget().grid(column = 0, row = 1)

    def plot_scplot(self):
        best_pol, best_pol_reg = b.find_max(self.centered_x, self.y)
        reg_plot_frame = tk.Frame(self.frame, bg = "blue")
        reg_plot_frame.pack(expand=True, fill="x")
        title = ttk.Label(reg_plot_frame, text = "Plot of {} \n vs. \n{}:".format(self.outcome, best_pol), font = ("Ariel", "18", "bold"), justify=tk.CENTER)
        title.grid(column=0, row = 0, padx = 35, pady = 25)
        plotframe = tk.Frame(reg_plot_frame, bg = "blue")
        plotframe.grid(column=0, row=1)
        fig = plt.Figure(figsize=(5,4), dpi=100)
        ax = u.scplot(fig, self.x[best_pol], self.y, best_pol_reg)
        #X_plot = self.nctq[best_pol]
        #ax.plot(X_plot, best_pol_reg.loc[best_pol, "values"]*X_plot + best_pol_reg.loc["Intercept", "values"], '-')
        canvas = FigureCanvasTkAgg(fig, master=plotframe)
        canvas.draw()
        canvas.get_tk_widget().pack()
        note = tk.Text(reg_plot_frame, height = 1, bg = "white", bd = 0, relief = tk.FLAT, wrap = tk.WORD, font=("Times", "13", "italic"))
        note.tag_configure("tag_left", justify="left")
        note.insert(tk.END, "*Intercept has been recalculated to show value when all other variables are held at mean value", "tag_left")
        note.grid(column = 0, row = 2, pady = 1)

    def plot_corr_df(self):
        corr_table_frame = tk.Frame(self.frame, bg = "purple")
        corr_table_frame.pack(expand=True, fill="x")
        title = ttk.Label(corr_table_frame, text = "Correlation Matrix:", font = ("Ariel", "18", "bold"))
        title.grid(column=0, row = 0, padx = 35, pady = 25)
        tableframe = tk.Frame(corr_table_frame, bg = "purple")
        tableframe.grid(column=0, row=1)
        corr_df = pd.concat([self.y, self.x], axis = 1).corr()
        corr_df.reset_index(level=0, inplace=True)
        table2 = pt = Table(tableframe, dataframe = corr_df, showtoolbar=False, showstatusbar=True)
        table2.show()
        note = tk.Text(corr_table_frame, height = 1, bg = "white", bd = 0, relief = tk.FLAT, wrap = tk.WORD, font=("Times", "13", "italic"))
        note.tag_configure("tag_left", justify="left")
        note.insert(tk.END, "*It is advisable to separate policies that are highly correlated among one another in an OLS analysis.", "tag_left")
        note.grid(column = 0, row = 2, pady = 1)
        

    def close_windows(self):
        self.master.destroy()

def test():
    root = tk.Tk()
    nces = pd.read_csv("csv/nces_final.csv", index_col=0)
    avg_nctq = pd.read_csv("csv/avg_nctq.csv", index_col = 0)
    output = Output2(root, nces, avg_nctq, "Trend: Average Daily Attendance %", avg_nctq.columns[:3])
    root.mainloop()

test()