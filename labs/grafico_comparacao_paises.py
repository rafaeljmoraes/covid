# -*- coding: utf-8 -*-
"""
Created on Sat Mar 21 09:43:06 2020

@author: Erico
"""

from CovidDatabase import CovidDatabase
from Plot import Plot

              
if __name__ == '__main__':
    covid_database = CovidDatabase()
    minimal_cases = 100
    covid_database.build_days_column(minimal_cases)
    df = covid_database.get_data()

    plot1 = Plot(covid_database)
    plot1.create_plot(minimal_cases, 5e-4, True, None, 'normalized.png')

    plot2 = Plot(covid_database)
    plot2.create_plot(minimal_cases, 2.3e-4, True, None, 'normalized2.png')

    plot3 = Plot(covid_database)
    plot3.create_plot(minimal_cases, 2000, False, None, 'absolute.png')
