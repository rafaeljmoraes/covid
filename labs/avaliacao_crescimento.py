# -*- coding: utf-8 -*-
"""
Created on Sat Mar 21 09:43:06 2020

@author: Erico
"""

import numpy as np
import matplotlib.pyplot as plt

from CovidDatabase import CovidDatabase

if __name__ == '__main__':
    covid_database = CovidDatabase()
    minimal_cases = 100
    forecast = 7 #days
    start = 5 #days
    covid_database.build_days_column(minimal_cases)
    df = covid_database.get_data()

    df['growth'] = np.power(df['total_cases'] / df['total_cases'].min(), 1 / (df['days']-1)) - 1

    brazil_df = df[df['location'] == 'Brazil']
    brazil_df = brazil_df[brazil_df['days'] >= start]
    ndays = brazil_df['days'].max()
    x = range(start, ndays + forecast + 1)
    
    p0 = []
    p1 = []
    p10 = []
    p50 = []
    p90 = []
    p99 = []
    p100 = []
    length = []
    for t in x:
        growth = df[df['days'] == t]['growth']
        p0.append(growth.min())
        p10.append(np.percentile(growth, 10))
        p50.append(np.percentile(growth, 50))
        p90.append(np.percentile(growth, 90))
        p100.append(growth.max())
        length.append(len(growth))
        
    plt.figure()
    plt.plot(x, p0, 'k--')
    plt.plot(x, p10, 'c')
    plt.plot(x, p50, 'y')
    plt.plot(x, p90, 'c')
    plt.plot(x, p100, 'k--')
    plt.plot(brazil_df['days'], brazil_df['growth'], 'ko')
    plt.xlabel('Dias')
    plt.ylabel('Crescimento')
    plt.savefig('growth_percentiles.png')
    
    plt.figure()
    plt.plot(x, length)
    plt.savefig('number_of_countries.png')

    plt.figure()
    countries = ['Iran', 'Italy', 'China', 'France', 'Germany', 'Japan', 'Australia']
    for country in countries:
        country_df = df[df['location'] == country]
        country_df = country_df[country_df['days'] <= ndays + forecast]
        country_df = country_df[country_df['days'] >= start]
        plt.plot(country_df['days'], country_df['growth'])

    plt.plot(brazil_df['days'], brazil_df['growth'], 'ko')
    plt.legend(countries + ['Brazil'])
    plt.xlabel('Dias')
    plt.ylabel('Número de países')
    plt.savefig('growth_countries.png')

    # FORECAST 1
    x = range(ndays + 1, ndays + forecast + 1)
    growth_p10 = []
    growth_p50 = []
    growth_p90 = []
    ncases_p10 = []
    ncases_p50 = []
    ncases_p90 = []
    ncases = brazil_df['total_cases'].max()
    for t in x:
        growth = df[df['days'] == t]['growth']
        aux_p10 = np.percentile(growth, 10)
        aux_p50 = np.percentile(growth, 50)
        aux_p90 = np.percentile(growth, 90)
        growth_p10.append(aux_p10)
        growth_p50.append(aux_p50)
        growth_p90.append(aux_p90)
        if t == x[0]:
            ncases_p10.append(ncases * (1 + aux_p10))
            ncases_p50.append(ncases * (1 + aux_p50))
            ncases_p90.append(ncases * (1 + aux_p90))
        else:
            ncases_p10.append(ncases_p10[-1] * (1 + aux_p10))
            ncases_p50.append(ncases_p50[-1] * (1 + aux_p50))
            ncases_p90.append(ncases_p90[-1] * (1 + aux_p90))
    plt.figure()
    plt.plot(x, growth_p10, 'r')
    plt.plot(x, growth_p50, 'g')
    plt.plot(x, growth_p90, 'b')
    plt.plot(brazil_df['days'], brazil_df['growth'], 'ko')
    plt.legend(['P10', 'P50', 'P90', 'Brazil'])
    plt.xlabel('Dias')
    plt.ylabel('Crescimento')
    plt.savefig('forecast1_growth.png')

    plt.figure()
    plt.plot(x, ncases_p10, 'r')
    plt.plot(x, ncases_p50, 'g')
    plt.plot(x, ncases_p90, 'b')
    plt.plot(brazil_df['days'], brazil_df['total_cases'], 'ko')
    plt.legend(['P10', 'P50', 'P90', 'Brazil'])
    plt.xlabel('Dias')
    plt.ylabel('Casos')
    plt.savefig('forecast1_cases.png')
