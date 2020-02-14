#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Feb 11 22:17:12 2020

@author: mikewoodward
"""

import pandas as pd
from bokeh.plotting import figure, show
from bokeh.models.widgets import Div
from bokeh.layouts import column, row


# %%---------------------------------------------------------------------------
# Functions
# -----------------------------------------------------------------------------
def get_berkeley_data():
    
    """Get the Berkeley data and clean it up. This could probably be
    done in fewer lines of Pandas, but I don't have time to build a 
    more compact solution."""
    
    berk = pd.read_excel("40000tosses.xlsx", sheet_name='Sheet2')
    
    # Get Janet's tosses - looks like they recorded heads only
    berk_janet = berk[['Toss #', 'End: H']].copy()
    berk_janet['End: H'] = berk_janet['End: H'].fillna(0)
    berk_janet['Toss #'] = pd.to_numeric(berk_janet['Toss #'],
                                         downcast='integer', 
                                         errors='coerce')
    berk_janet = berk_janet[~berk_janet['Toss #'].isna()]
    berk_janet['Toss'] = range(1, berk_janet.shape[0] + 1)    
    berk_janet['End: H'] = pd.to_numeric(berk_janet['End: H'],
                                         downcast='integer', 
                                         errors='coerce')       
    berk_janet['mean'] = berk_janet['End: H'].expanding().mean()
    
    # Get Priscillas's tosses - looks like they recorded tails only
    berk_priscilla = berk[['Toss #.1', 'End: T']].copy()
    berk_priscilla['End: T'] = berk_priscilla['End: T'].fillna(0) 
    berk_priscilla['Toss #.1'] = pd.to_numeric(berk_priscilla['Toss #.1'],
                                               downcast='integer', 
                                               errors='coerce')
    berk_priscilla = berk_priscilla[~berk_priscilla['Toss #.1'].isna()]
    berk_priscilla['Toss'] = range(1, berk_priscilla.shape[0] + 1)   
    berk_priscilla['End: T'] = pd.to_numeric(berk_priscilla['End: T'],
                                             downcast='integer', 
                                             errors='coerce') 
    berk_priscilla['End: H'] = 1 - berk_priscilla['End: T'] 
    berk_priscilla['mean'] = berk_priscilla['End: H'].expanding().mean()  
    
    
    return berk_janet, berk_priscilla

# %%
def get_chart(df, title, color):
    
    """Build and retrieves the chart."""
    
    chart = figure(title=title)
    
    chart.line(x=df['Toss'],
               y=df['mean'],
               line_color=color,
               line_width=4)
    
    chart.xaxis.axis_label = 'Toss'
    chart.yaxis.axis_label = 'Mean'
    
    chart.title.text_font_size = "20px"
    chart.xaxis.axis_label_text_font_size = "15px"
    chart.xaxis.major_label_text_font_size = "12px"
    chart.yaxis.axis_label_text_font_size = "15px"
    chart.yaxis.major_label_text_font_size = "12px"   
    
    return chart

# %%
if __name__ == "__main__":

    title = Div(text="""<h1>University of California, Berkeley """
                     """coin tossing data</H1>""")    
    janet, priscilla = get_berkeley_data()    
    janet_chart = get_chart(janet, "Janet's coin tosses", "red")
    priscilla_chart = get_chart(priscilla, "Priscilla's coin tosses", "blue")
    
    layout = column(title, 
                    row(janet_chart, priscilla_chart))
    
    show(layout)
    