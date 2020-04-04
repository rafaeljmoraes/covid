# -*- coding: utf-8 -*-
"""
Created on Sat Mar 21 09:43:06 2020

@author: Erico
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

from CovidDatabase import CovidDatabase


def build_growth_column(df):
    #df['growth'] = np.power(df['total_cases'] / df['total_cases'].min(), 1 / (df['days']-1)) - 1
    window = 7
    right_window = window // 2
    left_window = window - right_window
    df['growth'] = np.power(df['total_cases'].shift(-right_window) / df['total_cases'].shift(left_window), 1 / window) - 1
    df.loc[ (df['days'].shift(-right_window) - df['days'].shift(left_window)) != window , 'growth'] = np.nan

    # Postergação das curvas mantendo o último crescimento
    countries = df['location'].drop_duplicates()
    for country in countries:
        country_df = df[df['location'] == country].dropna()
        if not country_df.empty:
            last_growth = country_df['growth'].values[-1]
            last_days = country_df['days'].values[-1]
            df.loc[(df['days'] > last_days) & (df['location'] == country), 'growth'] = last_growth
    return df

    
def get_forecast(df, start, ndays, forecast, countries = [], country_groups = []):
    x = range(start, ndays + forecast + 1)

    # Cria cenarios P10, P50 e P90
    forecast_columns = ['Dias', 'Cenario', 'Taxa_crescimento']
    df_forecast = pd.DataFrame(columns=forecast_columns)
    data = []
    for t in x:
        growth = df[df['days'] == t]['growth'].dropna()
        data.append([t, 'P10', np.percentile(growth, 10)])
        data.append([t, 'P50', np.percentile(growth, 50)])
        data.append([t, 'P90', np.percentile(growth, 90)])
    df_forecast = df_forecast.append(pd.DataFrame(data, columns=forecast_columns))

    # Cria cenarios dos países
    for country in countries:
        country_df = df[df['location'] == country]
        country_df = country_df[country_df['days'] <= ndays + forecast]
        country_df = country_df[country_df['days'] >= start]
        df_forecast = df_forecast.append(pd.DataFrame({'Dias': country_df['days'],
                                                       'Cenario': country,
                                                       'Taxa_crescimento': country_df['growth']}))

    return df_forecast
        

def plot_growth(df, scenario_list, max_days):
    plt.figure()
    for scenario in scenario_list:
        scenario_df = df[df['Cenario'] == scenario]
        scenario_df = scenario_df[scenario_df['Dias'] <= max_days]
        plt.plot(scenario_df['Dias'], scenario_df['Taxa_crescimento'])
    plt.legend(scenario_list)


def plot_brazil_forecast(df, brazil_df, scenario_list, max_days):
    plt.figure()
    ncases = brazil_df['total_cases'].max()
    ndays = brazil_df['days'].max()
    for scenario in scenario_list:
        scenario_df = df[df['Cenario'] == scenario]
        days = scenario_df['Dias'].to_numpy()
        growth = scenario_df['Taxa_crescimento'].to_numpy()
        x = []
        y = []
        for i in range(len(days)):
            if days[i] <= ndays or days[i] > max_days:
                pass
            elif days[i] == ndays + 1:
                x.append(days[i])
                y.append(ncases * (1 + growth[i]))
            else:
                x.append(days[i])
                y.append(y[-1] * (1 + growth[i]))
        plt.plot(x, y)
    plt.plot(brazil_df['days'], brazil_df['total_cases'], 'ko')
    plt.legend(scenario_list + ['Brazil'])
    plt.xlabel('Dias')
    plt.ylabel('Casos')
    
if __name__ == '__main__':
    covid_database = CovidDatabase()
    minimal_cases = 100
    forecast = 30 #days
    plot_forecast = 14
    start = 5 #days
    covid_database.build_days_column(minimal_cases)
    df = covid_database.get_data()
    df = build_growth_column(df)


    brazil_df = df[df['location'] == 'Brazil']
    brazil_df = brazil_df[brazil_df['days'] >= start]
    ndays = brazil_df['days'].max()
    max_days = ndays + plot_forecast

    countries = ['Iran', 'Italy', 'China', 'France', 'Germany', 'Japan', 
                 'Australia', 'Spain', 'United States', 'Austria', 'Belgium', 
                 'Netherlands', 'South Korea', 'Switzerland', 'United Kingdom',
                 'Canada', 'Hong Kong']
    df_forecast = get_forecast(df, start, ndays, forecast, countries)
    df_forecast.to_csv('previsao.csv', index=False)

    plot_growth(df_forecast, ['P10', 'P50', 'P90'], max_days)
    scenario_df = df[df['location'] == 'Brazil']
    scenario_df = scenario_df[scenario_df['days'] <= max_days]
    plt.plot(scenario_df['days'], scenario_df['growth'], 'ko')

    plot_growth(df_forecast, countries, max_days)
    scenario_df = df[df['location'] == 'Brazil']
    scenario_df = scenario_df[scenario_df['days'] <= max_days]
    plt.plot(scenario_df['days'], scenario_df['growth'], 'ko')

    plot_growth(df_forecast, ['P50', 'Germany', 'Belgium', 'Netherlands'], max_days)
    scenario_df = df[df['location'] == 'Brazil']
    scenario_df = scenario_df[scenario_df['days'] <= max_days]
    plt.plot(scenario_df['days'], scenario_df['growth'], 'ko')
    
    plot_brazil_forecast(df_forecast, brazil_df, ['P10', 'P50', 'P90'], max_days)
    plot_brazil_forecast(df_forecast, brazil_df, ['Italy', 'Netherlands', 'Japan'], max_days)
    plot_brazil_forecast(df_forecast, brazil_df, countries, max_days)
    plot_brazil_forecast(df_forecast, brazil_df, ['P10', 'Japan', 'South Korea'], max_days)
    plot_brazil_forecast(df_forecast, brazil_df, ['P50', 'Germany', 'Belgium', 'Netherlands'], max_days)
    plot_brazil_forecast(df_forecast, brazil_df, ['P90', 'Iran', 'Spain', 'Italy'], max_days)
    #plot_brazil_forecast(df_forecast, brazil_df, ['Iran', 'Germany', 'Japan', 'Belgium', 'Netherlands'], max_days)
    #plot_brazil_forecast(df_forecast, brazil_df, ['Iran', 'Germany', 'Japan', 'Netherlands', 'Canada', 'Hong Kong'], max_days)
    #plot_brazil_forecast(df_forecast, brazil_df, ['Canada', 'Hong Kong'], max_days)
