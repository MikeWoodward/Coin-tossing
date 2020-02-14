#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Feb 12 07:03:32 2020

@author: mwoodward

License: MIT

"""

# %%---------------------------------------------------------------------------
# Imports
# -----------------------------------------------------------------------------
import numpy as np

from bokeh.models.widgets import Button, Div, Spinner
from bokeh.plotting import Figure
from bokeh.layouts import column, row
from bokeh.models import ColumnDataSource
from bokeh.io import curdoc


# %%---------------------------------------------------------------------------
# Module metadata
# -----------------------------------------------------------------------------
__author__ = "Mike Woodward"
__license__ = "MIT"


# %%---------------------------------------------------------------------------
# Class
# -----------------------------------------------------------------------------
class Coins():

    """Coin tossing simulator class."""

    # %%
    def __init__(self):

        title = Div(text="""<h1>Coin tossing simulation</h1>"""
                         """<p>Simulates the effects of tossing a coin """
                         """many times. Heads are scored 1 and tails 0. """
                         """The chart shows the cumlative mean, which """
                         """should go to 0.5 in 'the long run'. To use """
                         """the software, select the number of coin """
                         """tosses or press go to generate a fresh """
                         """data set.</p>""",
                    sizing_mode="""stretch_width""")

        self.tosses = 2000

        self.toss_count = Spinner(step=1,
                                  value=self.tosses,
                                  title="""Number of tosses""",
                                  sizing_mode="""stretch_width""")
        self.go = Button(label="Button",
                         button_type="""success""",
                         sizing_mode="""stretch_width""")

        chart = Figure(title='Cumulative mean of coin tosses',
                       x_axis_label='Number of tosses',
                       y_axis_label='Cumulative mean')
        self.cds = ColumnDataSource()
        self.make_means()
        chart.line(source=self.cds,
                   x='tosses',
                   y='means',
                   line_color='red',
                   line_width=4,
                   line_alpha=0.5)

        chart.title.text_font_size = '20px'
        chart.xaxis.axis_label_text_font_size = '15px'
        chart.xaxis.major_label_text_font_size = '15px'
        chart.yaxis.axis_label_text_font_size = '15px'
        chart.yaxis.major_label_text_font_size = '15px'

        title_bar = column(children=[title],
                           sizing_mode="stretch_both")
        widget_bar = column(children=[self.toss_count, self.go],
                            sizing_mode='fixed',
                            width=250,
                            height=500)
        chart_row = row(children=[widget_bar, chart],
                        sizing_mode='stretch_both')
        self.layout = column(children=[title_bar, chart_row],
                             sizing_mode='stretch_both')


    # %%
    def setup(self):
        """Setup the callbacks"""
        self.toss_count.on_change('value', self.callback_toss_count)
        self.go.on_change('clicks', self.callback_go)


    # %%
    def callback_toss_count(self, attrname, old, new):
        """Callback method for mean count"""

        self.tosses = self.toss_count.value
        self.make_means()


    # %%
    def callback_go(self, attrname, old, new):
        """Callback method for mean count"""
        self.make_means()


    # %%
    def make_means(self):
        """Create thje means be generating a random number serioes."""
        heads = np.random.randint(2, size=self.toss_count.value)
        means = np.cumsum(heads)/np.arange(1, self.toss_count.value+1)
        
        self.cds.data = {'tosses': range(1, self.tosses + 1),
                         'means': means}

# %%---------------------------------------------------------------------------
# Main
# -----------------------------------------------------------------------------

coins = Coins()
coins.setup()

curdoc().add_root(coins.layout)
curdoc().title = 'Coin toss simulator'
