# -*- coding: utf-8 -*-
"""
Created on Sun Mar 22 10:24:12 2020

@author: Erico
"""

import pandas as pd

class CovidDatabase:
    def __init__(self):
        self._covid_data = self._get_covid_data()
        self._population_data = self._get_population_data()
        
    def _get_covid_data(self):
        url = "https://covid.ourworldindata.org/data/ecdc/full_data.csv"
        return pd.read_csv(url)

    def _get_population_data(self):
        url = "100005.csv"
        return pd.read_csv(url)
    
    def build_days_column(self, minimal_cases = 1):
        df = self._covid_data
        df = df.loc[:, ['date', 'location', 'total_cases']]
        df = df[df['total_cases'] >= minimal_cases]
        df['days'] = 0
        
        countries = df['location'].drop_duplicates()
        for country in countries:
            country_df = df[df['location'] == country]
            index = country_df.index
            df.loc[index, 'days'] = range(1, index.size + 1)
        self._covid_data = df
        
    def get_country_population(self, country):
        df = self._population_data

        result = df[df['Location'] == country]['PopTotal']
        if result.empty:
            return 0
        else:
            return int(result)

    def get_data(self):
        return self._covid_data
