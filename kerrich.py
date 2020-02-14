#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Feb 10 20:32:06 2020

@author: mikewoodward
"""

# %%---------------------------------------------------------------------------
# Module metadata
# -----------------------------------------------------------------------------
__author__ = "Mike Woodward"
__license__ = "MIT"


# %%---------------------------------------------------------------------------
# Model
# -----------------------------------------------------------------------------
import math
import pandas as pd
from bokeh.plotting import ColumnDataSource, figure, show, output_file
from bokeh.models.widgets import DataTable, Div, TableColumn
from bokeh.layouts import column, row

# %%---------------------------------------------------------------------------
# Functions
# -----------------------------------------------------------------------------
def get_kerrich_data():
    kerrich_str = ("""00011101001111101000110101111000100111001000001110"""
                   """00101010100100001001100010000111010100010000101101"""
                   """01110100001101001010000011111011111001101100101011"""
                   """01010000011000111001111101101010110100110110110110"""
                   """01111100001110110001010010000010100111111011101011"""
                   """10001100011000110001100110100100001000011101111000"""
                   """11111110000000001101011010011111011110010010101100"""
                   """11101101110010000010001100101100111110100111100010"""
                   """00001001101011101010110011111011001000001101011111"""
                   """11010001111110010111111001110011111111010000100000"""
                   """00001111100101010111100001110111001000110100001111"""
                   """11000101001111111101101110110111011010010110110011"""
                   """01010011011111110010111000111101111111000001001001"""
                   """01001110111011011011111100000101010101010101001001"""
                   """11101101110011100000001001101010011001000100001100"""
                   """10111100010011010110110111001101001010100000010000"""
                   """00001011001101011011111000101100101000011100110011"""
                   """11100101011010000110001001100010010001100100001001"""
                   """01000011100000011101101111001110011010101101001011"""
                   """01000001110110100010001110010011100001010000000010"""
                   """10010001011000010010100011111101101111010101010000"""
                   """01100010100000100000000010000001100100011011101010"""
                   """11011000110111010110010010111000101101101010110110"""
                   """00001011011101010101000011100111000110100111011101"""
                   """10001101110000010011110001110100001010000111110100"""
                   """00111111111111010101001001100010111100101010001111"""
                   """11000110101010011010010111110000111011110110011001"""
                   """11111010000011101010111101101011100001000101101001"""
                   """10011010000101111101111010110011011110000010110010"""
                   """00110110101111101011100101001101100100011000011000"""
                   """01010011000110100111010000011001100011101011100001"""
                   """11010111011110101101101111001111011100011011010000"""
                   """01011110100111011001001110001111011000011110011111"""
                   """01101011101110011011100011001111001011101010010010"""
                   """10100011010111011000111110000011000000010011101011"""
                   """10001011101000101111110111000001111111011000000010"""
                   """10111111011100010000110000110001111101001110110000"""
                   """00001111011100011101010001011000110111010001110111"""
                   """10000010000110100000101000010101000101100010111100"""
                   """00101110010111010010110010110100011000001110000111""")
    
    # Prepare
    kerrich_int = [0]*len(kerrich_str)
    for i, char in enumerate(kerrich_str):
        if char == '1':
            kerrich_int[i] = 1
            
    return kerrich_int

def get_kerrich_chart(kerrich):
    
    chart = figure(title="Kerrich's coin tossing means")
    
    chart.line(x=kerrich_df['x'],
               y=kerrich_df['mean'],
               line_color='red',
               line_width=4)
    
    chart.xaxis.axis_label = 'Toss'
    chart.yaxis.axis_label = 'Mean'
    
    chart.title.text_font_size = "20px"
    chart.xaxis.axis_label_text_font_size = "15px"
    chart.xaxis.major_label_text_font_size = "12px"
    chart.yaxis.axis_label_text_font_size = "15px"
    chart.yaxis.major_label_text_font_size = "12px"   
    
    return chart

def get_kerrich_summary():

    summary = [{'No tosses':    10, 'Heads' :    4},
               {'No tosses':    20, 'Heads' :   10},
               {'No tosses':    30, 'Heads' :   17},
               {'No tosses':    40, 'Heads' :   21},
               {'No tosses':    50, 'Heads' :   25},
               {'No tosses':    60, 'Heads' :   29},
               {'No tosses':    70, 'Heads' :   32},
               {'No tosses':    80, 'Heads' :   35},
               {'No tosses':    90, 'Heads' :   40},
               {'No tosses':   100, 'Heads' :   44},
               {'No tosses':   200, 'Heads' :   98},
               {'No tosses':   300, 'Heads' :  146},
               {'No tosses':   400, 'Heads' :  199},
               {'No tosses':   500, 'Heads' :  255},
               {'No tosses':   600, 'Heads' :  312},
               {'No tosses':   700, 'Heads' :  368},
               {'No tosses':   800, 'Heads' :  413},
               {'No tosses':   900, 'Heads' :  458},
               {'No tosses':  1090, 'Heads' :  502},
               {'No tosses':  2000, 'Heads' : 1013},
               {'No tosses':  3000, 'Heads' : 1510},
               {'No tosses':  4000, 'Heads' : 2029},
               {'No tosses':  5000, 'Heads' : 2533},
               {'No tosses':  6000, 'Heads' : 3009},
               {'No tosses':  7000, 'Heads' : 3516},
               {'No tosses':  8000, 'Heads' : 4034},
               {'No tosses':  9000, 'Heads' : 4538},
               {'No tosses': 10000, 'Heads' : 5067},
               ]  
    
    summary_df = pd.DataFrame(summary)
    summary_df['Mean'] = summary_df['Heads']/summary_df['No tosses']

    summary_df['CI'] = \
        (summary_df['Mean']*(1 - summary_df['Mean']))/summary_df['No tosses']
    summary_df['CI'] = 1.96*(summary_df['CI']**(1/2))

    return summary_df

# %%
if __name__ == "__main__":

    # Title
    title = Div(text="<H1>Kerrich's coin tossing data</H1>")
   
    # Kerrich 2,000 coin toss data 
    chart_explanation = Div(
        text="<p>The chart shows the expanding, "
             "or cumulative mean for the first 2,000 of "
             "Kerrich's coin tosses.</p>")
    
    kerrich_int = get_kerrich_data()
    kerrich_df = pd.DataFrame({'x': range(1, len(kerrich_int) + 1),
                               'k': kerrich_int})
    kerrich_df['mean'] = kerrich_df['k'].expanding().mean()
        
    chart = get_kerrich_chart(kerrich_df)
    
    # Kerrich 10,000 summary data
    table_explanation = Div(
        text="<p>The table shows the summary Kerrich data out to 10,000 "
             "tosses. </p>")    

    kerrich_summary = get_kerrich_summary()    
    data = dict(toss=kerrich_summary['No tosses'],
                mean=kerrich_summary['Mean'],
                ci=kerrich_summary['CI'])  
    source = ColumnDataSource(data)  
    columns = [TableColumn(field="toss", title="No tosses"),
               TableColumn(field="mean", title="Mean"),
               TableColumn(field='ci', title='Confidence interval (±)')]  
    data_table = DataTable(source=source, 
                           columns=columns)
    
    # Layout
    layout = column(title, 
                    row(column(chart_explanation, chart), 
                        column(table_explanation, data_table)))
    
    show(layout)
