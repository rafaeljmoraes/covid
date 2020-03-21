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
    df = pd.read_csv(url, sep=';')

    from_to = {}
    from_to['Austria'] = 'Áustria'
    from_to['Belgium'] = 'Bélgica'
    from_to['Brazil'] = 'Brasil'
    from_to['Denmark'] = 'Dinamarca'
    from_to['France'] = 'França'
    from_to['Germany'] = 'Alemanha'
    from_to['Iran'] = 'Irã'
    from_to['Italy'] = 'Itália'
    from_to['Japan'] = 'Japão'
    from_to['Malaysia'] = 'Malásia'
    from_to['Netherlands'] = 'Países Baixos'
    from_to['Norway'] = 'Noruega'
    from_to['South Korea'] = 'Coréia do Sul'
    from_to['Spain'] = 'Espanha'
    from_to['Sweden'] = 'Suécia'
    from_to['Switzerland'] = 'Suíça'
    from_to['United Kingdom'] = 'Reino Unido'
    from_to['United States'] = 'Estados Unidos'
    
    if country in from_to.keys():
        country = from_to[country]
    #print(df)
    result = df[df['País'] == country]['População']
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

def plot_country(df, country, normalize, emphasis):
    country_df = df[df['location'] == country]
    total_cases = country_df['total_cases']
    plot = True
    if normalize:
        population = get_country_population(country)
        if population > 0:
            total_cases = total_cases / population
        else:
            plot = False
    if plot:
        if emphasis:
            plt.plot(country_df['days'], total_cases, marker='o', markersize=12, linewidth=4)
        else:
            plt.plot(country_df['days'], total_cases)
    return plot

if __name__ == '__main__':
    minimal_cases = 100
    show_from = 2000
    normalize = True
    df = get_covid_data()
    df = build_days_column(df, minimal_cases)

    # Get countries to show (remove World data)
    country_df = df[df['total_cases'] >= show_from]
    countries = country_df['location'].drop_duplicates()
    countries = countries.where(countries != 'World').dropna()

    # Plot curves
    legend_curves = []
    for country in countries:
        emphasis = ['Brazil']
        if plot_country(df, country, normalize, country in emphasis):
            legend_curves.append(country)
            
    # plot Brazil
    if 'Brazil' not in countries.values:
        if plot_country(df, 'Brazil', normalize, True):
            legend_curves.append('Brazil')
    
    # Add plot information
    plt.title('Casos a partir do %dº caso' % minimal_cases)
    plt.xlabel('Dias')
    plt.ylabel('Casos')
    plt.yscale("log")
    plt.legend(legend_curves)
