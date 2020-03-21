# -*- coding: utf-8 -*-
"""
Created on Sat Mar 21 09:43:06 2020

@author: Erico
"""
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

def get_country_population(country):
    url = "100005.csv"
    df = pd.read_csv(url)

    result = df[df['Location'] == country]['PopTotal']
    if result.empty:
        return 0
    else:
        return int(result)
    
    
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

def plot_country(df, country, show_from, normalize, emphasis):
    country_df = df[df['location'] == country]
    total_cases = country_df['total_cases']
    plot = True
    if normalize:
        population = get_country_population(country)
        if population > 0:
            total_cases = total_cases / population
            if total_cases.max() < show_from:
                plot = False
        else:
            plot = False
    else:
        if total_cases.max() < show_from:
            plot = False
    if country == 'Brazil':
        plot = True
        print("%s, %.2f%%" % (country, total_cases.max()))
    if plot:
        if emphasis:
            plt.plot(country_df['days'], total_cases, marker='o', markersize=12, linewidth=4)
        else:
            plt.plot(country_df['days'], total_cases)
    return plot

def create_plot(df, minimal_cases, show_from, normalize, title=None, export_file=''):
    # Create new plot
    plt.figure()

    # Get countries to show (remove World data)
    countries = df['location'].drop_duplicates()
    countries = countries.where(countries != 'World').dropna()

    # Plot curves
    legend_curves = []
    for country in countries:
        emphasis = ['Brazil']
        if plot_country(df, country, show_from, normalize, country in emphasis):
            legend_curves.append(country)
            
    # plot Brazil
    if 'Brazil' not in countries.values:
        if plot_country(df, 'Brazil', show_from, normalize, True):
            legend_curves.append('Brazil')
    
    # Add plot information
    if title:
        plt.title(title)
    else:
        if normalize:
            plt.title('Casos a partir do %dº caso\n(normalizados pela população)' % minimal_cases)
        else:
            plt.title('Casos a partir do %dº caso' % minimal_cases)
    plt.xlabel('Dias')
    plt.ylabel('Casos')
    plt.yscale("log")
    plt.legend(legend_curves)
    if export_file:
        plt.savefig(export_file)
              
if __name__ == '__main__':
    minimal_cases = 100
    show_from = 2000
    df = get_covid_data()
    df = build_days_column(df, minimal_cases)
    create_plot(df, minimal_cases, 5e-4, True, None, 'normalized.png')
    create_plot(df, minimal_cases, 2e-4, True, None, 'normalized2.png')
    create_plot(df, minimal_cases, show_from, False, None, 'absolute.png')
