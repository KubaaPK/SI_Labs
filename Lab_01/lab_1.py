#!/usr/bin/env python
# coding: utf-8

# In[10]:


### Obsługa APi

import pandas as pd
import numpy as np
import requests
import matplotlib.pyplot as plt
from matplotlib.dates import date2num

"""Loads currency data from NBP api
Args:
    currency (string):
    date_from (string):
    date_to (string):

Returns:
    json:
"""
def load_currency(currency, date_from, date_to):
    return requests.get(f'http://api.nbp.pl/api/exchangerates/rates/A/{currency}/{date_from}/{date_to}/').json()


"""Parses currency json to Pandas Data Frame
Args:
    currency (json):
    take (integer):
    skip (integer):

Returns:
    DataFrame:
"""
def currency_json_to_data_frame(currency, take=None, skip=None):
    ###parse string to Timestamp
    for rates in currency['rates']:
        rates['effectiveDate'] = pd.to_datetime(rates['effectiveDate'])
    data_frame = pd.DataFrame.from_dict(currency['rates'])
    data_frame['code'] = currency['code']
    take = take if take is not None else len(data_frame.index)
    skip = skip if skip is not None else 0
    return data_frame[skip:take+skip]


"""Calculate correlation between two currencies
Args:
    currency_one (DataFrame): 
    currency_two (DataFrame):

Returns:
    float:
"""
def calculate_currencies_correlation(currency_one, currency_two):
    return np.corrcoef(currency_one['mid'], currency_two['mid'])[1, 0]
    
"""Calculates values difference of given currency
Args:
    currency(DataFrame)
Returns:
    Float[]:
"""
def calculate_currency_values_difference(currency):
    difference = []
    for i in range(0, len(currency['mid']) - 1):
        difference.append((float(currency['mid'][i+1]) - float(currency['mid'][i])))
    return difference


# In[11]:


### Wykresy

"""Paints plot of currency changes
Args:
    currency (DataFrame)
Returns:
    void:
"""
def paint_currency_plot(currency):
    plot_data = currency.set_index(['effectiveDate'])['mid']
    plt.title(f'Currency change in time')
    plt.xlabel('Date')
    plt.ylabel('Currency')
    plt.plot(plot_data)


"""Colors the currency plot. The red color represents decrease in value, green one increase in value
Args: 
    currency(DataFrame)
    plot(subplot)
"""
def color_currency_plot(currency, plot):
    currency_differences = calculate_currency_values_difference(currency)
    for i in range(len(currency_differences) -1):
        if currency_differences[i] < 0:
            plot.axvspan(date2num(currency['effectiveDate'][i]), date2num(currency['effectiveDate'][i+1]), facecolor='red', alpha=0.5)
        else:
            plot.axvspan(date2num(currency['effectiveDate'][i]), date2num(currency['effectiveDate'][i+1]), facecolor='green', alpha=0.5)

def set_sub_plot_labels(plot):
    plot.set_xlabel('date')
    plot.set_ylabel('value')

"""Paints subplots of given currencies and calculate correlations between them
Args:
    currency_one (DataFrame)
    currency_two (DataFrame)
    
Returns:
    void:
"""
def paint_currencies_sub_plots(currency_one, currency_two):
    currency_one_code = currency_one['code'][0]
    currency_two_code = currency_two['code'][0]
    plot_data_one = currency_one.set_index(['effectiveDate'])['mid']
    plot_data_two = currency_two.set_index(['effectiveDate'])['mid']
    
    fig, (ax1, ax2) = plt.subplots(2)
    ax1.plot(plot_data_one)
    ax2.plot(plot_data_two)
    
    ax1.set_title(currency_one_code)
    set_sub_plot_labels(ax1)
    
    ax2.set_title(currency_two_code)
    set_sub_plot_labels(ax2)
    
    color_currency_plot(currency_one, ax1)
    color_currency_plot(currency_two, ax2)
    
    fig.suptitle(f'Correlation between {currency_one_code} - {currency_two_code}: {calculate_currencies_correlation(currency_one, currency_two)}')
    fig.subplots_adjust(hspace=0.5);
    fig.set_size_inches(20, 6)


# In[14]:


### Rezultat

currency_one = load_currency('USD', '2019-09-01', '2019-09-30')
currency_two = load_currency('MXN', '2019-09-01', '2019-09-30')
currency_one_data_frame = currency_json_to_data_frame(currency_one)
currency_two_data_frame = currency_json_to_data_frame(currency_two)

pd.plotting.register_matplotlib_converters()
paint_currencies_sub_plots(currency_one_data_frame, currency_two_data_frame)

