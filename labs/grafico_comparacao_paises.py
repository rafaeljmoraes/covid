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

def build_days_column(df, minimal_cases = 1):
    df = df.loc[:, ['date', 'location', 'total_cases']]
    df = df[df['total_cases'] >= minimal_cases]
    df['days'] = 0
    
    countries = df['location'].drop_duplicates()
    for country in countries:
        country_df = df[df['location'] == country]
        index = country_df.index
        df.loc[index, 'days'] = range(1, index.size + 1)
    return df

if __name__ == '__main__':
    minimal_cases = 100
    show_from = 2000
    df = get_covid_data()
    df = build_days_column(df, minimal_cases)

    # Get countries to show (remove World data)
    country_df = df[df['total_cases'] >= show_from]
    countries = country_df['location'].drop_duplicates()
    countries = countries.where(countries != 'World').dropna()

    # Plot curves
    for country in countries:
        country_df = df[df['location'] == country]
        plt.plot(country_df['days'], country_df['total_cases'])
        
    # plot Brazil
    if 'Brazil' not in countries:
        country_df = df[df['location'] == 'Brazil']
        plt.plot(country_df['days'], country_df['total_cases'], marker='o', markerfacecolor='blue', markersize=12, color='skyblue', linewidth=4)
    
    # Add plot information
    plt.title('Casos a partir do %dº caso' % minimal_cases)
    plt.xlabel('Dias')
    plt.ylabel('Casos')
    plt.yscale("log")
    plt.legend(countries)
