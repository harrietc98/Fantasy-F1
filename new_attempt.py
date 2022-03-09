## IMPORTS
import pandas as pd
from IPython.display import display
import requests
from bs4 import BeautifulSoup
import re
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time


## PREPPING TABLES
# Get driver and constructor table
url = r'https://en.wikipedia.org/wiki/2022_Formula_One_World_Championship'
wiki_table = pd.read_html(url)[0]
wiki_table = wiki_table.drop(columns=['Entrant', 'Chassis', 'Power unit'], axis=1)
wiki_table = wiki_table[0:]
wiki_table.columns = ['Constructor', 'Number', 'Driver']
wiki_table = wiki_table.drop(columns=['Number'], axis=1)
wiki_table.drop(wiki_table.tail(1).index,inplace=True)
try:
    wiki_table['Driver'] = wiki_table['Driver'].apply(lambda x : re.findall(r"[\w']+\s[\w']+",x)[0])
except:
    pass
wiki_table['Constructor'] = wiki_table['Constructor'].apply(lambda x : re.findall(r"([\w']+\s[\w']+|[\w']+)",x)[0])

# Get pricing table
driver = webdriver.Chrome()
url = r'https://www.f1fantasytracker.com/prices.html'
driver.get(url)
time.sleep(1)
soup = BeautifulSoup(driver.page_source, 'html.parser')
tag = 'table'
attributes = {'id':'driverTable'}
table_soup = soup.find(tag,attributes)
price_table = pd.read_html(str(table_soup))[0]
driver.close()

price_table['Driver'] = price_table['Driver'].apply(lambda x : re.findall(r"[\w']+\s[\w']+",x)[0])
price_table.rename(columns={'Season Start PriceSeason Price': 'Start Price'}, inplace=True)
price_table['Current Price'] = price_table['Current Price'].apply(lambda x: x.replace('$','').replace('m',''))
price_table['Start Price'] = price_table['Start Price'].apply(lambda x: x.replace('$','').replace('m',''))
price_table['Driver'] = price_table['Driver'].replace('SAI Carlos','Carlos Sainz Jr.')
price_table['Driver'] = price_table['Driver'].replace('Sergio Perez','Sergio Pérez')


# Combine tables
df = pd.merge(wiki_table, price_table, on ='Driver', how ="left")
df = df.sort_values(by=['Points/Million'], ascending=False)
display(df)


##LETS GET DOWN TO BUSINESS

## REST UP BABIES
def drivers_not_racing():
    return []


## CHOOSE BEST TEAM
def make_best_team(budget=100, no_drivers=6, con=1):
    best_team = []
    budget = budget
    not_racing = drivers_not_racing()
    for index, row in df.iterrows():
        if len(best_team) < no_drivers and row['Driver'] not in not_racing and budget >= float(row['Current Price']):
            best_team.append(row['Driver'])
            budget -= float(row['Current Price'])
    return best_team, budget

    
a, b = make_best_team()
print('Best team: ',a)
print('Leftover money: $',b)

