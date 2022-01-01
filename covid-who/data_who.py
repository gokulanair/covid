# This python file defines functions which performs some pandas dataframe operations.
import pandas as pd


# Reads the covid data
def covid_data_who():
    url = 'https://covid19.who.int/WHO-COVID-19-global-table-data.csv'
    covid_who_df = pd.read_csv(url, usecols=[1, 2, 3, 7, 8])
    # covid__who_df = pd.read_csv('/home/gokul/Downloads/covid_who.csv', usecols=[1, 2, 3, 7, 8])
    covid_who_df.reset_index(level=0, inplace=True)
    covid_who_df.columns = ['country', 'region', 'cases', 'cases_per_100000', 'deaths', 'deaths_per_100000']
    covid_who_df.drop(index=0, inplace=True)
    covid_who_df.reset_index(drop=True, inplace=True)
    return covid_who_df


# Reads the vaccine data
def vaccine_data_who():
    url = 'https://covid19.who.int/who-data/vaccination-data.csv'
    vaccine_who_df = pd.read_csv(url, usecols=[0, 5, 6, 7, 8, 9, 10])
    # vaccine_who_df = pd.read_csv('/home/gokul/Downloads/vaccine_who.csv', usecols=[0, 5, 6, 7, 8, 9, 10])
    vaccine_who_df.columns = ['country', 'total_vaccinations', 'first_dose', 'vaccinations_per_100',
                              'first_dose_per_100', 'second_dose', 'second_dose_per_100']
    return vaccine_who_df


# Merge the two dataframes
def data_merge_who():
    covid_who = covid_data_who().merge(vaccine_data_who(), on='country', how='inner')
    covid_who.to_csv('/home/gokul/Documents/DS/covid/covid_who.csv', index=None, header=True)


data_merge_who()
