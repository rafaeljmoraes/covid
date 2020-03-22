# -*- coding: utf-8 -*-
"""
Created on Sat Mar 21 09:43:06 2020

@author: Erico
"""
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

from CovidDatabase import CovidDatabase


def plot_country(covid_database, country, show_from, normalize, emphasis):
    df = covid_database.get_data()
    country_df = df[df['location'] == country]
    total_cases = country_df['total_cases']
    plot = True
    if normalize:
        population = covid_database.get_country_population(country)
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

def create_plot(covid_database, minimal_cases, show_from, normalize, title=None, export_file=''):
    df = covid_database.get_data()
    
    # Create new plot
    plt.figure()

    # Get countries to show (remove World data)
    include = ['Brazil']
    countries = df['location'].drop_duplicates()
    if normalize:
        include.append('World')
    else:
        countries = countries.where(countries != 'World').dropna()

    # Plot curves
    legend_curves = []
    for country in countries:
        if country not in include:
            if plot_country(covid_database, country, show_from, normalize, country in include):
                legend_curves.append(country)
            
    # plot included countries
    for country in include:
        if plot_country(covid_database, country, 0, normalize, True):
            legend_curves.append(country)
    
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
    covid_database = CovidDatabase()
    minimal_cases = 100
    covid_database.build_days_column(minimal_cases)
    df = covid_database.get_data()
    
    create_plot(covid_database, minimal_cases, 5e-4, True, None, 'normalized.png')
    create_plot(covid_database, minimal_cases, 2.3e-4, True, None, 'normalized2.png')
    create_plot(covid_database, minimal_cases, 2000, False, None, 'absolute.png')
