# -*- coding: utf-8 -*-
"""
Created on Sat Mar 21 09:43:06 2020

@author: Erico
"""
import pandas as pd

def get_covid_data():
    url = "https://covid.ourworldindata.org/data/ecdc/full_data.csv"
    return pd.read_csv(url)

a = get_covid_data()
print(a)
