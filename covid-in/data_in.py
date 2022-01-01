# This python file defines functions which are used for scraping data from the web and
# performs some pandas dataframe operations.
import csv
import requests
import pandas as pd
from bs4 import BeautifulSoup


# Web Scraping using BeautifulSoup
def web_scraping_in():
    try:
        url = 'https://www.mygov.in/covid-19'
        r = requests.get(url, timeout=5).text
        soup = BeautifulSoup(r, 'lxml')
        with open('/home/gokul/Downloads/covid_in.csv', 'w') as f:
            csv_writer = csv.writer(f)
            csv_writer.writerow(['state', 'cases', 'deaths'])
            count = 0
            for table in soup.find_all('div', class_='views-row'):
                count += 1
                st = table.find('span', class_='st_name')
                state = st.text
                print(state)
                cs = table.find('span', class_='st_number')
                cases = cs.text
                print(cases)
                dt = table.find('div', class_='tick-death')
                deaths = dt.small.text
                print(deaths)
                csv_writer.writerow([state, cases, deaths])
                if count == 36:
                    break
    except Exception as e:
        print(e)


# Reads the covid data
def covid_data_in():
    covid_in_df = pd.read_csv('/home/gokul/Downloads/covid_in.csv')
    covid_in_df.loc[7, 'state'] = 'DNH and DD'
    covid_in_df.loc[31, 'state'] = 'Telangana'
    for col in ['cases', 'deaths']:
        covid_in_df[col] = covid_in_df[col].str.replace(',', '').astype(int)
    return covid_in_df


# Reads the vaccine data
def vaccine_data_in():
    sheet1 = pd.read_excel('/home/gokul/Downloads/vaccine_in.xlsx', sheet_name=11, usecols=['title', 'total'])
    sheet2 = pd.read_excel('/home/gokul/Downloads/vaccine_in.xlsx', sheet_name=12)
    vaccine_in_df = sheet2.merge(sheet1, on='title')
    vaccine_in_df.columns = ['state', 'first_dose', 'second_dose', 'total_vaccinations']
    vaccine_in_df.loc[32, ['first_dose', 'second_dose', 'total_vaccinations']] \
        += vaccine_in_df.loc[34, ['first_dose', 'second_dose', 'total_vaccinations']]
    vaccine_in_df.drop(34, inplace=True)
    vaccine_in_df.loc[32, 'state'] = 'DNH and DD'
    vaccine_in_df.loc[33, 'state'] = 'Andaman and Nicobar'
    return vaccine_in_df


# Merge the two dataframes
def data_merge_in():
    covid_in = covid_data_in().merge(vaccine_data_in(), on='state')
    covid_in.to_csv('/home/gokul/Documents/DS/covid/covid_in.csv', index=None, header=True)


web_scraping_in()
data_merge_in()
