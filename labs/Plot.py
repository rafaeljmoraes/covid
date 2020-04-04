# -*- coding: utf-8 -*-
"""
Created on Sun Mar 22 20:37:55 2020

@author: Erico
"""

import matplotlib.pyplot as plt

class Plot:
    def __init__(self, covid_database):
        self._covid_database = covid_database
        plt.figure()

    def _plot_curve(self, country, show_from, normalize, emphasis):
        df = self._covid_database.get_data()
        
        country_df = df[df['location'] == country]
        total_cases = country_df['total_cases']
        plot = True
        if normalize:
            population = self._covid_database.get_country_population(country)
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
                plt.plot(country_df['days'], total_cases, marker='o', markersize=8, linewidth=4)
            else:
                plt.plot(country_df['days'], total_cases)
        return plot

    def create_plot(self, minimal_cases, show_from, normalize, title=None, export_file=''):
        df = self._covid_database.get_data()
        
        # Get countries to show (remove World data)
        include = ['Brazil', 'China', 'United States']
        #include = ['Brazil']
        countries = df['location'].drop_duplicates()
        if normalize:
            include.append('World')
        else:
            countries = countries.where(countries != 'World').dropna()
    
        # Plot curves
        legend_curves = []
        for country in countries:
            if country not in include:
                if self._plot_curve(country, show_from, normalize, country in include):
                    legend_curves.append(country)
                
        # plot included countries
        for country in include:
            if self._plot_curve(country, 0, normalize, True):
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
        