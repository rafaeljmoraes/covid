# -*- coding: utf-8 -*-
"""
Created on Sat Mar 21 09:43:06 2020

@author: Erico
"""
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

def get_covid_data():
    url = "https://covid.ourworldindata.org/data/ecdc/full_data.csv"
    return pd.read_csv(url)

def build_days_column(df):
    df = df.loc[:, ['date', 'location', 'total_cases']]
    df = df[df['total_cases'] > 0]
    df['days'] = 0
    
    countries = df['location'].drop_duplicates()
    for country in countries:
        country_df = df[df['location'] == country]
        index = country_df.index
        df.loc[index, 'days'] = range(1, index.size + 1)
    return df

if __name__ == '__main__':
    df = get_covid_data()
    df = build_days_column(df)
    
    country_df = df[df['location'] == 'Brazil']
    plt.plot(country_df['days'], country_df['total_cases'])
